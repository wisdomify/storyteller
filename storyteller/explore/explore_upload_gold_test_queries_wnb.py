from storyteller.supporters.wandb_controller import WandBSupport


def upload_gold_test_queries():
    wandb_support = WandBSupport(
        specification={
            'job_name': 'upload_ultimate_test_query',
            'job_desc': 'this run uploads ultimate golden test queries'
        },
    )

    name = 'test_query'
    desc = 'This dataset is golden ultimate test queries.'

    artifact = wandb_support.create_artifact(name=name, dtype='dataset', desc=desc)
    wandb_support.add_artifact(artifact, '../../data/gold_test_queries.tsv')

    # ✍️ Save the artifact to W&B.
    wandb_support.wandb_obj.log_artifact(artifact)

    wandb_support.push(is_only_push=True)


if __name__ == '__main__':
    # load_and_log()
    upload_gold_test_queries()
