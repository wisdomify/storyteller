"""
This is a script for building the datasets.
This includes -
"""
import argparse
from storyteller.builders import WisdomifyTestBuilder, Wisdom2DefBuilder, Wisdom2EgBuilder, WisdomsBuilder
from storyteller.connectors import connect_to_es


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact_name", type=str,
                        default="wisdoms")
    parser.add_argument("--seed", type=int,
                        default=38)
    parser.add_argument("--train_ratio", type=float,
                        default=0.9)
    # --- parse the arguments --- #
    args = parser.parse_args()
    artifact_name: str = args.artifact_name
    seed: int = args.seed
    train_ratio: float = args.train_ratio
    # --- instantiate a builder to use --- #
    if artifact_name == "wisdomify_test":
        builder = WisdomifyTestBuilder()
    elif artifact_name == "wisdoms":
        builder = WisdomsBuilder()
    elif artifact_name == "wisdom2def":
        builder = Wisdom2DefBuilder(train_ratio, seed)
    elif artifact_name == "wisdom2eg":
        client = connect_to_es()
        builder = Wisdom2EgBuilder(client, train_ratio, seed)
    else:
        raise ValueError(f"Invalid artifact_name: {artifact_name}")
    # execute the building process
    builder()


if __name__ == '__main__':
    main()


# import os
# import zipfile
# import pandas as pd
# from typing import Optional
# from sklearn.model_selection import train_test_split
# from storyteller.paths import DATA_DIR
#
#
# class Splitter:
#
#     def __init__(self,
#                  train_portion: int, validation_portion: int, test_portion: int,
#                  train_test_shuffle: bool, train_val_shuffle: bool,
#                  train_test_stratify_col: Optional[str], train_val_stratify_col: Optional[str],
#                  seed: int):
#         """
#         :param train_portion:
#         :param validation_portion:
#         :param test_portion:
#         :param train_test_shuffle:
#         :param train_test_stratify_col:
#         :param train_val_shuffle:
#         :param train_val_stratify_col:
#         :param seed:
#         """
#         self.train_portion = train_portion
#         self.validation_portion = validation_portion
#         self.test_portion = test_portion
#         self.train_test_shuffle = train_test_shuffle
#         self.train_val_shuffle = train_val_shuffle
#         self.train_val_stratify_col = train_val_stratify_col
#         self.train_test_stratify_col = train_test_stratify_col
#         self.seed = seed
#
#     def __call__(self, data_path: str, dty: str):
#         """
#         :param data_path: path to train_{DATA}.tsv, val_{DATA}.tsv, test_{DATA}.tsv
#         :return:
#         """
#         self.split_and_save(data_path)
#         self.make_zip_files(data_path, dty)
#
#     def split_and_save(self, data_path: str):
#         """
#         The data path will be form of
#         {data_dir}/{version}/raw/{data_name}.{file_format}
#         Then the split data will be stored on {data_dir}/.
#         Final output includes .tsv files and .zip files
#         :return:
#         Final output:
#         - train_{DATA}.tsv
#         - val_{DATA}.tsv
#         - test_{DATA}.tsv
#         """
#         if 'raw' not in data_path:
#             raise ValueError("data path should be {data_dir}/{version}/raw/{data_name}.{file_format}."
#                              "\nYou have written:", data_path)
#
#         data_name = ''.join(data_path.split('/')[-1].split('.')[:-1])
#         data_dir = '/'.join(data_path.split('/')[:-2])
#         file_format = data_path.split('/')[-1].split('.')[-1]
#         separator = '\t' if file_format == 'tsv' else ',' if file_format == 'csv' else None
#
#         df = pd.read_csv(data_path, sep=separator)
#
#         total_portion = self.train_portion + self.validation_portion + self.test_portion
#         train_val_size = (self.train_portion + self.validation_portion) / total_portion
#         test_size = self.test_portion / total_portion
#
#         train_val_portion = self.train_portion + self.validation_portion
#
#         train_size = self.train_portion / train_val_portion
#         val_size = self.validation_portion / train_val_portion
#
#         print("====== SPECIFICATION ======")
#         print(f"Train + Val: Test = {round(train_val_size * 100, 2)}%: {round(test_size * 100, 2)}%")
#         print(f"Train: Validation = {round(train_size * 100, 2)}%: {round(val_size * 100, 2)}%")
#         print()
#
#         train_val, test = train_test_split(df,
#                                            train_size=train_val_size,
#                                            test_size=test_size,
#                                            random_state=self.seed,
#                                            shuffle=self.train_test_shuffle,
#                                            stratify=df[self.train_test_stratify_col]
#                                            if self.train_test_stratify_col else self.train_test_stratify_col)
#
#         train, val = train_test_split(train_val,
#                                       train_size=train_size,
#                                       test_size=val_size,
#                                       random_state=self.seed,
#                                       shuffle=self.train_val_shuffle,
#                                       stratify=df[self.train_val_stratify_col]
#                                       if self.train_val_stratify_col else self.train_val_stratify_col)
#
#         train.to_csv(f'{data_dir}/train_{data_name}.tsv', sep='\t', index=False)
#         val.to_csv(f'{data_dir}/val_{data_name}.tsv', sep='\t', index=False)
#         test.to_csv(f'{data_dir}/test_{data_name}.tsv', sep='\t', index=False)
#
#         print("====== RESULT ======")
#         print(f"Total Data Count: {len(df)}")
#         print(f"Train Data Count: {len(train)} ({len(train) / len(df) * 100} %)")
#         print(f"Val   Data Count: {len(val)} ({len(val) / len(df) * 100} %)")
#         print(f"Test  Data Count: {len(test)} ({len(test) / len(df) * 100} %)")
#
#     @staticmethod
#     def make_zip_files(data_path: str, dty: str):
#         """
#         :param data_path: str
#         :param dty: definition | example
#         :return:
#         Final output:
#         - {data_path}/{dty}.zip
#         """
#         dtp = 'def' if dty == 'definition' else 'eg'
#         with zipfile.ZipFile(f'{data_path}/{dty}.zip', 'w') as zipf:
#             zipf.write(os.path.join(data_path, f'train_wisdom2{dtp}.tsv'), arcname=f'train_wisdom2{dtp}.tsv')
#             zipf.write(os.path.join(data_path, f'val_wisdom2{dtp}.tsv'), arcname=f'val_wisdom2{dtp}.tsv')
#             zipf.write(os.path.join(data_path, f'test_wisdom2{dtp}.tsv'), arcname=f'test_wisdom2{dtp}.tsv')
#
#
# def main():
#     # TODO: Not sure how the directory structure should work.
#     ver_dir = os.path.join(DATA_DIR, 'version_1')
#     # --- instantiate a splitter --- #
#     splitter = Splitter(train_portion=80, validation_portion=10,
#                         test_portion=10, train_test_shuffle=True, train_val_shuffle=True,
#                         train_test_stratify_col=None, train_val_stratify_col=None,
#                         seed=42)
#     # --- split wisdom2def & wisdom2eg --- #
#     splitter(os.path.join(ver_dir, 'raw/wisdom2def.tsv'), dty="definition")
#     splitter(os.path.join(ver_dir, 'raw/wisdom2eg.tsv'), dty="example")
#
#
# if __name__ == '__main__':
#     main()
