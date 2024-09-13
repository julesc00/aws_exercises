import copy
import os
from dataclasses import dataclass, field
from pprint import pprint
from typing import List


@dataclass
class FileFormatExclusions:
    _formats: List[str] = field(default_factory=lambda: [".exe", ".docx", ".xlsx"])

    @property
    def formats(self):
        return self._formats


metadata_json = {
    "homeowner_contract_id": "0280afb0",
    "contract_status:": "pto_date_applied",
    "type_of_facility": "Solar - electricity generation or heating/cooling",
    "county": "Broward",
    "postal_code": "24524-2849",
    "state": "FL",
    "latitude": "34.778407",
    "longitude": "-112.515267",
    "date_const_began": "20240501",
    "date_place_in_serive": "20240715",
    "low_income_Community_Indicator": "1",
    "file_mappings": [
        {
            "document_name": "CA PowerShift Agreement - Signed.pdf",
            "document_type": "contract",
            "document_path": "path/0280afb0/contract"
        }
        ,
        {
            "document_name": "California Solar + Storage PPA Installation Agreement - Signed.pdf",
            "document_type": "ppa_agreement",
            "document_path": "path/0280afb0/contract/California Solar + Storage PPA Installation Agreement - Signed.pdf"
        },
        {
            "document_name": "35786 Grandview- PTO Issued - SBP-32644.pdf",
            "document_type": "pto_letter",
            "document_path": "path/0280afb0/pto"
        },
        {
            "document_name": "certificate - Signed.exe",
            "document_type": "work_order_certificate",
            "document_path": "path/0280afb0/work_order_2"
        },
        {
            "document_name": "Work Order - Signed.pdf",
            "document_type": "work_order",
            "document_path": "path/0280afb0/work_order_2"
        }
    ],
    "source_system": "Everbright",
    "technology": "RESI",
    "tax_year": "2023"
}

class FileValidator:
    def __init__(self, metadata, s3_files):

        self.exclusions = FileFormatExclusions()
        self.s3_files = s3_files
        self.metadata = copy.deepcopy(metadata)
        self.contract_id = metadata["homeowner_contract_id"]
        self.mappings = metadata_json["file_mappings"]

    def exclude_invalid_file_formats(self):
        excluded = []
        for file in self.mappings[:]:
            _, file_ext = os.path.splitext(file.get("document_name"))
            if file_ext in self.exclusions.formats:
                excluded.append(file)
                self.metadata["file_mappings"].remove(file)

        print(f"Excluded files: {excluded}")
        return self.metadata, excluded


if __name__ == "__main__":
    s3_files = ["CA PowerShift Agreement - Signed.pdf", "California Solar + Storage PPA Installation Agreement - Signed.pdf", "35786 Grandview- PTO Issued - SBP-32644.pdf", "certificate - Signed.exe", "Work Order - Signed.pdf"]
    fv = FileValidator(metadata_json, s3_files)
    pprint(fv.exclude_invalid_file_formats())