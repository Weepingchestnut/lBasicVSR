import lmmcv

from .version import __version__, version_info

try:
    from lmmcv.utils import digit_version
except ImportError:

    def digit_version(version_str):
        digit_ver = []
        for x in version_str.split('.'):
            if x.isdigit():
                digit_ver.append(int(x))
            elif x.find('rc') != -1:
                patch_version = x.split('rc')
                digit_ver.append(int(patch_version[0]) - 1)
                digit_ver.append(int(patch_version[1]))
        return digit_ver


LMMCV_MIN = '1.0.0'
LMMCV_MAX = '1.6'

lmmcv_min_version = digit_version(LMMCV_MIN)
lmmcv_max_version = digit_version(LMMCV_MAX)
lmmcv_version = digit_version(lmmcv.__version__)


assert (lmmcv_min_version <= lmmcv_version <= lmmcv_max_version), \
    f'mmcv=={lmmcv.__version__} is used but incompatible. ' \
    f'Please install mmcv-full>={lmmcv_min_version}, <={lmmcv_max_version}.'

__all__ = ['__version__', 'version_info']
