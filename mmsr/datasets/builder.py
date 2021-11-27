import copy

from torch.utils.data import ConcatDataset

from lmmcv.utils import build_from_cfg
from .dataset_wrappers import RepeatDataset
from .registry import DATASETS


def _concat_dataset(cfg, default_args=None):
    """Concat datasets with different ann_file but the same type.

    Args:
        cfg (dict): The config of dataset.
        default_args (dict, optional): Default initialization arguments.
            Default: None.

    Returns:
        Dataset: The concatenated dataset.
    """
    ann_files = cfg['ann_file']

    datasets = []
    num_dset = len(ann_files)
    for i in range(num_dset):
        data_cfg = copy.deepcopy(cfg)
        data_cfg['ann_file'] = ann_files[i]
        datasets.append(build_dataset(data_cfg, default_args))

    return ConcatDataset(datasets)


def build_dataset(cfg, default_args=None):
    """Build a dataset from config dict.

    It supports a variety of dataset config. If ``cfg`` is a Sequential (list
    or dict), it will be a concatenated dataset of the datasets specified by
    the Sequential. If it is a ``RepeatDataset``, then it will repeat the
    dataset ``cfg['dataset']`` for ``cfg['times']`` times. If the ``ann_file``
    of the dataset is a Sequential, then it will build a concatenated dataset
    with the same dataset type but different ``ann_file``.

    Args:
        cfg (dict): Config dict. It should at least contain the key "type".
        default_args (dict, optional): Default initialization arguments.
            Default: None.

    Returns:
        Dataset: The constructed dataset.
    """
    if isinstance(cfg, (list, tuple)):      # 是元组中的一个返回 True
        dataset = ConcatDataset([build_dataset(c, default_args) for c in cfg])      # 合并子数据集
    elif cfg['type'] == 'RepeatDataset':
        dataset = RepeatDataset(
            build_dataset(cfg['dataset'], default_args), cfg['times'])
    elif isinstance(cfg.get('ann_file'), (list, tuple)):
        dataset = _concat_dataset(cfg, default_args)
    else:
        dataset = build_from_cfg(cfg, DATASETS, default_args)

    return dataset
