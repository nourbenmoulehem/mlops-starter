import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import mlflow
from mlflow.tracking import MlflowClient

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# mlflow tracks everything inside this block
with mlflow.start_run():

    
    n_estimators = 100
    max_depth = 3

    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # train
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)

  
    acc = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", acc)

    # save the model as an artifact
    mlflow.sklearn.log_model(model, "iris_model")

    print(f"accuracy: {acc:.3f}")
    print("model saved to mlflow")


    # after your training run, register the model
    model_uri = f"runs:/{mlflow.active_run().info.run_id}/iris_model"

    registered = mlflow.register_model(model_uri, "iris-classifier")

    # promote it to Production
    client = MlflowClient()
    client.transition_model_version_stage(
        name="iris-classifier",
        version=registered.version,
        stage="Production"
    )
    print(f"version {registered.version} promoted to Production")