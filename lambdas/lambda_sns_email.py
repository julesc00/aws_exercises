# import boto3
from http import HTTPStatus
from typing import Dict, List

topic_arn = "arn:aws:sns:us-east-1:145622053217:s3-events-to-lambda-topic"


log_data = [{'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/work_order_1/Work '
             'Order - Signed.pdf/Work Order - Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/work_order_1/certificate '
             '- Signed.pdf/certificate - Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/other_docs/Shade '
             'Report.pdf/Shade Report.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/work_order_2/Installer '
             'Change Order - Signed.pdf/Installer Change Order - Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/other_docs/ID682499_20240612_1.pdf/ID682499_20240612_1.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/contract/IL Solar '
             'PPA Installation Agreement - Signed.pdf/IL Solar PPA '
             'Installation Agreement - Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/contract/Welcome '
             'Call Checklist Single Signer (EverFixed PPA) - '
             'Signed.pdf/Welcome Call Checklist Single Signer (EverFixed PPA) '
             '- Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/contract/Illinois '
             'Fixed PPA Agreement - Signed.pdf/Illinois Fixed PPA Agreement - '
             'Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/contract/certificate '
             '- Signed.pdf/certificate - Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/work_order_3/certificate '
             '- Signed.pdf/certificate - Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/work_order_2/certificate '
             '- Signed.pdf/certificate - Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/conditional_lien_waiver/Conditional '
             'Lien Waiver - Signed.pdf/Conditional Lien Waiver - Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/other_docs/IMG_1805.jpg/IMG_1805.jpg',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/work_order_3/Installer '
             'Change Order - Signed.pdf/Installer Change Order - Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/conditional_lien_waiver/certificate '
             '- Signed.pdf/certificate - Signed.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/other_docs/IMG_1806.jpg/IMG_1806.jpg',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/pto_letter/Certificate '
             'of Completion.pdf/Certificate of Completion.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/other_docs/635 '
             'Mulberry St, Browns, IL 62818, USA_A2.pdf/635 Mulberry St, '
             'Browns, IL 62818, USA_A2.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'},
 {'contract_id': 'b55b27c8',
  'error_indicator': 1,
  'error_message': 'Document does not exist in bucket',
  'new_doc': '-',
  'new_path': '-',
  'old_doc': '202409181904_everbright_b55b27c8_contractpkg/pto_letter/Charles '
             'D (David)Terry PTO.pdf/Charles D (David)Terry PTO.pdf',
  'old_path': '-',
  'process_id': 100,
  'timestamp': '20241009-114425'}]


# def send_sns(message: str, subject: str) -> bool:
#     sns_client = boto3.client("sns")
#
#     try:
#         res = sns_client.publish(
#             TopicArn=topic_arn,
#             Message=message,
#             Subject=subject
#         )
#         if res["ResponseMetadata"]["HttpsStatusCode"] == HTTPStatus.OK:
#             print(res)
#             print("[INFO] Notification sent successfully")
#             return True
#     except Exception as err:
#         print(err)
#         return True

def process_sns_logs(l_data: List[dict], env: str) -> bool:
    contract_id = l_data[0].get("contract_id")
    message= f"Contract: {contract_id}\nEnvironment: {env}".strip()
    for log in log_data:
        doc = log["old_doc"]
        err_msg = log["error_message"]
        sep = "-" * 10
        partial = f"{sep}\nfile: {doc}\nfile status: {err_msg}".strip()
        message += "\n" + partial

    print(message)

if __name__ == "__main__":
    process_sns_logs(l_data=log_data, env="dev")