from storyteller.connectors import connect_wandb
from storyteller.paths import WISDOM2EG_TEST_TSV
import wandb


def main():
    run = connect_wandb(name="explore_wandb_create_artifact", notes="just exploring artifact.download()")
    # the first version of wisdom2eg_test - we manage this with
    artifact = wandb.Artifact(name="wisdom2eg_test", type="dataset",
                              description="The test dataset to be used for comparing all rd's")
    artifact.add_file(WISDOM2EG_TEST_TSV, name="wisdom2eg_test.tsv")
    run.log_artifact(artifact)
    # and then, wandb will automatically finish the run as soon as the script finishes.


if __name__ == '__main__':
    main()
