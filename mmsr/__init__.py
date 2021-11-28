import lmmcv

from .version import __version__

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

