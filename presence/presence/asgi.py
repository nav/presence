import os
from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presence.live_settings")

channel_layer = get_channel_layer()
