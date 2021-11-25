from decouple import Config
from os import path

from .base import *

DEBUG = config("DEBUG", False, cast=bool)


if DEBUG:
    from .development import *
else:
    from .production import *


STATIC_ROOT = path.join(BASE_DIR, "live/static")
