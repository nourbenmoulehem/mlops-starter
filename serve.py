import mlflow.sklearn
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from prometheus_client import Histogram, Counter, make_asgi_app


app = FastAPI()

# load the latest saved model from mlflow, currently in Production (champion alias)
model = mlflow.sklearn.load_model("models:/iris-classifier@champion")


metrics_app = make_asgi_app() # mini app that declares the metrics and format them for prometheus
app.mount("/metrics", metrics_app)


# now we're declaring our metrics:
sepal_length_hist = Histogram(
    "iris_sepal_length_cm",
    "Sepal length distribution",
    buckets=[4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]
)
petal_length_hist = Histogram(
    "iris_petal_length_cm",
    "Petal length distribution",
    buckets=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
)
prediction_counter = Counter(
    "iris_predictions_total",
    "Predictions by class",
    ["class_name"]
)


class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

CLASSES = ["setosa", "versicolor", "virginica"]


# this is a comment to test ci github actions, updating this comment again after fixinf dir name in .github??!!
@app.post("/predict")
def predict(data: IrisInput):
    features = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])

    sepal_length_hist.observe(data.sepal_length)
    petal_length_hist.observe(data.petal_length)


    prediction = model.predict(features)[0]

    prediction_counter.labels(class_name=CLASSES[prediction]).inc()

    return {
        "prediction": int(prediction),
        "class_name": CLASSES[prediction]
    }