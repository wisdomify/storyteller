from storyteller.downloaders import dl_wisdom2query_raw
from storyteller.preprocess import stratified_split


def main():
    raw_df = dl_wisdom2query_raw("v0")
    val_df, test_df = stratified_split(raw_df, ratio=0.2, seed=410)
    # each class should have the same size
    print(val_df.groupby(by='wisdom').count())
    print(test_df.groupby(by='wisdom').count())


if __name__ == '__main__':
    main()
