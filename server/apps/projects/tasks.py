from apps.projects.models import ModelProcess, ModelGraphics
from config.celery import app


@app.task
def model_predict(model_id: int) -> None:
    model = ModelProcess.objects.get(pk=model_id)
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
    model_graphic = ModelGraphics.objects.create(
        model=model, graphic=graphic,
    )
