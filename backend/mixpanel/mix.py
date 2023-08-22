from mixpanel import Mixpanel
from ua_parser import user_agent_parser
from flask_jwt_extended import get_jwt

from backend import config
# Path: backend/mixpanel/mix.py

# Mixpanel connection
mp = Mixpanel.init(config.MIXPANEL_TOKEN)


def track_to_mp(request, event_name, properties):
    parsed = user_agent_parser.Parse(request.headers["User-Agent"])

    # Set parsed values as properties.
    # You can also parse out the browser/device/os versions.
    properties.update({
        "$browser": parsed["user_agent"]["family"],
        "$device": parsed["device"]["family"],
        "$os": parsed["os"]["family"],
    })

    if properties["user_id"] is None:
        user_id = get_jwt()["sub"]
    else:
        user_id = properties["user_id"]

    properties["ip"] = request.remote_addr
    mp.track(user_id, event_name, properties)
