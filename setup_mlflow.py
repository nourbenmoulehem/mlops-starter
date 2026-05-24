# run once against a fresh MLflow instance:
# MLFLOW_TRACKING_URI=http://mlflow.lan uv run setup_mlflow.py

# why MLFLOW_TRACKING_URI=http://mlflow.lan  ? injecting the env var into the process, and MLflow picks it up without you having to write anything in the file

# mlflow does this under the hood : os.environ.get("MLFLOW_TRACKING_URI")


import mlflow

experiment_id = mlflow.create_experiment('iris', artifact_location='mlflow-artifacts:/iris')
print(f"created experiment 'iris' with id {experiment_id}")


'''
experiments is just a table mlflow uses to group models, it's like namespace in k8s, for organizationnal puropses


An experiment is just a label. When you train a model, MLflow needs to know two things:

  What group does this training run belong to? → the experiment name
  Where should I store the model files? → the artifact location

Artifact location could be:
  * A local path: /home/nourbenmoulehem/mlops-demo/mlruns — only accessible on that specific machine
  
  * An HTTP path: mlflow-artifacts:/iris — served by MLflow over HTTP, accessible from anywhere


What group does this training run belong to? → the experiment name
Where should I store the model files? → the artifact location
'''