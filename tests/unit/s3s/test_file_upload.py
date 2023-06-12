import pytest
from moto import mock_s3

from s3s.file_upload import S3Handler


@mock_s3
@pytest.mark.skip
def test_upload_s3_file():
    s3_handler = S3Handler()
    s3_handler.upload_s3_file()
