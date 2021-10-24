"""
This is for pushing all the tsv files to wandb
"""

import argparse
import wandb
from wandb.sdk.wandb_run import Run

from storyteller.connectors import connect_to_wandb
from storyteller.paths import WISDOMIFY_TEST_TSV, WISDOM2DEF_DIR, WISDOM2EG_DIR, WISDOMS_TXT


class Uploader:
    def __init__(self, run: Run):
        self.run = run

    def file(self, local_file_path: str, artifact_name: str, desc: str, **kwargs):
        artifact = wandb.Artifact(name=artifact_name, description=desc, **kwargs)
        artifact.add_file(local_file_path)
        self.run.log_artifact(artifact)

    def dir(self, local_dir_path: str, artifact_name: str, desc: str, **kwargs):
        artifact = wandb.Artifact(name=artifact_name, description=desc, **kwargs)
        artifact.add_dir(local_dir_path)
        self.run.log_artifact(artifact)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact_name", type=str,
                        default="wisdoms")
    args = parser.parse_args()
    artifact_name: str = args.artifact_name
    # --- instantiate an uploader --- #
    run = connect_to_wandb(name="storyteller.main.upload")
    uploader = Uploader(run)
    if artifact_name == "wisdomify_test":
        uploader.file(local_file_path=WISDOMIFY_TEST_TSV, artifact_name=artifact_name,
                      type="dataset", desc="The very wisdomify test - This is to be used to compare all the RD's")
    elif artifact_name == "wisdoms":
        uploader.file(local_file_path=WISDOMS_TXT, artifact_name=artifact_name,
                      type="dataset", desc="The vocabulary of wisdoms to search for")
    elif artifact_name == "wisdom2def":
        uploader.dir(local_dir_path=WISDOM2DEF_DIR, artifact_name=artifact_name,
                     type="dataset", desc="The definitions of Korean proverbs")
    elif artifact_name == "wisdom2eg":
        uploader.dir(local_dir_path=WISDOM2EG_DIR, artifact_name=artifact_name,
                     type="dataset", desc="The examples of Korean proverbs")


if __name__ == '__main__':
    main()
