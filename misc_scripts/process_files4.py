import re

string = "etl/alphasense/simon_mail/events/2024/02/19/15/alphasense_simon_mail_events_2024-02-19-03-54-918568-431f199e-00c1-409c-b7c8-e881597842c3"
pattern = r"(?<=-)\d{6}(?=-)"

matches = re.findall(pattern, string)
breakpoint()
print(matches)


def test__process_org(self, subscription_center):
    importer = SubscriptionCenterImporter()
    importer._process_org(subscription_center.organization)
    logger_info = (
        f"Processing organization: {subscription_center.organization.unique_name}"
    )
    assert logger_info == "Processing organization: org_0"
