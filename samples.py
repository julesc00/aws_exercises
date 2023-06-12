

class PayloadType:
    CREDIT_APP_POST = "CREDIT_APP_POST"
    CREDIT_APP_PATCH = "CREDIT_APP_PATCH"
    CREDIT_APP_UPDATE = "CREDIT_APP_UPDATE"
    CREDIT_APP_REPROCESS = "CREDIT_APP_REPROCESS"
    CONTRACT_POST = "CONTRACT_POST"
    VERIFY_CONTRACT_POST = "VERIFY_CONTRACT_POST"
    SIGN_CONTRACT_POST = "SIGN_CONTRACT_POST"
    LEAD_POST = "LEAD_POST"
    LEAD_PATCH = "LEAD_PATCH"
    LEAD_UPDATE = "LEAD_UPDATE"
    CREDIT_BUREAU_PULL = "CREDIT_BUREAU_PULL"
    CREDIT_BUREAU_PULL_DEAL_UPDATE = "CREDIT_BUREAU_PULL_DEAL_UPDATE"
    CREDIT_BUREAU_RESPONSE = "CREDIT_BUREAU_RESPONSE"
    KEY_DATA_UPDATE = "KEY_DATA_UPDATE"
    KEY_DATA_POST = "KEY_DATA_POST"
    KEY_DATA_STREAM = "KEY_DATA_STREAM"

    @staticmethod
    def get_payload_component_id(payload_type: str):
        return {
            PayloadType.LEAD_POST: "leadRefId",
            PayloadType.LEAD_UPDATE: "leadRefId",
            PayloadType.LEAD_PATCH: "leadRefId",
            PayloadType.CREDIT_APP_POST: "creditAppId",
            PayloadType.CREDIT_APP_PATCH: "creditAppId",
            PayloadType.CREDIT_APP_UPDATE: "creditAppId",
            PayloadType.CONTRACT_POST: "contractRefId",
            PayloadType.VERIFY_CONTRACT_POST: "contractRefId",
            PayloadType.SIGN_CONTRACT_POST: "contractRefId",
        }.get(payload_type)


if __name__ == "__main__":
    payload = PayloadType()
    print(payload.get_payload_component_id("hello"))
