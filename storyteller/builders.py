import wandb
import pandas as pd
from storyteller.connectors import connect_to_es
from storyteller.downloaders import dl_wisdoms, dl_wisdom2query_raw, dl_wisdom2def_raw, dl_wisdom2eg_raw
from storyteller.elastic.crud import Searcher
from storyteller.preprocess import stratified_split, normalise, augment, upsample, parse, cleanse


class ArtifactBuilder:

    def __init__(self, ver: str):
        self.ver = ver

    def __call__(self, *args, **kwargs) -> wandb.Artifact:
        raise NotImplementedError


class WisdomsBuilder(ArtifactBuilder):

    def __call__(self) -> wandb.Artifact:
        artifact = wandb.Artifact(name="wisdoms", type="dataset")
        wisdoms_df = dl_wisdoms(self.ver)
        table = wandb.Table(dataframe=wisdoms_df)
        artifact.add(table, name="wisdoms")  # just wisdoms
        return artifact


class Wisdom2DescBuilder(ArtifactBuilder):

    def __call__(self):
        artifact = self.artifact()
        raw_df = self.raw_df(self.ver)
        all_df = self.preprocess(raw_df)
        raw_table = wandb.Table(dataframe=raw_df)
        all_table = wandb.Table(dataframe=all_df)
        # add the tables to the artifact
        artifact.add(raw_table, "raw")
        artifact.add(all_table, "all")
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


class Wisdom2QueryBuilder(Wisdom2DescBuilder):

    def __init__(self, ver: str, val_ratio: float, seed: int):
        super().__init__(ver)
        self.val_ratio = val_ratio
        self.seed = seed

    def __call__(self) -> wandb.Artifact:
        artifact = self.artifact()
        artifact.metadata = self.__dict__
        raw_df = self.raw_df(self.ver)
        all_df = self.preprocess(raw_df)
        val_df, test_df = stratified_split(raw_df, self.val_ratio, self.seed)
        raw_table = wandb.Table(dataframe=raw_df)
        all_table = wandb.Table(dataframe=all_df)
        val_table = wandb.Table(dataframe=val_df)
        test_table = wandb.Table(dataframe=test_df)
        # add the tables to the artifact
        artifact.add(raw_table, "raw")
        artifact.add(all_table, "all")
        artifact.add(val_table, "val")
        artifact.add(test_table, "test")
        return artifact

    @staticmethod
    def artifact() -> wandb.Artifact:
        return wandb.Artifact(name="wisdom2query", type="dataset")

    @staticmethod
    def raw_df(ver: str) -> pd.DataFrame:
        return dl_wisdom2query_raw(ver)

    @staticmethod
    def preprocess(raw_df: pd.DataFrame) -> pd.DataFrame:
        return raw_df\
            .pipe(cleanse)\
            .pipe(normalise)


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
        return raw_df\
            .pipe(cleanse)\
            .pipe(normalise)\
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
        return raw_df\
            .pipe(parse)\
            .pipe(cleanse)\
            .pipe(normalise)\
            .pipe(augment)\
            .pipe(upsample)
