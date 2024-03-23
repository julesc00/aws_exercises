import re

from collections import defaultdict


def sort_strings_by_timestamp_v2(files):
    timestamps_files_dict = defaultdict(list)

    # Group files by their timestamps
    for file in files:
        timestamp = extract_unix_timestamp_v2(file)
        timestamps_files_dict[timestamp].append(file)

    # Extract files associated with each timestamp
    sorted_files = [
        file
        for timestamp in sorted(timestamps_files_dict.keys())
        for file in timestamps_files_dict[timestamp]
    ]
    return sorted_files


# Assume extract_unix_timestamp function is defined as before
def extract_unix_timestamp_v2(file):
    pattern = r"(?<=-)\d{6}(?=-)"
    match = re.findall(pattern, file.get("Key"))
    if match:
        return match[0]
    return None


def extract_unix_timestamps(files: list[dict]):
    pattern = r"(?<=-)\d{6}(?=-)"
    unix_timestamps = [
        re.findall(pattern, file.get("Key"))[0]
        for file in files
        if re.findall(pattern, file.get("Key"))
    ]
    return sorted(unix_timestamps)


def sort_strings_by_timestamp(files: list[dict]):
    timestamps = extract_unix_timestamps(files)
    sorted_files = []
    for timestamp in timestamps:
        for file in files:
            if timestamp in file["Key"]:
                sorted_files.append(file)

    return sorted_files


objs = [
    {
        "Key": "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-53-978254-33f9fbdb-9f41-4628-bba8-0fdf3eeebfdb",
        "Size": "1.0 KB",
        "LastModified": "978254",
    },
    {
        "Key": "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-54-548758-ab0c411c-8dcd-424f-a3d5-d82d0edfc825",
        "Size": "1.0 KB",
        "LastModified": "978254",
    },
    {
        "Key": "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-54-918568-431f199e-00c1-409c-b7c8-e881597842c3",
        "Size": "1.0 KB",
        "LastModified": "978254",
    },
    {
        "Key": "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-55-049009-b3d9bdb6-d1dd-4cfc-a86c-6f22ebf0c9ad",
        "Size": "1.0 KB",
        "LastModified": "978254",
    },
    {
        "Key": "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-55-521807-91572738-fe03-4bec-b610-8c190cc91080",
        "Size": "1.0 KB",
        "LastModified": "978254",
    },
    {
        "Key": "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-56-353497-62b8b9ef-87bf-45e6-b9ce-eac21e407519",
        "Size": "1.0 KB",
        "LastModified": "978254",
    },
]

# Example usage:
strings = [
    "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-53-978254-33f9fbdb-9f41-4628-bba8-0fdf3eeebfdb",
    "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-54-548758-ab0c411c-8dcd-424f-a3d5-d82d0edfc825",
    "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-54-918568-431f199e-00c1-409c-b7c8-e881597842c3",
    "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-55-049009-b3d9bdb6-d1dd-4cfc-a86c-6f22ebf0c9ad",
    "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-55-521807-91572738-fe03-4bec-b610-8c190cc91080",
    "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-56-353497-62b8b9ef-87bf-45e6-b9ce-eac21e407519",
]

if __name__ == "__main__":
    sorted_strings = sort_strings_by_timestamp(objs)
    print(len(sorted_strings))
    for string in sorted_strings:
        print(string)
