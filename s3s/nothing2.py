import multiprocessing
import os
from multiprocessing import Pool
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


def extract_date(img):
    env = os.getenv("ENV", "dev")
    dgi_idx = img.find("DJI_")
    ext = ["_T.JPG", "_T.jpg", "_T_FLIR.jpg", "_T_FLIR.JPG"]
    for e in ext:
        if img.endswith(e):
            return img[dgi_idx + 4 : -len(e)]
    return None


def process_file(file):
    date = extract_date(file)
    return date, file


def group_by_date():
    unique_dates = set()

    # Create a multiprocessing pool with the number of available CPU cores
    num_processes = multiprocessing.cpu_count()
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_file, files)

    for date, _ in results:
        if date:
            unique_dates.add(date)

    grouped_items = {date: [] for date in unique_dates}
    for date, file in results:
        print("file", file)
        print("date", date)
        if date:
            grouped_items[date].append(file)

    print(unique_dates)
    print(f"Number of groups: {len(grouped_items)}")

    return grouped_items


if __name__ == "__main__":
    pprint(group_by_date())
