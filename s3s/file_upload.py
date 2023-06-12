import os
from io import BytesIO
import boto3
from botocore.exceptions import ConnectionError
from PIL import Image, ImageOps


class S3Handler:
    def __init__(self):
        self.s3_session = boto3.session.Session()
        self.s3_client = self.s3_session.client("s3")
        self.s3_resource = self.s3_session.resource("s3")
        self.bucket = "my_bucket"
        self.file_name = "my_file.txt"
        self.file_path = "/s3s/my_file.txt"
        self.bytes_file = None
        self.img = None

    def upload_s3_file(self):
        path_to_file = os.path.join(self.file_path, self.file_name)

        self.s3_client.upload_file(
            path_to_file,
            bucket=self.bucket,
            filename=self.file_name
        )

    def get_s3_file(self, bucket, obj_key):
        file = self.s3_resource.Object(
            bucket,
            obj_key
        )
        self.bytes_file = file.get()["Body"].read()
        print(self.bytes_file)
        return self.bytes_file

    def resize_image(self, img_from_s3, obj_key, width_size):
        try:
            self.img = self.get_s3_file(img_from_s3, obj_key)
        except ConnectionError as error:
            print(error)
        img_bytes = Image.open(BytesIO(self.img))
        img = ImageOps.exif_transpose(img_bytes)
        w_percent = (width_size / float(img.size[0]))
        print(w_percent)
        h_size = int((float(img.size[1] * float(w_percent))))
        print(h_size)
        img = img.resize((width_size, h_size))
        print(img)
        img.save("descontrolar3.jpeg", "jpeg")


handler = S3Handler()
handler.resize_image("briones-user-data-12242023", "descontrolar.jpeg", 480)
