
def lambda_handler(event, context):
    result = int(event["first_number"]) + int(event["second_number"])
    return {
        "sum": result
    }
