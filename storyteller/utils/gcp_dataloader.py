import itertools
import os
import shutil
import zipfile

from typing import Iterator, List

from tqdm import tqdm
from google.cloud import storage
from google.cloud.storage import Blob

from copy import copy

from storyteller.paths import BS_DIR, CVC_DIR, DS_DIR


class GCPStorage:
    def __init__(self,
                 bucket_name: str):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(self.bucket_name)

    def get_item(self, file_path: str) -> Blob:
        return self.bucket.get_blob(file_path)

    def get_item_list(self, sub_path: str, is_blob: bool = False) -> Iterator:
        """
        :param is_blob: if true the item includes blob object
        :param sub_path: directory path in gcloud storage
        :return: iterable that includes file/dir names that starts with sub_path from gcloud storage.
        """
        if sub_path[-1] != '/':
            sub_path += '/'

        return iter(filter(
            lambda path: len(path) != 0 if not is_blob else path,
            map(
                lambda blob: blob.name.replace(sub_path, '') if not is_blob else blob,
                self.bucket.list_blobs(prefix=sub_path)
            )
        ))

    def get_elastic_data_dirs(self) -> Iterator:
        """
        :return: iterator includes folder names in elastic directory in gcloud storage
        """
        return iter(set(
            filter(
                lambda path: len(path) != 0,
                map(
                    lambda path: path.split('/')[0],
                    self.get_item_list('story/elastic')
                )
            )
        ))

    @staticmethod
    def _create_local_dirs_of(blobs: Iterator[Blob], at: str) -> None:
        """
        path create for blobs download
        :param blobs: target blobs
        :param at: local dir for path creation
        :return:
        """
        tmp_blobs = list(blobs)
        at = at + '/' if at[-1] != '/' else at
        dirs = sorted(
            set(
                map(
                    lambda path_list: '/'.join(path_list[:-1]),
                    map(
                        lambda blob: blob.name.split('/'),
                        tmp_blobs
                    )
                )
            ),
            key=lambda pth: len(pth)
        )

        for d in dirs:
            target_dir = os.path.join(at, d)
            try:
                os.makedirs(target_dir, exist_ok=True)
            except OSError:
                raise OSError(f"Creation of the directory failed: {target_dir}")
            else:
                print(f"Successfully created the directory: {target_dir}")

    def _download(self, blob: Blob, to: str):
        to = to + '/' if to[-1] != '/' else to
        try:
            with open(to + blob.name, 'wb') as f:
                with tqdm.wrapattr(f, "write", total=blob.size) as file_obj:
                    self.client.download_blob_to_file(blob, file_obj)

            print(f"\nSuccessful download: {blob.name}")

        except Exception as e:
            raise IOError(f"Fail to download file: {blob}\n"
                          f"Details: {e}")

    @staticmethod
    def _unzip_file(blob: Blob, to: str):
        target_file = os.path.join(os.getcwd(), to, blob.name)
        try:
            with zipfile.ZipFile(target_file) as z:
                for info in z.infolist():
                    if '.nt' in info.filename:
                        continue

                    info.filename = info.orig_filename.encode('cp437').decode('euc-kr', 'ignore')
                    if os.sep != "/" and os.sep in info.filename:
                        info.filename = info.filename.replace(os.sep, "/")
                    info.filename = f"{target_file.split('/')[-1].split('.zip')[0]}_{info.filename}"

                    z.extract(info, path='/'.join(target_file.split('/')[:-1]))

                    print(f"\nSuccessful unzip: {info.filename}")

        except Exception as e:
            raise IOError(f"Fail to unzip zipfile: {target_file}\n"
                          f"Details: {e}")

        try:
            os.remove(target_file)

        except Exception as e:
            raise IOError(f"Fail to remove zipfile: {target_file}\n"
                          f"Details: {e}")

    def download(self, path: str, to: str, unzip: bool) -> None:
        if '.' in path.split('/')[-1]:
            blobs = [self.get_item(file_path=path)]
        else:
            blobs = self.get_item_list(sub_path=path, is_blob=True)
        dir_blobs, dl_blobs = itertools.tee(blobs)

        self._create_local_dirs_of(dir_blobs, at=to)
        for blob in dl_blobs:
            if blob.name.split('/')[-1] == '.DS_Store':
                continue
            if '.zip' not in blob.name:
                continue

            self._download(blob, to)

            if unzip:
                self._unzip_file(blob, to)


if __name__ == '__main__':
    gcp_storage = GCPStorage('wisdomify')
    gcp_storage.download('story/elastic/문서요약 텍스트', DS_DIR, unzip=True)

