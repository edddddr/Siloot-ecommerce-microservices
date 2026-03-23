def parse_payment_completed(event):
    return event["data"]

def parse_payment_failed(event):
    return event["data"]