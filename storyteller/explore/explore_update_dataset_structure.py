import pandas as pd

from storyteller.utils.wandb_controller import WandBSupport


def update_dataset_from_wandb():
    datasets = [
        'init_wisdom2def-raw',
        'init_wisdom2eg-raw',
        'init_kuniv_wisdom2eg-raw',
        'wikiquote_wisdom2def-raw',
        'wikiquote_wisdom2eg-raw',
        'namuwiki_wisdom2def-raw',
        'namuwiki_wisdom2eg-raw',
        'opendict_wisdom2def-raw',
        'opendict_wisdom2eg-raw',
        'init_kuniv-preprocess_wisdom_token',
        'init_kuniv-preprocess_no_wisdom',
    ]

    for dataset in datasets:
        # obj init
        wandb_support = WandBSupport(
            specification={
                'job_name': 'update_dataset_split',
                'job_desc': 'this run updates split structure.'
            },
        )

        # download
        dl_spec = wandb_support.download_artifact(name=dataset, dtype='dataset')

        train_df = pd.read_csv(f"{dl_spec['download_dir']}/training.tsv", sep='\t')
        validate_df = pd.read_csv(f"{dl_spec['download_dir']}/validation.tsv", sep='\t')
        test_df = pd.read_csv(f"{dl_spec['download_dir']}/test.tsv", sep='\t')

        # convert
        new_train_df = train_df.append(validate_df)
        new_val_df = test_df

        desc = 'split structure updated dataset'
        artifact = wandb_support.create_artifact(name=dataset, dtype='dataset', desc=desc)

        with artifact.new_file('train.tsv', mode="wb") as file:
            new_train_df.to_csv(file, sep='\t')

        with artifact.new_file('validation.tsv', mode="wb") as file:
            new_val_df.to_csv(file, sep='\t')

        # ✍️ Save the artifact to W&B.
        wandb_support.wandb_obj.log_artifact(artifact)

        wandb_support.push(is_only_push=True)


if __name__ == '__main__':
    update_dataset_from_wandb()
