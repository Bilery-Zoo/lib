#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
author    : Bilery Zoo(bilery.zoo@gmail.com)
create_ts : 2020-04-10
program   : *_* Microsoft Azure Blob service utility *_*
"""


from azure.storage.blob import BlobServiceClient


class AzureBlob(object):
    def __init__(self, account_url, credential, **kwargs):
        """
        See also:
            https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobserviceclient?view=azure-python
        """
        self.account_url = account_url
        self.credential = credential
        self.kwargs = kwargs

        self.blob_service_client = BlobServiceClient(account_url=self.account_url, credential=self.credential,
                                                     **self.kwargs)

    def blob_client(self, blob_service_client=None, *args, **kwargs):
        blob_service_client = blob_service_client if blob_service_client else self.blob_service_client
        return blob_service_client.get_blob_client(*args, **kwargs)

    def easy_upload_blob(self, upload_local_blob, blob_client, **kwargs):
        with open(upload_local_blob, "rb") as f:
            blob_client.upload_blob(f, **kwargs)


if __name__ == "__main__":
    AzureBlobClient = AzureBlob(account_url="https://.windows.net/",
                                credential="8FYQTOCiw89CO+OAx0lw==")
    AzureBlobClient.easy_upload_blob("jb.xlsx",
                                     AzureBlobClient.blob_client(container="kpi", blob="jb.xlsx"),
                                     overwrite=True)
