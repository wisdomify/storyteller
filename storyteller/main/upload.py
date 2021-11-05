"""
This is for pushing all the tsv files to wandb
"""

import argparse
from storyteller.connectors import connect_to_wandb
from storyteller.uploaders import WisdomsUploader, Wisdom2TestUploader, Wisdom2DescUploader, Wisdom2DefUploader, \
    Wisdom2EgUploader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=str,
                        default="wisdom2def")
    parser.add_argument("--ver", type=str,
                        default="v0")
    parser.add_argument("--train_ratio", type=float,
                        default=0.9)
    parser.add_argument("--seed", type=int,
                        default=400)

    args = parser.parse_args()
    artifact: str = args.artifact
    ver: str = args.ver
    train_ratio: float = args.train_ratio
    seed: int = args.seed

    # --- instantiate an uploader --- #
    run = connect_to_wandb(name="storyteller.main.upload")
    if artifact == "wisdoms":
        uploader = WisdomsUploader(run)
    # --- instantiate an appropriate uploader --- #
    elif artifact == "wisdom2test":
        uploader = Wisdom2TestUploader(run)
    elif artifact == "wisdom2def":
        uploader = Wisdom2DefUploader(run, train_ratio, seed)
    elif artifact == "wisdom2eg":
        uploader = Wisdom2EgUploader(run, train_ratio, seed)
    else:
        raise ValueError
    # --- upload the given version --- #
    uploader(ver)


if __name__ == '__main__':
    main()
