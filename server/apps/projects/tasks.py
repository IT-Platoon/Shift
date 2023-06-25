import os

from apps.core.services import send_email
from apps.projects.machine_learning import main, utils
from apps.projects.models import ModelProcess
from config.celery import app


@app.task
def model_predict(model_id: int, email: str) -> None:
    model = ModelProcess.objects.select_related("project").get(pk=model_id)
    path = "media/" + model.request_file.name
    response = main(path)
    model.graphic = response
    model.save()
    if email:
        created_date = model.created.date()
        created_time = model.created.time().replace(microsecond=0)
        email_context = {
            "name": model.project.name,
            "created": f"{created_date} {created_time}",
        }
        send_email("info", email_context, [email])
