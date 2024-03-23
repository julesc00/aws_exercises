from datetime import datetime

# Example timestamps as strings
timestamp_str1 = "2024-02-20 18:02:07+00:00"
timestamp_str2 = "2024-02-20 18:02:08+00:00"

# Parse strings into datetime objects
timestamp_dt1 = datetime.strptime(timestamp_str1, "%Y-%m-%d %H:%M:%S%z")
timestamp_dt2 = datetime.strptime(timestamp_str2, "%Y-%m-%d %H:%M:%S%z")

# Compare the datetime objects
if timestamp_dt1 < timestamp_dt2:
    print("Timestamp 1 is earlier than Timestamp 2")
elif timestamp_dt1 > timestamp_dt2:
    print("Timestamp 1 is later than Timestamp 2")
else:
    print("Timestamps are equal")
