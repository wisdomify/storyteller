import abc
import io
import json
import requests
import wandb
import pandas as pd
from tqdm import tqdm
from storyteller.connectors import connect_to_es
from storyteller.elastic.crud import Searcher
from storyteller.elastic.docs import Story
from storyteller.preprocess import stratified_split, cleanse, normalise, augment, upsample, parse
from storyteller.urls import WISDOMS_V0, WISDOMS_V1, WISDOM2TEST_V0, WISDOM2DEF_RAW_V0, WISDOM2DEF_RAW_V1


# --- builders --- #
class ArtifactBuilder:

    def __init__(self, ver: str):
        self.ver = ver

    def __call__(self, *args, **kwargs) -> wandb.Artifact:
        raise NotImplementedError

    @staticmethod
    def get(url: str) -> str:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text

    def dl_raw_df(self) -> pd.DataFrame:
        raise NotImplementedError


class WisdomsBuilder(ArtifactBuilder):

    def __call__(self) -> wandb.Artifact:
        # now, how do you build them?
        artifact = wandb.Artifact(name="wisdoms", type="dataset")
        wisdoms_df = self.dl_raw_df()
        table = wandb.Table(dataframe=wisdoms_df)
        artifact.add(table, name="wisdoms")  # just wisdoms
        return artifact

    def dl_raw_df(self) -> pd.DataFrame:
        if self.ver == "v0":
            text = self.get(WISDOMS_V0)
        elif self.ver == "v1":
            text = self.get(WISDOMS_V1)
        else:
            raise ValueError
        return pd.read_csv(io.StringIO(text), delimiter="\t")


class Wisdom2DescBuilder(ArtifactBuilder, abc.ABC):

    def __call__(self) -> wandb.Artifact:
        artifact = self.artifact()
        raw_df = self.dl_raw_df()
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
        raw_df = self.dl_raw_df()
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

    def dl_raw_df(self) -> pd.DataFrame:
        if self.ver == "v0":
            text = self.get(WISDOM2TEST_V0)
        else:
            raise ValueError
        return pd.read_csv(io.StringIO(text), delimiter="\t")

    @staticmethod
    def artifact() -> wandb.Artifact:
        return wandb.Artifact(name="wisdom2query", type="dataset")

    @staticmethod
    def preprocess(raw_df: pd.DataFrame) -> pd.DataFrame:
        return raw_df\
            .pipe(cleanse)\
            .pipe(normalise)


class Wisdom2DefBuilder(Wisdom2DescBuilder):

    def dl_raw_df(self) -> pd.DataFrame:
        if self.ver == "v0":
            text = self.get(WISDOM2DEF_RAW_V0)
        elif self.ver == "v1":
            text = self.get(WISDOM2DEF_RAW_V1)
        else:
            raise ValueError
        return pd.read_csv(io.StringIO(text), delimiter="\t")

    @staticmethod
    def artifact() -> wandb.Artifact:
        return wandb.Artifact(name="wisdom2def", type="dataset")

    @staticmethod
    def preprocess(raw_df: pd.DataFrame) -> pd.DataFrame:
        # as for wisdom2def, we don't need parsing.
        return raw_df\
            .pipe(cleanse)\
            .pipe(normalise)\
            .pipe(augment)\
            .pipe(upsample)


class Wisdom2EgBuilder(Wisdom2DescBuilder):

    def dl_raw_df(self) -> pd.DataFrame:
        client = connect_to_es()
        searcher = Searcher(client)
        wisdoms_df = WisdomsBuilder(self.ver).dl_raw_df()
        total = len(wisdoms_df)
        rows = list()
        for _, row in tqdm(wisdoms_df.iterrows(), desc="searching for wisdoms on stories...", total=total):
            wisdom = row['wisdom']
            raw = searcher(wisdom, ",".join(Story.all_indices()), size=10000)
            # https://stackoverflow.com/a/18337754
            raw = json.dumps(raw, ensure_ascii=False)
            rows.append((wisdom, raw))
        return pd.DataFrame(data=rows, columns=["wisdom", "eg"])

    @staticmethod
    def artifact() -> wandb.Artifact:
        return wandb.Artifact(name="wisdom2eg", type="dataset")

    @staticmethod
    def preprocess(raw_df: pd.DataFrame) -> pd.DataFrame:
        return raw_df\
            .pipe(parse)\
            .pipe(cleanse)\
            .pipe(normalise)\
            .pipe(augment)\
            .pipe(upsample)
