import math

import torch
import torch.nn as nn
import torch.nn.functional as F
from lmmcv.runner import load_checkpoint

from mmsr.datasets.pipelines.utils import make_coord
from mmsr.models.builder import build_backbone, build_component
from mmsr.models.registry import BACKBONES
from mmsr.utils import get_root_logger








class MeanShift(nn.Conv2d):
    def __init__(self, rgb_range, rgb_mean, rgb_std, sign=-1):
        super(MeanShift, self).__init__(3, 3, kernel_size=1)
        std = torch.Tensor(rgb_std)
        self.weight.data = torch.eye(3).view(3, 3, 1, 1)
        self.weight.data.div_(std.view(3, 1, 1, 1))
        self.bias.data = sign * rgb_range * torch.Tensor(rgb_mean)
        self.bias.data.div_(std)
        self.requires_grad = False


class MetaSR(nn.Module):
    def __init__(self,
                 flm,   # feature learning module
                 upscale,
                 rgb_mean=[0.4488, 0.4371, 0.4040],
                 rgb_std=[1.0, 1.0, 1.0]):
        super(MetaSR, self).__init__()

        # rgb_mean = (0.4488, 0.4371, 0.4040)
        # rgb_std = (1.0, 1.0, 1.0)
        # self.sub_mean = MeanShift(255, rgb_mean, rgb_std)
        # self.add_mean = MeanShift(255, rgb_mean, rgb_std, 1)

        self.mean = torch.Tensor(rgb_mean).view(1, -1, 1, 1)
        self.std = torch.Tensor(rgb_std).view(1, -1, 1, 1)

        # model
        self.encoder = build_backbone(flm)
        self.upscale = build_backbone(upscale)

        # position to weight
        # self.P2W = Pos2Weight(inC=encoder.mid_channels)

    def forward(self, x, scale):
        """Forward function

        Args:
            x: input tensor

        Returns:

        """

        self.mean = self.mean.to(x)

        feature = self.gen_fearture(x)
        sr = self.upscale(feature, scale)

        self.std = self.std.to(x)

        return sr


@BACKBONES.register_module()
class MetaEDSR(MetaSR):
    def __init__(self,
                 flm,
                 upscale):
        super(MetaEDSR, self).__init__(
            flm=flm,
            upscale=upscale)

        self.conv_first = self.flm.conv_first
        self.body = self.flm.body
        self.conv_after_body = self.encoder.conv_afer_body
        del self.encoder

    def gen_feature(self, x):
        """Generate feature.

        Args:
            x (Tensor): Input tensor with shape (n, c, h, w).

        Returns:
            Tensor: Forward results.
        """

        x = self.conv_first(x)
        res = self.body(x)
        res = self.conv_after_body(res)
        res += x

        return res


@BACKBONES.register_module()
class MetaRDN(MetaSR):
    def __init__(self,
                 flm,
                 upscale):
        super().__init__(
            flm=flm,
            upscale=upscale)

        self.sfe1 = self.encoder.sfe1  # Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.sfe2 = self.encoder.sfe2  # Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.rdbs = self.encoder.rdbs
        self.gff = self.encoder.gff  # # 1x1 Conv(1024 -> 64) => 3x3 Conv(64 -> 64)
        self.num_blocks = self.encoder.num_blocks
        del self.encoder

    def gen_feature(self, x):
        """Generate feature.

        Args:
            x (Tensor): Input tensor with shape (n, c, h, w).

        Returns:
            Tensor: Forward results.
        """

        sfe1 = self.sfe1(x)
        sfe2 = self.sfe2(sfe1)

        x = sfe2
        local_features = []
        for i in range(self.num_blocks):
            x = self.rdbs[i](x)
            local_features.append(x)

        x = self.gff(torch.cat(local_features, 1)) + sfe1

        return x
