from storyteller.connectors import connect_wandb


def main():
    run = connect_wandb(name="explore_wandb_use_artifact", notes="just exploring run.use_artifact()")
    artifact = run.use_artifact(artifact_or_name="test_query:v2")
    # what does an artifact contains? - it houses the metadata of the artifact.
    print(artifact)
    print(artifact.description)
    print(artifact.name)
    print(artifact.version)


if __name__ == '__main__':
    main()
