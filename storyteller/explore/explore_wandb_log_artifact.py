from storyteller.connectors import connect_to_wandb
from storyteller.paths import WISDOMIFY_TEST_TSV
import wandb


def main():
    run = connect_to_wandb(name="explore_wandb_log_artifact", notes="just exploring artifact.download()")
    # the first version of wisdom2eg_test - we manage this with
    artifact = wandb.Artifact(name="wisdomify_test", type="dataset",
                              description="The test dataset to be used for comparing all the rd's")
    artifact.add_file(WISDOMIFY_TEST_TSV, name="wisdomify_test.tsv")
    run.log_artifact(artifact)
    # and then, wandb will automatically finish the run as soon as the script finishes.


if __name__ == '__main__':
    main()