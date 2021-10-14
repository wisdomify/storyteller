import os
import shutil

import wandb as wandb


class WandBSupport:
    def __init__(self,
                 ver: str,
                 run_type: str,
                 entity: str = 'wisdomify',
                 project: str = 'wisdomify'):
        self.conf_json = load_conf()['versions'][ver]
        self.config = self.conf_json['wandb']

        self.job_name = f"{run_type}_{self.conf_json['exp_name']}"
        self.job_desc = self.conf_json['exp_desc']

        # initialise wandb connection object.
        self.wandb_obj = wandb.init(
            entity=entity,
            project=project,
            name=self.job_name,
            notes=self.job_desc
        )
        self.logger = None

        self.models = WandBModels(self)
        self.tmp_files = ['./wandb', './artifacts']

    def _get_artifact(self,
                      name: str,
                      dtype: str,
                      ver: str = 'latest'):
        # this function returns existing artifact object.
        ver = ver if len(ver) > 1 else 'latest'

        return self.wandb_obj.use_artifact(f"{name}:{ver}", type=dtype)

    def download_artifact(self,
                          name: str,
                          dtype: str,
                          ver: str = 'latest'):
        # this function returns download path and downloaded files
        """
        :return:
        {
            'downloaded_dir': downloaded directory
            'downloaded_files': file names downloaded
        }
        """
        dl_dir = self._get_artifact(name=name, ver=ver, dtype=dtype).download()
        return {
            'download_dir': dl_dir,
            'download_files': list(filter(lambda s: s != '.DS_Store', os.listdir(dl_dir)))
        }

    @staticmethod
    def create_artifact(name: str,
                        dtype: str,
                        desc: str,
                        meta: str = None):
        # this function creates and returns new artifact
        return wandb.Artifact(name, type=dtype, description=desc, metadata=meta)

    def write_artifact(self,
                       artifact: wandb.Artifact,
                       file_name: str,
                       scripts):
        # This function was intended to make user to write file on the desired artifact.
        # However, file saving script may be different depending on the data type.
        """
        >>> with artifact.new_file(file_name, mode="wb") as file:
        >>>     Write_data_saving_script
        """
        raise NotImplementedError

    @staticmethod
    def add_artifact(artifact: wandb.Artifact,
                     file_path: str):
        # This function is used when user trying to add already saved file directly with file path
        return artifact.add_file(file_path)

    def push(self) -> None:
        self.wandb_obj.finish()
        wandb.finish()

        for file in self.tmp_files:
            shutil.rmtree(file)
