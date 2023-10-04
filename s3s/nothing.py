from pprint import pprint
from collections import defaultdict

files = [
    "COMPLETED 2023/20223-579 HOMELAND 408661 FF-RELIABILITY 3.7 MI 9.1.23/DJI_20230901153505_0034_T.JPG",
    "COMPLETED 2023/20223-579 HOMELAND 408661 FF-RELIABILITY 3.7 MI 9.1.23/DJI_20230901153505_0034_W.jpg",
    "COMPLETED 2023/20223-579 HOMELAND 408661 FF-RELIABILITY 3.7 MI 9.1.23/DJI_20230901153505_0034_Z.JPG",
    "COMPLETED 2023/20223-579 HOMELAND 408661 FF-RELIABILITY 3.7 MI 9.1.23/DJI_20230901153506_0034_T.jpg",
    "COMPLETED 2023/20223-579 HOMELAND 408661 FF-RELIABILITY 3.7 MI 9.1.23/DJI_20230901153506_0034_W.JPG",
    "COMPLETED 2023/20223-579 HOMELAND 408661 FF-RELIABILITY 3.7 MI 9.1.23/DJI_20230901153506_0034_Z.JPG",
    "COMPLETED 2023/20223-579 HOMELAND 408661 FF-RELIABILITY 3.7 MI 9.1.23/DJI_20230901153507_0035_T_FLIR.JPG",
    "COMPLETED 2023/20223-579 HOMELAND 408661 FF-RELIABILITY 3.7 MI 9.1.23/DJI_20230901153507_0035_W.JPG",
    "COMPLETED 2023/20223-579 HOMELAND 408661 FF-RELIABILITY 3.7 MI 9.1.23/DJI_20230901153507_0035_Z.JPG",
]


def group_by_date():
    unique_dates = set()
    grouped_items = []
    ext = "_T.JPG"
    ext2 = "_T.jpg"
    ext3 = "_T_FLIR.jpg"
    ext4 = "_T_FLIR.JPG"

    for img in files:
        dgi_idx = img.find("DJI_")

        if ".jpg" in img or ".JPG" in img:
            if ext in img or ext2 in img:
                unique_dates.add(img[dgi_idx + 4 : -len(ext)])
            elif ext3 in img or ext4 in img:
                unique_dates.add(img[dgi_idx + 4 : -len(ext3)])
    counter = 0
    group_counter = 0
    group_counts = []
    grouped_dict = defaultdict(list)
    for img in files:
        for date in unique_dates:
            if date in img and "_T" not in img:
                group_counter += 1
                group_counts.append(group_counter)
                break

    for count in group_counts:
        if count < 3:
            counter += 1

    print(unique_dates)

    return f"Groups with no images: {counter}"


pprint(group_by_date())
