import io
import wandb
import pandas as pd
from metaflow import FlowSpec, step, Parameter
from wandb.integration.metaflow import wandb_log
from storyteller.constants import WISDOM2DEF_RAW_A, WISDOM2DEF_RAW_B, WANDB_PROJECT
from storyteller.preprocess import cleanse, normalise, augment, upsample
from storyteller.utils import get_url


class BuildWisdom2DefFlow(FlowSpec):
    ver: str = Parameter('ver',
                         type=str,
                         help='The version of this artifact. Should be a single alphabet',
                         default="a")

    raw_df: pd.DataFrame
    all_df: pd.DataFrame

    @step
    def start(self):
        """
        set ver to be available
        """
        self.next(self.download)

    @step
    def download(self):
        """
        ver  -> raw_df
        """
        if self.ver == "a":
            text = get_url(WISDOM2DEF_RAW_A)
        elif self.ver == "b":
            text = get_url(WISDOM2DEF_RAW_B)
        else:
            raise ValueError
        self.raw_df = pd.read_csv(io.StringIO(text), delimiter="\t")
        self.next(self.preprocess)

    @step
    def preprocess(self):
        """
        raw_df -> all_df
        """
        self.all_df = self.raw_df \
                          .pipe(cleanse) \
                          .pipe(normalise) \
                          .pipe(augment) \
                          .pipe(upsample)
        self.next(self.end)

    @step
    @wandb_log(settings=wandb.Settings(project=WANDB_PROJECT))
    def end(self):
        """
        raw_df, all_df
        -> raw_table, all_table
        -> artifact: upload this
        """
        artifact = wandb.Artifact("wisdom2def", type="dataset")
        raw_table = wandb.Table(dataframe=self.raw_df)
        all_table = wandb.Table(dataframe=self.all_df)
        # add the tables to the artifact
        artifact.add(raw_table, "raw")
        artifact.add(all_table, "all")
        wandb.log_artifact(artifact, aliases=[self.ver, "latest"])


if __name__ == '__main__':
    BuildWisdom2DefFlow()
