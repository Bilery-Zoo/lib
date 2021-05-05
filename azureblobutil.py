#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
author    : Bilery Zoo(bilery.zoo@gmail.com)
create_ts : 2020-01-01
program   : *_* Microsoft Azure Blob service utility *_*
"""


import sys
from azure.storage.blob import BlobServiceClient


reload(sys)
sys.setdefaultencoding("UTF-8")


class AzureBlob(object):
    def __init__(self, account_url, credential, **kwargs):
        """
        See also:
            https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobserviceclient?view=azure-python
        """
        self._account_url = account_url
        self._credential = credential
        self._kwargs = kwargs

    def get_service_client(self):
        return BlobServiceClient(account_url=self._account_url, credential=self._credential, **self._kwargs)

    @staticmethod
    def get_container_client(_service_client, container):
        return _service_client.get_container_client(container)

    @staticmethod
    def get_blob_client(_service_client, container, blob, **kwargs):
        return _service_client.get_blob_client(container, blob, **kwargs)

    @staticmethod
    def easy_upload_blob(_blob_client, blob, **kwargs):
        with open(blob, "rb") as f:
            _blob_client.upload_blob(f, **kwargs)

    @staticmethod
    def easy_download_blob(_blob_client, blob, **kwargs):
        with open(blob, "wb") as f:
            f.write(_blob_client.download_blob(**kwargs).readall())

    @staticmethod
    def easy_delete_blob(_container_client, blob, **kwargs):
        _container_client.delete_blob(blob, **kwargs)

    @staticmethod
    def pseudo_move_blob(_container_client, _blob_upload_client, blob_local, blob_container,
                         is_need_download=False, _blob_download_client=None, **kwargs):
        if is_need_download:
            assert _blob_download_client
            AzureBlob.easy_download_blob(_blob_download_client, blob_local)
        try:
            AzureBlob.easy_upload_blob(_blob_upload_client, blob_local, **kwargs)
        except BaseException as E:
            raise E
        else:
            AzureBlob.easy_delete_blob(_container_client, blob_container)


if __name__ == "__main__":
    blob_service_client = AzureBlob(account_url="https://******windows.net/", credential="8FYQTOCi******x0lw==").get_service_client()
    container_client = AzureBlob.get_container_client(_service_client=blob_service_client, container="kpi")
    blob_client = AzureBlob.get_blob_client(_service_client=blob_service_client, container="kpi", blob="upload/test.txt")

    for _ in container_client.list_blobs(name_starts_with="upload/"):
        print(_["name"])

    AzureBlob.easy_upload_blob(blob_client, "/home/zoo/upload.txt", overwrite=True)
    AzureBlob.easy_download_blob(blob_client, "/home/zoo/download.txt")
    AzureBlob.easy_delete_blob(container_client, "upload/delete.txt")
