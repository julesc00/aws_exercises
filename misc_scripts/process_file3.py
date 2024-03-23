import re
from typing import List


def extract_unix_timestamp(self, files: List[dict]):
    pattern = r"(?<=-)\d{6}(?=-)"
    unix_timestamps = [
        re.findall(pattern, file.get("Key"))[0]
        for file in files
        if re.findall(pattern, file.get("Key"))[0]
    ]
    return sorted(unix_timestamps)


def sort_strings_by_timestamp(self, files: List[dict]):
    timestamps = self.extract_unix_timestamp(files)
    sorted_files = []
    for timestamp in timestamps:
        for file in files:
            if timestamp in file["Key"]:
                sorted_files.append(file)

    return sorted_files
