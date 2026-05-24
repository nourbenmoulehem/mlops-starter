import mlflow.sklearn
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# load the latest saved model from mlflow, currently in Production (champion alias)
model = mlflow.sklearn.load_model("models:/iris-classifier@champion")



class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

CLASSES = ["setosa", "versicolor", "virginica"]

@app.post("/predict")
def predict(data: IrisInput):
    features = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])
    prediction = model.predict(features)[0]
    return {
        "prediction": int(prediction),
        "class_name": CLASSES[prediction]
    }