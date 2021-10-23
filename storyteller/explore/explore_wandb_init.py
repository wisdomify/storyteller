from storyteller.connectors import connect_wandb


def main():
    # What does an init do?
    # This starts a new run to track an ml pipeline
    run = connect_wandb(name="explore_wandb_init", notes="just exploring wandb.init()")


if __name__ == '__main__':
    main()
