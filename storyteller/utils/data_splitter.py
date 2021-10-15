import os
import zipfile

import pandas as pd
from sklearn.model_selection import train_test_split

from storyteller.paths import DATA_DIR


def split_and_save(data_path: str,
                   train_portion: int, validation_portion: int, test_portion: int,
                   train_test_shuffle: bool = True, train_test_stratify_col: str = None,
                   train_val_shuffle: bool = True, train_val_stratify_col: str = None,
                   train_test_random_num: int = 42, train_val_random_num: int = 42
                   ):
    """
    The data path will be form of
    {data_dir}/{version}/raw/{data_name}.{file_format}

    Then the split data will be stored on {data_dir}/.
    Final output includes .tsv files and .zip files

    :param data_path: dataset (csv or tsv) path

    The proportion is calculated by
    train_val: test = (train + val) / total: test / total
    train: val = train / (train + val) : test / (train + val)
    :param train_portion: amount for train
    :param validation_portion: amount for val
    :param test_portion: amount for test

    :param train_test_shuffle: does train+val / test split shuffle?
    :param train_test_stratify_col: which column to be stratified for train+val / test split?
    :param train_val_shuffle: does train / val split shuffle?
    :param train_val_stratify_col: which column to be stratified for train / val split?
    :param train_test_random_num: random number for train+val / test split
    :param train_val_random_num: random number for train / val split

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

    total_portion = train_portion + validation_portion + test_portion
    train_val_size = (train_portion + validation_portion) / total_portion
    test_size = test_portion / total_portion

    train_val_portion = train_portion + validation_portion

    train_size = train_portion / train_val_portion
    val_size = validation_portion / train_val_portion

    print("====== SPECIFICATION ======")
    print(f"Train + Val: Test = {round(train_val_size * 100, 2)}%: {round(test_size * 100, 2)}%")
    print(f"Train: Validation = {round(train_size * 100, 2)}%: {round(val_size * 100, 2)}%")
    print()

    train_val, test = train_test_split(df,
                                       train_size=train_val_size,
                                       test_size=test_size,
                                       random_state=train_test_random_num,
                                       shuffle=train_test_shuffle,
                                       stratify=df[train_test_stratify_col]
                                       if train_test_stratify_col else train_test_stratify_col)

    train, val = train_test_split(train_val,
                                  train_size=train_size,
                                  test_size=val_size,
                                  random_state=train_val_random_num,
                                  shuffle=train_val_shuffle,
                                  stratify=df[train_val_stratify_col]
                                  if train_val_stratify_col else train_val_stratify_col)

    train.to_csv(f'{data_dir}/train_{data_name}.tsv', sep='\t', index=False)
    val.to_csv(f'{data_dir}/val_{data_name}.tsv', sep='\t', index=False)
    test.to_csv(f'{data_dir}/test_{data_name}.tsv', sep='\t', index=False)

    print("====== RESULT ======")
    print(f"Total Data Count: {len(df)}")
    print(f"Train Data Count: {len(train)} ({len(train) / len(df) * 100} %)")
    print(f"Val   Data Count: {len(val)} ({len(val) / len(df) * 100} %)")
    print(f"Test  Data Count: {len(test)} ({len(test) / len(df) * 100} %)")


def make_zip_files(data_path, dty):
    """
    :param data_path: path to train_{DATA}.tsv, val_{DATA}.tsv, test_{DATA}.tsv
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


if __name__ == '__main__':
    ver_dir = os.path.join(DATA_DIR, 'version_1/')

    split_and_save(os.path.join(ver_dir, 'raw/wisdom2def.tsv'), 80, 10, 10)
    make_zip_files(ver_dir, 'definition')
    print()

    split_and_save(os.path.join(ver_dir, 'raw/wisdom2eg.tsv'), 80, 10, 10)
    make_zip_files(ver_dir, 'example')
