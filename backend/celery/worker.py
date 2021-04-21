from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

# Array of all URLs for partner api endpoints
urls = ["https://f21c7154-fa77-4f81-89f1-2f254714f45c.mock.pstmn.io/api"]


app = Celery("tasks")
app.conf.broker_url = "redis://localhost:6379/0"
app.conf.result_backend = "redis://localhost:6379/0"


app.conf.beat_schedule = {
    "refresh": {
        "task": "refresh",
        "schedule": crontab(hour="*/12"),
        "args": ([urls]),
    }
}

app.conf.result_backend_transport_options = {"retry_policy": {"timeout": 5.0}}
