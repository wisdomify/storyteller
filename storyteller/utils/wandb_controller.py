import collections
import os
import shutil
from collections import namedtuple

import wandb as wandb


class WandBSupport:
    @staticmethod
    def _check_field(spec: dict,
                     field: str,
                     field_type: type) -> None:
        """
        This function checks field existence and its type from specification written in form of dictionary.
        :param spec:
        :param field:
        :param field_type:
        :return: None
        """
        if field not in spec.keys():
            raise KeyError(f"Missing Key: specification parameter must have '{field}'.")

        if type(spec[field]) is not str:
            raise TypeError(f"Wrong Type for Key: type for '{field}' is {type(spec['job_name'])}. "
                            f"This must be {field_type}.")

    def _check_spec(self, spec: dict) -> namedtuple:
        # This function checks specification for wandb run object.
        self._check_field(spec, 'job_name', str)
        self._check_field(spec, 'job_desc', str)

        return namedtuple('GenericDict', spec.keys())(**spec)

    def __init__(self,
                 specification: dict,
                 entity: str = 'wisdomify',
                 project: str = 'wisdomify'):
        # initialise wandb connection object.
        self.specification = self._check_spec(specification)

        self.wandb_obj = wandb.init(
            entity=entity,
            project=project,
            name=self.specification.job_name,
            notes=self.specification.job_desc
        )
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
                        meta: dict = None):
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

    def push(self, is_only_push: bool = False) -> None:
        self.wandb_obj.finish()
        wandb.finish()

        if not is_only_push:
            for file in self.tmp_files:
                if os.path.exists(file):
                    shutil.rmtree(file)
