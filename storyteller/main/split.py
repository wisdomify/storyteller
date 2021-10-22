import os
from storyteller.paths import DATA_DIR
from storyteller.supporters import Splitter


def main():
    ver_dir = os.path.join(DATA_DIR, 'version_1')
    # --- instantiate a splitter --- #
    splitter = Splitter(train_portion=80, validation_portion=10,
                        test_portion=10, train_test_shuffle=True, train_val_shuffle=True,
                        train_test_stratify_col=None, train_val_stratify_col=None,
                        seed=42)
    # --- split wisdom2def & wisdom2eg --- #
    splitter(os.path.join(ver_dir, 'raw/wisdom2def.tsv'), dty="definition")
    splitter(os.path.join(ver_dir, 'raw/wisdom2eg.tsv'), dty="example")


if __name__ == '__main__':
    main()
