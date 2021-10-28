"""
This is for pushing all the tsv files to wandb
"""

import argparse
from storyteller.connectors import connect_to_wandb
from storyteller.paths import WISDOMIFY_TEST_TSV, WISDOM2DEF_DIR, WISDOM2EG_DIR, WISDOMS_TXT
from storyteller.uploaders import upload_dir, upload_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact_name", type=str,
                        default="wisdoms")
    args = parser.parse_args()
    artifact_name: str = args.artifact_name
    # --- instantiate an uploader --- #
    run = connect_to_wandb(name="storyteller.main.upload")
    if artifact_name == "wisdomify_test":
        upload_file(run=run, local_file_path=WISDOMIFY_TEST_TSV, artifact_name=artifact_name, type="dataset",
                    desc="The very wisdomify test - This is to be used to compare all the RD's")
    elif artifact_name == "wisdoms":
        upload_file(run=run, local_file_path=WISDOMS_TXT,
                    artifact_name=artifact_name, type="dataset", desc="The vocabulary of wisdoms to search for")
    elif artifact_name == "wisdom2def":
        upload_dir(run=run, local_dir_path=WISDOM2DEF_DIR, artifact_name=artifact_name,
                   type="dataset", desc="The definitions of Korean proverbs")
    elif artifact_name == "wisdom2eg":
        upload_dir(run=run, local_dir_path=WISDOM2EG_DIR, artifact_name=artifact_name,
                   type="dataset", desc="The examples of Korean proverbs")


if __name__ == '__main__':
    main()
