from storyteller.connectors import connect_to_wandb


def main():
    run = connect_to_wandb(name="explore_wandb_use_artifact", notes="just exploring run.use_artifact()")
    # this pushes
    artifact = run.use_artifact(artifact_or_name="wisdomify_test:latest")
    # what does an artifact contains? - it houses the metadata of the artifact.
    print(artifact)
    print(artifact.description)
    print(artifact.name)
    print(artifact.version)


if __name__ == '__main__':
    main()
