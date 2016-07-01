from channels.routing import route
from apps.presence import consumers as presence_consumers
from apps.whiteboard import consumers as whiteboard_consumers

channel_routing = [
    # route("http.request", "apps.presence.consumers.http_consumer"),
    route("websocket.connect", presence_consumers.ws_connect, path=r"^/presence/$"),
    route("websocket.receive", presence_consumers.ws_message, path=r"^/presence/$"),
    route("websocket.disconnect", presence_consumers.ws_disconnect, path=r"^/presence/$"),

    route("websocket.connect", whiteboard_consumers.ws_connect, path=r"^/whiteboard/$"),
    route("websocket.receive", whiteboard_consumers.ws_message, path=r"^/whiteboard/$"),
    route("websocket.disconnect", whiteboard_consumers.ws_disconnect, path=r"^/whiteboard/$"),
]
