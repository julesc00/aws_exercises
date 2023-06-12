
def test_create_bucket(s3):
    s3.create_bucket(Bucket="some_bucket")
    result = s3.list_buckets()

    assert len(result.get("Buckets")) == 1
    assert result["Buckets"][0]["Name"] == "some_bucket"

