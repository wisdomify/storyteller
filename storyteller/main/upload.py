"""
This is for pushing all the tsv files to wandb
"""

import argparse
from storyteller.builders import WisdomsBuilder, Wisdom2QueryBuilder, Wisdom2DefBuilder, Wisdom2EgBuilder
from storyteller.connectors import connect_to_wandb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str,
                        default="wisdom2def")
    parser.add_argument("--ver", type=str,
                        default="v1")
    parser.add_argument("--val_ratio", type=float,
                        default=0.2)
    parser.add_argument("--seed", type=int,
                        default=410)

    args = parser.parse_args()
    name: str = args.name
    ver: str = args.ver
    val_ratio: float = args.val_ratio
    seed: int = args.seed

    # --- instantiate an uploader --- #
    run = connect_to_wandb(name="storyteller.main.upload")
    if name == "wisdoms":
        builder = WisdomsBuilder(ver)
    # --- instantiate an appropriate uploader --- #
    elif name == "wisdom2query":
        builder = Wisdom2QueryBuilder(ver, val_ratio, seed)
    elif name == "wisdom2def":
        builder = Wisdom2DefBuilder(ver)
    elif name == "wisdom2eg":
        builder = Wisdom2EgBuilder(ver)
    else:
        raise ValueError
    # --- upload the given version --- #
    artifact = builder()
    run.log_artifact(artifact)


if __name__ == '__main__':
    main()
