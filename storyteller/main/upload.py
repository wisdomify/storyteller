"""
This is for pushing all the tsv files to wandb
"""

import argparse
from storyteller.builders import WisdomsBuilder, Wisdom2TestBuilder, Wisdom2DefBuilder, Wisdom2EgBuilder
from storyteller.connectors import connect_to_wandb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str,
                        default="wisdom2def")
    parser.add_argument("--ver", type=str,
                        default="v1")
    parser.add_argument("--train_ratio", type=float,
                        default=0.9)
    parser.add_argument("--seed", type=int,
                        default=400)

    args = parser.parse_args()
    name: str = args.name
    ver: str = args.ver
    train_ratio: float = args.train_ratio
    seed: int = args.seed

    # --- instantiate an uploader --- #
    run = connect_to_wandb(name="storyteller.main.upload")
    if name == "wisdoms":
        artifact = WisdomsBuilder()(ver)
    # --- instantiate an appropriate uploader --- #
    elif name == "wisdom2test":
        artifact = Wisdom2TestBuilder()(ver)
    elif name == "wisdom2def":
        artifact = Wisdom2DefBuilder(train_ratio, seed)(ver)
    elif name == "wisdom2eg":
        artifact = Wisdom2EgBuilder(train_ratio, seed)(ver)
    else:
        raise ValueError
    # --- upload the given version --- #
    run.log_artifact(artifact)


if __name__ == '__main__':
    main()
