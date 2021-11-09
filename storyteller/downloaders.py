from typing import List
import wandb
from storyteller.connectors import connect_to_wandb


def dl_wisdoms(ver: str) -> List[str]:
    with connect_to_wandb():
        artifact = wandb.use_artifact(f"wisdoms:{ver}")
        table = artifact.get("all")
        return [row[0] for _, row in table.iterrows()]


# .... and we also have others as well..
