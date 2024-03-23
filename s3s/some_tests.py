extract_unix_timestamp = SubscriptionCenterImporter().extract_unix_timestamp
sort_strings_by_timestamp = SubscriptionCenterImporter().sort_strings_by_timestamp


def test_extract_unix_timestamp_with_match():
    file = {
        "Key": "etl/alphasense/simon_mail/events/2024/02/19/15"
        "/alphasense_simon_mail_events_2024-02-19-03-54-918568-431f199e"
        "-00c1-409c-b7c8-e881597842c3"
    }
    assert extract_unix_timestamp(file) == "918568"


def test_extract_unix_timestamp_without_match():
    file = {
        "Key": "etl/alphasense/simon_mail/events/2024/02/19/15"
        "/alphasense_simon_mail_events_2024-02-19-03-54-abcde-431f199e"
        "-00c1-409c-b7c8-e881597842c3"
    }
    timestamp = extract_unix_timestamp(file)

    assert timestamp is None


def test_extract_unix_timestamp_with_invalid_key():
    file = {"Key": ""}
    assert extract_unix_timestamp(file) is None


def test_sort_strings_by_timestamp_with_valid_files():
    files = [
        {
            "Key": "etl/alphasense/simon_mail/events/2024/02/19/15"
            "/alphasense_simon_mail_events_2024-02-19-03-54-918568-431f199e"
            "-00c1-409c-b7c8-e881597842c3",
            "Size": "1.0 KB",
            "LastModified": "2024-02-21 18:52:52+00:00",
        },
        {
            "Key": "etl/alphasense/simon_mail/events/2024/02/19/15"
            "/alphasense_simon_mail_events_2024-02-19-03-53-978254-33f9fbdb"
            "-9f41-4628-bba8-0fdf3eeebfdb",
            "Size": "1.0 KB",
            "LastModified": "2024-02-21 18:53:12+00:00",
        },
        {
            "Key": "etl/alphasense/simon_mail/events/2024/02/19/15"
            "/alphasense_simon_mail_events_2024-02-19-03-55-049009-b3d9bdb6"
            "-d1dd-4cfc-a86c-6f22ebf0c9ad",
            "Size": "1.0 KB",
            "LastModified": "2024-02-21 18:53:14+00:00",
        },
    ]
    expected_result = [
        {
            "Key": "etl/alphasense/simon_mail/events/2024/02/19/15"
            "/alphasense_simon_mail_events_2024-02-19-03-55-049009-b3d9bdb6"
            "-d1dd-4cfc-a86c-6f22ebf0c9ad",
            "Size": "1.0 KB",
            "LastModified": "049009",
        },
        {
            "Key": "etl/alphasense/simon_mail/events/2024/02/19/15"
            "/alphasense_simon_mail_events_2024-02-19-03-54-918568-431f199e"
            "-00c1-409c-b7c8-e881597842c3",
            "Size": "1.0 KB",
            "LastModified": "2024-02-21 18:53:12+00:00",
        },
        {
            "Key": "etl/alphasense/simon_mail/events/2024/02/19/15"
            "/alphasense_simon_mail_events_2024-02-19-03-53-978254-33f9fbdb"
            "-9f41-4628-bba8-0fdf3eeebfdb",
            "Size": "1.0 KB",
            "LastModified": "2024-02-21 18:53:14+00:00",
        },
    ]
    assert sort_strings_by_timestamp(files) == expected_result


def test_sort_strings_by_timestamp_with_empty_list():
    files = []
    assert sort_strings_by_timestamp(files) == []

    def test__process_org(self, subscription_center):
        importer = SubscriptionCenterImporter()
        importer._process_org(subscription_center.organization)
        logger_info = (
            f"Processing organization: {subscription_center.organization.unique_name}"
        )

        assert logger_info == "Processing organization: org_0"
