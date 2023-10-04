from collections import defaultdict
from pprint import pprint

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


def group_by_date_and_index(files):
    grouped_items = defaultdict(list)

    for img in files:
        # Extract relevant substring that follows "DJI_"
        dgi_idx = img.find("DJI_")
        if dgi_idx != -1:  # If "DJI_" found
            date_and_index = img[
                dgi_idx + 4 : dgi_idx + 6 + 17
            ]  # Extract date and index
            grouped_items[date_and_index].append(img)

    print(f"Unique date and index: {list(grouped_items.keys())}")
    print(f"Number of groups: {len(grouped_items)}")

    return grouped_items


items = group_by_date_and_index(files)

for key, group in items.items():
    for img in group:
        print(img)
        if "_T" not in img:
            print(f"Thermal image NOT found in group {key}")
            break
