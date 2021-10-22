import itertools
import os
import zipfile
import pandas as pd
from typing import Iterator, Optional
from tqdm import tqdm
from google.cloud.storage import Client, Bucket
from google.cloud.storage import Blob
from sklearn.model_selection import train_test_split


class Supporter:

    def __call__(self, *args, **kwargs):
        """
        whatever the supporter does,
        it supports the main commands written under the storyteller/main package.
        """
        raise NotImplementedError


class Downloader(Supporter):
    """
    supports storyteller/main/dl.py
    """
    def __init__(self,
                 client: Client,
                 bucket: Bucket):
        self.client = client
        self.bucket = bucket

    def __call__(self, path: str, to: str, unzip: bool) -> None:
        if '.' in path.split('/')[-1]:
            blobs = [self.get_item(file_path=path)]
        else:
            blobs = self.get_item_list(sub_path=path, is_blob=True)
        dir_blobs, dl_blobs = itertools.tee(blobs)

        self._create_local_dirs_of(dir_blobs, at=to)
        for blob in dl_blobs:
            if blob.name.split('/')[-1] == '.DS_Store':
                continue
            if '.zip' not in blob.name:
                continue

            self._download(blob, to)

            if unzip:
                self._unzip_file(blob, to)

    def get_item(self, file_path: str) -> Blob:
        return self.bucket.get_blob(file_path)

    def get_item_list(self, sub_path: str, is_blob: bool = False) -> Iterator:
        """
        :param is_blob: if true the item includes blob object
        :param sub_path: directory path in gcloud storage
        :return: iterable that includes file/dir names that starts with sub_path from gcloud storage.
        """
        if sub_path[-1] != '/':
            sub_path += '/'

        return iter(filter(
            lambda path: len(path) != 0 if not is_blob else path,
            map(
                lambda blob: blob.name.replace(sub_path, '') if not is_blob else blob,
                self.bucket.list_blobs(prefix=sub_path)
            )
        ))

    def get_elastic_data_dirs(self) -> Iterator:
        """
        :return: iterator includes folder names in elastic directory in gcloud storage
        """
        return iter(set(
            filter(
                lambda path: len(path) != 0,
                map(
                    lambda path: path.split('/')[0],
                    self.get_item_list('story/elastic')
                )
            )
        ))

    @staticmethod
    def _create_local_dirs_of(blobs: Iterator[Blob], at: str) -> None:
        """
        path create for blobs download
        :param blobs: target blobs
        :param at: local dir for path creation
        :return:
        """
        tmp_blobs = list(blobs)
        at = at + '/' if at[-1] != '/' else at
        dirs = sorted(
            set(
                map(
                    lambda path_list: '/'.join(path_list[:-1]),
                    map(
                        lambda blob: blob.name.split('/'),
                        tmp_blobs
                    )
                )
            ),
            key=lambda pth: len(pth)
        )

        for d in dirs:
            target_dir = os.path.join(at, d)
            try:
                os.makedirs(target_dir, exist_ok=True)
            except OSError:
                raise OSError(f"Creation of the directory failed: {target_dir}")
            else:
                print(f"Successfully created the directory: {target_dir}")

    def _download(self, blob: Blob, to: str):
        try:
            with open(to + blob.name, 'wb') as f:
                with tqdm.wrapattr(f, "write", total=blob.size) as file_obj:
                    self.client.download_blob_to_file(blob, file_obj)

            print(f"\nSuccessful download: {blob.name}")

        except Exception as e:
            raise IOError(f"Fail to download file: {blob}"
                          f"Details: {e}")

    @staticmethod
    def _unzip_file(blob: Blob, to: str):
        target_file = os.path.join(to, blob.name)
        try:
            with zipfile.ZipFile(target_file) as z:
                for info in z.infolist():
                    if '.nt' in info.filename:
                        continue
                    info.filename = info.orig_filename.encode('cp437').decode('euc-kr', 'ignore')
                    if os.sep != "/" and os.sep in info.filename:
                        info.filename = info.filename.replace(os.sep, "/")
                    info.filename = f"{target_file.split('/')[-1].split('.zip')[0]}_{info.filename}"

                    z.extract(info, path='/'.join(target_file.split('/')[:-1]))

                    print(f"\nSuccessful unzip: {info.filename}")

        except Exception as e:
            raise IOError(f"Fail to unzip zipfile: {target_file}\n"
                          f"Details: {e}")

        try:
            os.remove(target_file)

        except Exception as e:
            raise IOError(f"Fail to remove zipfile: {target_file}\n"
                          f"Details: {e}")


class Indexer(Supporter):
    """
    supports storyteller/main/index.py
    """
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


class Searcher(Supporter):
    """
    supports storyteller/main/search.py
    """
    def __call__(self, *args, **kwargs):
        pass


