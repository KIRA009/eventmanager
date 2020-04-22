import requests
import sys
import hmac
import hashlib
from event_manager.settings import RAZORPAY_KEY, RAZORPAY_MID, RAZORPAY_SECRET

base_url = "https://api.razorpay.com/v1"
auth = (RAZORPAY_KEY, RAZORPAY_SECRET)


def create_order(amount):
    res = requests.post(
        f"{base_url}/orders",
        json={
            "amount": amount * 100,
            "currency": "INR",
            "receipt": "receipt",
            "payment_capture": 1,
        },
        auth=auth,
    ).json()
    if "error" in res:
        return False, res["error"]
    return True, res["id"]


def compare_string(expected_str, actual_str):
    if len(expected_str) != len(actual_str):
        return False
    result = 0
    for x, y in zip(expected_str, actual_str):
        result |= ord(x) ^ ord(y)
    return result == 0


def is_signature_safe(parameters):
    order_id = str(parameters["razorpay_order_id"])
    payment_id = str(parameters["razorpay_payment_id"])
    razorpay_signature = str(parameters["razorpay_signature"])
    msg = "{}|{}".format(order_id, payment_id)

    if sys.version_info[0] == 3:  # pragma: no cover
        key = bytes(RAZORPAY_SECRET, "utf-8")
        body = bytes(msg, "utf-8")

    dig = hmac.new(key=key, msg=body, digestmod=hashlib.sha256)

    generated_signature = dig.hexdigest()

    if sys.version_info[0:3] < (2, 7, 7):
        result = compare_string(generated_signature, razorpay_signature)
    else:
        result = hmac.compare_digest(generated_signature, razorpay_signature)

    if not result:
        return False
    return True


def get_order(order_id):
    res = requests.get(f"{base_url}/orders/{order_id}/payments", auth=auth).json()
    return res["items"]
