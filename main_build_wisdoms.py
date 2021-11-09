import io
import wandb
import pandas as pd
from wandb.integration.metaflow import wandb_log
from metaflow import FlowSpec, step, Parameter
from storyteller.utils import get
from storyteller.constants import WISDOMS_A, WISDOMS_B, WANDB_PROJECT


class BuildWisdomsFlow(FlowSpec):
    # get the version of this artifact from command line
    # """https://github.com/Netflix/metaflow/issues/175#issuecomment-610518458"""
    ver: str = Parameter('ver',
                         type=str,
                         help='The version of this artifact. Should be a single alphabet',
                         default="a")

    # --- to be saved locally --- #
    all_df: pd.DataFrame

    @step
    def start(self):
        self.next(self.download)

    @step
    def download(self):
        """
        ver  -> all_df
        """
        if self.ver == "a":
            text = get(WISDOMS_A)
        elif self.ver == "b":
            text = get(WISDOMS_B)
        else:
            raise ValueError
        self.all_df = pd.read_csv(io.StringIO(text), delimiter="\t")
        self.next(self.end)

    @step
    @wandb_log(settings=wandb.Settings(project=WANDB_PROJECT))
    def end(self):
        """
        package the dataframes into an artifact
        """
        artifact = wandb.Artifact(name="wisdoms", type="dataset")
        table = wandb.Table(dataframe=self.all_df)
        artifact.add(table, name="all")
        wandb.log_artifact(artifact, aliases=[self.ver, "latest"])


if __name__ == '__main__':
    # --- we register them here so that .metaflow directory is created under storyteller/main --- #
    BuildWisdomsFlow()

