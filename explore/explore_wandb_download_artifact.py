from storyteller.connectors import connect_to_wandb
from storyteller.paths import ARTIFACTS_DIR


def main():
    run = connect_to_wandb(name="explore_wandb_download_artifact", notes="just exploring artifact.download()")
    # just trying to download the test query.
    artifact = run.use_artifact(artifact_or_name="wisdom2query:latest")
    # what does an artifact contains? - it houses the metadata of the artifact.
    # this will download the file from:
    # https://wandb.ai/wisdomify/wisdomify/artifacts/dataset/test_query/e2d32531b72bfb4f3108/files
    artifact.download(root=ARTIFACTS_DIR)  # does this overwrite a previously existing file? - yes, it does!


if __name__ == '__main__':
    main()
