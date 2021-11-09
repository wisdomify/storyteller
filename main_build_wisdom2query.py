import io
import wandb
import pandas as pd
from metaflow import FlowSpec, step, Parameter
from wandb.integration.metaflow import wandb_log
from storyteller.utils import get
from storyteller.constants import WISDOM2QUERY_RAW_A, WANDB_PROJECT
from storyteller.preprocess import cleanse, normalise, stratified_split


class BuildWisdom2QueryFlow(FlowSpec):
    # get the version of this artifact from command line
    # """https://github.com/Netflix/metaflow/issues/175#issuecomment-610518458"""
    ver: str = Parameter('ver',
                         type=str,
                         help='The version of this artifact. Should be a single alphabet',
                         default="a")

    val_ratio = Parameter('val_ratio',
                          type=float,
                          help='The percentage of the validation set',
                          default=0.2)
    seed = Parameter('seed',
                     type=int,
                     help='random seed',
                     default=410)
    # --- to be saved locally --- #
    raw_df: pd.DataFrame
    all_df: pd.DataFrame
    val_df: pd.DataFrame
    test_df: pd.DataFrame

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
            text = get(WISDOM2QUERY_RAW_A)
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
                          .pipe(normalise)
        self.next(self.val_test_split)

    @step
    def val_test_split(self):
        """
        all_df -> val_df, test_df
        """
        self.val_ratio: float
        self.seed: int
        self.val_df, self.test_df = stratified_split(self.raw_df, self.val_ratio, self.seed)
        self.next(self.end)

    @step
    @wandb_log(settings=wandb.Settings(project=WANDB_PROJECT))
    def end(self):
        """
        raw_df, all_df, val_df, test_df
        -> raw_table, all_table, val_table, test_table
        -> artifact: upload this
        """
        artifact = wandb.Artifact("wisdom2query", type="dataset")
        artifact.metadata = {"ver": self.ver, "seed": self.seed}
        raw_table = wandb.Table(dataframe=self.raw_df)
        all_table = wandb.Table(dataframe=self.all_df)
        val_table = wandb.Table(dataframe=self.val_df)
        test_table = wandb.Table(dataframe=self.test_df)
        # add the tables to the artifact
        artifact.add(raw_table, "raw")
        artifact.add(all_table, "all")
        artifact.add(val_table, "val")
        artifact.add(test_table, "test")
        wandb.log_artifact(artifact, aliases=[self.ver, "latest"])


if __name__ == '__main__':
    BuildWisdom2QueryFlow()
