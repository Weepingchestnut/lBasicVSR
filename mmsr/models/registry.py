from lmmcv.cnn import MODELS as LMMCV_MODELS
from lmmcv.utils import Registry

MODELS = Registry('model', parent=LMMCV_MODELS)
BACKBONES = MODELS
COMPONENTS = MODELS
LOSSES = MODELS
