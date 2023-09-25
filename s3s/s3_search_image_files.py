import re
import boto3


class ImageSearch:
    """
    This class searches for thermal images which include `_T` in key, in an S3 bucket.
    """

    f_list = []

    def search_thermal_images(self, bucket_name, prefix):
        # List objects in the specified S3 bucket with the given prefix
        s3_client = boto3.client("s3")
        unique_dates = set()
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

            # Check if any objects were found and clean the list from non-image files.
            if "Contents" in response:
                print("Found matching files:")
                for obj in response["Contents"]:
                    file = obj["Key"].split("/").pop(1)
                    self.f_list.append(file)
            else:
                print("No matching files found in the bucket.")

            pattern = r"_T.jpeg"
            thermal_img_counter = 0
            no_thermal_img_counter = 0

            for idx, item in enumerate(self.f_list):
                if not item.endswith(".jpeg"):
                    self.f_list.pop(idx)

            # Get unique dates from the list of images. This will be used to group images by date.
            for img in self.f_list:
                unique_dates.add(img[:-7])

            # Sort images by date and build a dictionary with them.
            grouped_images = self.group_same_date_images(self.f_list)

            for item in self.f_list:
                if re.search(pattern, item):
                    thermal_img_counter += 1
                    print(f"Match found in '{item}'")
                else:
                    print(f"No _T match found in '{item}'")
            print(f"{thermal_img_counter} _T matches found")

            for group in grouped_images:
                if not any(pattern in img for img in group):
                    no_thermal_img_counter += 1

            return {
                "thermalImageCount": thermal_img_counter,
                "objectMissingThermalImageCount": no_thermal_img_counter,
            }

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    @staticmethod
    def group_same_date_images(img_list: list):
        """
        This method groups images with the same date in another list.
        :param img_list: list of images
        :return: list with grouped images
        """
        grouped_items = []
        unique_dates = set()

        for img in img_list:
            unique_dates.add(img[:-7])
        for img_name in unique_dates:
            tmp_list = []
            for img in img_list:
                if img_name == img[:-7]:
                    tmp_list.append(img)
            grouped_items.append(tmp_list)
        return grouped_items


if __name__ == "__main__":
    # Replace 'your-bucket-name' and 'your-prefix' with the actual S3 bucket name and prefix
    b_name = "briones-thermal-images"
    key_prefix = "COMPLETED 2023"

    img_search = ImageSearch()
    print(img_search.search_thermal_images(b_name, key_prefix))
