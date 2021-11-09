import json
from typing import List
import pandas as pd
import wandb
from tqdm import tqdm
from metaflow import FlowSpec, step, Parameter
from wandb.integration.metaflow import wandb_log
from storyteller.constants import WANDB_PROJECT
from storyteller.connectors import connect_to_es
from storyteller.downloaders import dl_wisdoms
from storyteller.elastic.docs import Story
from storyteller.elastic.searcher import Searcher
from storyteller.preprocess import parse, cleanse, normalise, augment, upsample


class BuildWisdom2EgFlow(FlowSpec):
    ver: str = Parameter('ver',
                         type=str,
                         help='The version of this artifact. Should be a single alphabet',
                         default="a")

    wisdoms: List[str]
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
        self.wisdoms = dl_wisdoms(self.ver)
        self.next(self.search)

    @step
    def search(self):
        """
        ver -> raw_df
        """
        # ---
        rows = list()
        with connect_to_es() as es:
            searcher = Searcher(es)
            for wisdom in tqdm(self.wisdoms, desc="searching for wisdoms on stories...",
                               total=len(self.wisdoms)):
                raw = searcher(wisdom, ",".join(Story.all_indices()), size=10000)
                # https://stackoverflow.com/a/18337754
                raw = json.dumps(raw, ensure_ascii=False)
                rows.append((wisdom, raw))
        self.raw_df = pd.DataFrame(data=rows, columns=["wisdom", "eg"])
        self.next(self.preprocess)

    @step
    def preprocess(self):
        """
        raw_df -> all_df
        """
        self.all_df = self.raw_df \
                          .pipe(parse) \
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
        -> wisdom2eg_artifact
        """
        artifact = wandb.Artifact("wisdom2eg", type="dataset")
        raw_table = wandb.Table(dataframe=self.raw_df)
        all_table = wandb.Table(dataframe=self.all_df)
        # add the tables to the artifact
        artifact.add(raw_table, "raw")
        artifact.add(all_table, "all")
        wandb.log_artifact(artifact, aliases=[self.ver, "latest"])


if __name__ == '__main__':
    BuildWisdom2EgFlow()
