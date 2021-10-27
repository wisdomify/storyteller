from wandb.sdk.wandb_run import Run
import wandb


def upload_file(run: Run, local_file_path: str, artifact_name: str, desc: str, **kwargs):
    artifact = wandb.Artifact(name=artifact_name, description=desc, **kwargs)
    artifact.add_file(local_file_path)
    run.log_artifact(artifact)


def upload_dir(run: Run, self, local_dir_path: str, artifact_name: str, desc: str, **kwargs):
    artifact = wandb.Artifact(name=artifact_name, description=desc, **kwargs)
    artifact.add_dir(local_dir_path)
    run.log_artifact(artifact)
