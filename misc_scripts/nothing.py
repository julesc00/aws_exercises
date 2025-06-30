from typing import Dict

def validate_and_format_year_date(metadata_obj: Dict):
    date_key = "date_placed_in_service"
    if date_key in metadata_obj:
        raw_date = str(metadata_obj[date_key])
        # Case 1: Already in YYYYMD format
        if len(raw_date) == 6:
            year, month = raw_date[:4], raw_date[4:6]
            month = "0" + month[0]

            # Correct and set the date back
            metadata_obj[date_key] = f"{year}{month}"
        elif len(raw_date) == 8:
            return metadata_obj
    return metadata_obj


metadata = {
    "date_placed_in_service": "20241110",
    "document_package": [
        {
            "document_type": "whatever",
            "document_category": "PTO",
            "document_tags": [
                "tct",
                "abc"
            ]
        }
    ]
}

validated_metadata = validate_and_format_year_date(metadata_obj=metadata)
print(validated_metadata)
print(f"date_year: {validated_metadata['date_placed_in_service']}")
print("tct" in validated_metadata["document_package"][0]["document_tags"])