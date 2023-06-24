import os

from apps.core.services import send_email
from apps.projects.machine_learning import main, utils
from apps.projects.models import ModelProcess
from config.celery import app


@app.task
def model_predict(model_id: int, email: str) -> None:
    model = ModelProcess.objects.select_related("project").get(pk=model_id)
    graphic = {
        "labels": [
            "01 Jan 2001",
            "02 Jan 2001",
            "03 Jan 2001",
            "04 Jan 2001",
            "05 Jan 2001",
            "06 Jan 2001",
            "07 Jan 2001",
            "08 Jan 2001",
            "09 Jan 2001",
            "10 Jan 2001",
            "11 Jan 2001",
            "12 Jan 2001",
        ],
        "datasets": [
            {
                "data": [
                    440,
                    505,
                    414,
                    671,
                    227,
                    413,
                    201,
                    352,
                    752,
                    320,
                    257,
                    160,
                ],
                "label": "Website Blog",
                "type": "bar",
            },
            {
                "data": [
                    23,
                    42,
                    35,
                    27,
                    43,
                    22,
                    17,
                    31,
                    22,
                    22,
                    12,
                    16,
                ],
                "label": "Social Media",
                "type": "line",
            },
        ],
    }
    path = "media/" + model.request_file.name
    response = main(path)
    print(f"1 {response}")
    response = main(os.path.abspath(path))
    print(f"2 {response}")
    model.graphic = graphic
    model.save()
    if email:
        created_date = model.created.date()
        created_time = model.created.time().replace(microsecond=0)
        email_context = {
            "name": model.project.name,
            "created": f"{created_date} {created_time}",
        }
        send_email("info", email_context, [email])
