from collections.abc import Iterator

from gcloud import storage
from gcloud.storage import Blob


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

    def download_directory(self, path: str, to: str):
        blobs = self.get_item_list(sub_path=path, is_blob=True)
        for blob in blobs:
            filename = blob.name.replace('/', '_')
            try:
                blob.download_to_filename(to + filename)
            except Exception as e:
                raise IOError(f"Fail to download file: {blob}"
                              f"Details: {e}")

    def download_file(self, file: str, to: str):
        blob = self.get_item(file_path=file)

        filename = blob.name.replace('/', '_')
        try:
            blob.download_to_filename(to + filename)  # Download
        except Exception as e:
            raise IOError(f"Fail to download file: {blob}"
                          f"Details: {e}")


if __name__ == '__main__':
    gcp_storage = GCPStorage('wisdomify')
    res = gcp_storage.get_item_list('story/elastic')
    print(res)
    ess = list(gcp_storage.get_elastic_data_dirs())
    print(ess)
    gcp_storage.download_file('story/elastic/일반상식/01_triples_일반상식(N-Triple형식).zip', to='./')
    # for r in res:
    #     print(r)
