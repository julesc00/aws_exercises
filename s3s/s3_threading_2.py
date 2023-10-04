"""
This is module which contains all classes related to aws S3

Approach by Soumil Nitin Shah at https://www.youtube.com/watch?v=KW2PNC0GouY
"""
"""
    awshelper.py
    -------

    This module contains the AWS class

"""

try:
    import re
    import os
    import json
    import boto3
    import datetime
    import uuid
    import math
    from boto3.s3.transfer import TransferConfig
    import threading
    import sys

    from tqdm import tqdm
except Exception as e:
    print("Error : {} ".format(e))

DATA = {
    "AWS_ACCESS_KEY": "XXXXXXXXXXXX",
    "AWS_SECRET_KEY": "XXXXXXXXXXXXX",
    "AWS_REGION_NAME": "us-east-1",
    "BUCKET": "XXXXXXXXXXXXXXXXXXXX",
}

for key, value in DATA.items():
    os.environ[key] = str(value)


class Size:
    @staticmethod
    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])


class ProgressPercentage(object):
    def __init__(self, filename, filesize):
        self._filename = filename
        self._size = filesize
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        def convertSize(size):
            if size == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size, 1024)))
            p = math.pow(1024, i)
            s = round(size / p, 2)
            return "%.2f %s" % (s, size_name[i])

        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)        "
                % (
                    self._filename,
                    convertSize(self._seen_so_far),
                    convertSize(self._size),
                    percentage,
                )
            )
            sys.stdout.flush()


class ProgressPercentageUpload(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)"
                % (self._filename, self._seen_so_far, self._size, percentage)
            )
            sys.stdout.flush()


class AWSS3(object):

    """Helper class to which add functionality on top of boto3"""

    def __init__(self, bucket, aws_access_key_id, aws_secret_access_key, region_name):
        self.BucketName = bucket
        self.client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def get_length(self, Key):
        response = self.client.head_object(Bucket=self.BucketName, Key=Key)
        size = response["ContentLength"]
        return {"bytes": size, "size": Size.convert_size(size)}

    def put_files(self, Response=None, Key=None):
        """
        Put the File on S3
        :return: Bool
        """
        try:
            response = self.client.put_object(
                ACL="private", Body=Response, Bucket=self.BucketName, Key=Key
            )
            return "ok"
        except Exception as e:
            print("Error : {} ".format(e))
            return "error"

    def item_exists(self, Key):
        """Given key check if the items exists on AWS S3"""
        try:
            response_new = self.client.get_object(Bucket=self.BucketName, Key=str(Key))
            return True
        except Exception as e:
            return False

    def get_item(self, Key):
        """Gets the Bytes Data from AWS S3"""

        try:
            response_new = self.client.get_object(Bucket=self.BucketName, Key=str(Key))
            return response_new["Body"].read()

        except Exception as e:
            print("Error :{}".format(e))
            return False

    def find_one_update(self, data=None, key=None):
        """
        This checks if Key is on S3 if it is return the data from s3
        else store on s3 and return it
        """

        flag = self.item_exists(Key=key)

        if flag:
            data = self.get_item(Key=key)
            return data

        else:
            self.put_files(Key=key, Response=data)
            return data

    def delete_object(self, Key):
        response = self.client.delete_object(
            Bucket=self.BucketName,
            Key=Key,
        )
        return response

    def get_all_keys(self, Prefix="", max_page_number=100):
        """
        :param Prefix: Prefix string
        :return: Keys List
        """
        try:
            paginator = self.client.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.BucketName, Prefix=Prefix)

            tmp = []

            for page_no, page in enumerate(pages):
                if page_no > max_page_number:
                    break
                print("page_no : {}".format(page_no))
                for obj in page["Contents"]:
                    tmp.append(obj["Key"])

            return tmp
        except Exception as e:
            return []

    def print_tree(self):
        keys = self.get_all_keys()
        for key in keys:
            print(key)
        return None

    def find_one_similar_key(self, searchTerm=""):
        keys = self.get_all_keys()
        return [key for key in keys if re.search(searchTerm, key)]

    def __repr__(self):
        return "AWS S3 Helper class "

    def download_file_locally(self, key, filename):
        try:
            response = self.client.download_file(
                Bucket=self.BucketName,
                Filename=filename,
                Key=key,
                Callback=ProgressPercentage(
                    filename,
                    (self.client.head_object(Bucket=self.BucketName, Key=key))[
                        "ContentLength"
                    ],
                ),
                Config=TransferConfig(
                    max_concurrency=10,
                    use_threads=True,
                ),
            )
            return True
        except Exception as e:
            print("Error Download file : {}".format(e))
            return False

    def upload_files_from_local(self, file_name, key):
        try:
            response = self.client.upload_file(
                Filename=file_name,
                Bucket=self.BucketName,
                Key=key,
                Callback=ProgressPercentageUpload(file_name),
                Config=TransferConfig(
                    max_concurrency=10,
                    use_threads=True,
                ),
            )
            return True
        except Exception as e:
            print("Error upload : {} ".format(e))
            return False


def batch_objects_delete_threadded(batch_size=50, max_page_size=100):
    helper_qa = AWSS3(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("XXXXXXXXXXXXX"),
        region_name=os.getenv("AWS_REGION_NAME"),
        bucket=os.getenv("BUCKET"),
    )

    keys = helper_qa.get_all_keys(
        Prefix="database=XXXXXXXXXXX/", max_page_number=max_page_size
    )
    MainThreads = [
        threading.Thread(target=helper_qa.delete_object, args=(key,)) for key in keys
    ]

    print("Length: keys : {} ".format(len(keys)))
    for thread in tqdm(range(0, len(MainThreads), batch_size)):
        for t in MainThreads[thread : thread + batch_size]:
            t.start()
        for t in MainThreads[thread : thread + batch_size]:
            t.join()


# ==========================================
start = datetime.datetime.now()
batch_objects_delete_threadded()
end = datetime.datetime.now()
print("Execution Time : {} ".format(end - start))
# ==========================================
