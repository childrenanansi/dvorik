from .global_settings import *
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '..', 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'