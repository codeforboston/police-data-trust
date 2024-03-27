from mixpanel import Mixpanel
from backend.config import Config
from ua_parser import user_agent_parser
from flask_jwt_extended import get_jwt

# Path: backend/mixpanel/mix.py

config = Config()

# Mixpanel connection
mp = Mixpanel(config.MIXPANEL_TOKEN)


def track_to_mp(request, event_name, properties):
    parsed = user_agent_parser.Parse(request.headers["User-Agent"])

    # Set parsed values as properties.
    # You can also parse out the browser/device/os versions.
    properties.update(
        {
            "$browser": parsed["user_agent"]["family"],
            "$device": parsed["device"]["family"],
            "$os": parsed["os"]["family"],
        }
    )

    if "user_id" not in properties:
        user_id = get_jwt()["sub"]
    else:
        user_id = properties["user_id"]

    properties["ip"] = request.remote_addr
    mp.track(user_id, event_name, properties)
