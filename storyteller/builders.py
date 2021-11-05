import wandb
import pandas as pd
from storyteller.connectors import connect_to_es
from storyteller.downloaders import dl_wisdoms, dl_wisdom2test, dl_wisdom2def_raw, dl_wisdom2eg_raw
from storyteller.elastic.crud import Searcher
from storyteller.preprocess import split_train_val, normalise, augment, upsample, parse


class ArtifactBuilder:

    def __call__(self, *args, **kwargs) -> wandb.Artifact:
        raise NotImplementedError


class WisdomsBuilder(ArtifactBuilder):

    def __call__(self, ver: str) -> wandb.Artifact:
        artifact = wandb.Artifact(name="wisdoms", type="dataset")
        wisdoms_df = dl_wisdoms(ver)
        table = wandb.Table(dataframe=wisdoms_df)
        artifact.add(table, name="wisdoms")  # just wisdoms
        return artifact


class Wisdom2TestBuilder(ArtifactBuilder):

    def __call__(self, ver: str) -> wandb.Artifact:
        artifact = wandb.Artifact(name="wisdom2test", type="dataset")
        wisdom2test_df = dl_wisdom2test(ver)
        table = wandb.Table(dataframe=wisdom2test_df)
        artifact.add(table, name="wisdom2test")  # just wisdoms
        return artifact


class Wisdom2DescBuilder(ArtifactBuilder):

    def __init__(self, train_ratio: float, seed: int):
        self.train_ratio = train_ratio
        self.seed = seed

    def __call__(self, ver: str):
        artifact = self.artifact()
        raw_df = self.raw_df(ver)
        all_df = self.preprocess(raw_df)
        train_df, val_df = split_train_val(raw_df, self.train_ratio, self.seed)
        raw_table = wandb.Table(dataframe=raw_df)
        all_table = wandb.Table(dataframe=all_df)
        train_table, val_table = wandb.Table(dataframe=train_df), wandb.Table(dataframe=val_df)
        # add the tables to the artifact
        artifact.add(raw_table, "raw")
        artifact.add(all_table, "all")
        artifact.add(train_table, "train")
        artifact.add(val_table, "val")
        return artifact

    @staticmethod
    def artifact() -> wandb.Artifact:
        raise NotImplementedError

    @staticmethod
    def raw_df(ver: str) -> pd.DataFrame:
        raise NotImplementedError

    @staticmethod
    def preprocess(raw_df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError


class Wisdom2DefBuilder(Wisdom2DescBuilder):

    @staticmethod
    def artifact() -> wandb.Artifact:
        return wandb.Artifact(name="wisdom2def", type="dataset")

    @staticmethod
    def raw_df(ver: str) -> pd.DataFrame:
        return dl_wisdom2def_raw(ver)

    @staticmethod
    def preprocess(raw_df: pd.DataFrame) -> pd.DataFrame:
        # as for wisdom2def, we don't need parsing.
        return raw_df.pipe(normalise)\
                     .pipe(augment)\
                     .pipe(upsample)


class Wisdom2EgBuilder(Wisdom2DescBuilder):

    @staticmethod
    def artifact() -> wandb.Artifact:
        return wandb.Artifact(name="wisdom2eg", type="dataset")

    @staticmethod
    def raw_df(ver: str) -> pd.DataFrame:
        client = connect_to_es()
        searcher = Searcher(client)
        return dl_wisdom2eg_raw(ver, searcher)

    @staticmethod
    def preprocess(raw_df: pd.DataFrame) -> pd.DataFrame:
        return raw_df.pipe(parse)\
                     .pipe(normalise)\
                     .pipe(augment)\
                     .pipe(upsample)
