import re
import boto3


class ImageSearch:
    """
    This class searches for thermal images which include `_T` in key, in an S3 bucket.
    """

    f_list = []

    def __int__(self):
        self.images = []

    def search_thermal_images(self, bucket_name, prefix):
        # List objects in the specified S3 bucket with the given prefix
        s3_client = boto3.client("s3")

        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

            # Check if any objects were found
            if "Contents" in response:
                print("Found matching files:")
                for obj in response["Contents"]:
                    file = obj["Key"].split("/").pop(1)
                    self.f_list.append(file)
            else:
                print("No matching files found in the bucket.")

            pattern = r"_T.jpeg"
            thermal_img_counter = 0
            for idx, item in enumerate(self.f_list):
                if not item.endswith(".jpeg"):
                    self.f_list.pop(idx)
            for item in self.f_list:
                if re.search(pattern, item):
                    thermal_img_counter += 1
                    print(f"Match found in '{item}'")
                else:
                    print(f"No _T match found in '{item}'")
            print(f"{thermal_img_counter} _T matches found")

            return self.f_list

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Replace 'your-bucket-name' and 'your-prefix' with your actual S3 bucket name and prefix
    b_name = "briones-thermal-images"
    key_prefix = "COMPLETED 2023"

    img_search = ImageSearch()
    print(img_search.search_thermal_images(b_name, key_prefix))