class Splitter(Supporter):

    def __init__(self,
                 train_portion: int, validation_portion: int, test_portion: int,
                 train_test_shuffle: bool, train_val_shuffle: bool,
                 train_test_stratify_col: Optional[str], train_val_stratify_col: Optional[str],
                 seed: int):
        """
        :param train_portion:
        :param validation_portion:
        :param test_portion:
        :param train_test_shuffle:
        :param train_test_stratify_col:
        :param train_val_shuffle:
        :param train_val_stratify_col:
        :param seed:
        """
        self.train_portion = train_portion
        self.validation_portion = validation_portion
        self.test_portion = test_portion
        self.train_test_shuffle = train_test_shuffle
        self.train_val_shuffle = train_val_shuffle
        self.train_val_stratify_col = train_val_stratify_col
        self.train_test_stratify_col = train_test_stratify_col
        self.seed = seed

    def __call__(self, data_path: str, dty: str):
        """
        :param data_path: path to train_{DATA}.tsv, val_{DATA}.tsv, test_{DATA}.tsv
        :return:
        """
        self.split_and_save(data_path)
        self.make_zip_files(data_path, dty)

    def split_and_save(self, data_path: str):
        """
        The data path will be form of
        {data_dir}/{version}/raw/{data_name}.{file_format}
        Then the split data will be stored on {data_dir}/.
        Final output includes .tsv files and .zip files
        :return:
        Final output:
        - train_{DATA}.tsv
        - val_{DATA}.tsv
        - test_{DATA}.tsv
        """
        if 'raw' not in data_path:
            raise ValueError("data path should be {data_dir}/{version}/raw/{data_name}.{file_format}."
                             "\nYou have written:", data_path)

        data_name = ''.join(data_path.split('/')[-1].split('.')[:-1])
        data_dir = '/'.join(data_path.split('/')[:-2])
        file_format = data_path.split('/')[-1].split('.')[-1]
        separator = '\t' if file_format == 'tsv' else ',' if file_format == 'csv' else None

        df = pd.read_csv(data_path, sep=separator)

        total_portion = self.train_portion + self.validation_portion + self.test_portion
        train_val_size = (self.train_portion + self.validation_portion) / total_portion
        test_size = self.test_portion / total_portion

        train_val_portion = self.train_portion + self.validation_portion

        train_size = self.train_portion / train_val_portion
        val_size = self.validation_portion / train_val_portion

        print("====== SPECIFICATION ======")
        print(f"Train + Val: Test = {round(train_val_size * 100, 2)}%: {round(test_size * 100, 2)}%")
        print(f"Train: Validation = {round(train_size * 100, 2)}%: {round(val_size * 100, 2)}%")
        print()

        train_val, test = train_test_split(df,
                                           train_size=train_val_size,
                                           test_size=test_size,
                                           random_state=self.seed,
                                           shuffle=self.train_test_shuffle,
                                           stratify=df[self.train_test_stratify_col]
                                           if self.train_test_stratify_col else self.train_test_stratify_col)

        train, val = train_test_split(train_val,
                                      train_size=train_size,
                                      test_size=val_size,
                                      random_state=self.seed,
                                      shuffle=self.train_val_shuffle,
                                      stratify=df[self.train_val_stratify_col]
                                      if self.train_val_stratify_col else self.train_val_stratify_col)

        train.to_csv(f'{data_dir}/train_{data_name}.tsv', sep='\t', index=False)
        val.to_csv(f'{data_dir}/val_{data_name}.tsv', sep='\t', index=False)
        test.to_csv(f'{data_dir}/test_{data_name}.tsv', sep='\t', index=False)

        print("====== RESULT ======")
        print(f"Total Data Count: {len(df)}")
        print(f"Train Data Count: {len(train)} ({len(train) / len(df) * 100} %)")
        print(f"Val   Data Count: {len(val)} ({len(val) / len(df) * 100} %)")
        print(f"Test  Data Count: {len(test)} ({len(test) / len(df) * 100} %)")

    @staticmethod
    def make_zip_files(data_path: str, dty: str):
        """
        :param data_path: str
        :param dty: definition | example
        :return:
        Final output:
        - {data_path}/{dty}.zip
        """
        dtp = 'def' if dty == 'definition' else 'eg'
        with zipfile.ZipFile(f'{data_path}/{dty}.zip', 'w') as zipf:
            zipf.write(os.path.join(data_path, f'train_wisdom2{dtp}.tsv'), arcname=f'train_wisdom2{dtp}.tsv')
            zipf.write(os.path.join(data_path, f'val_wisdom2{dtp}.tsv'), arcname=f'val_wisdom2{dtp}.tsv')
            zipf.write(os.path.join(data_path, f'test_wisdom2{dtp}.tsv'), arcname=f'test_wisdom2{dtp}.tsv')
