import hashlib
import hmac
import base64
import time
import requests

sms_uri = "/sms/v2/services/ncp:sms:kr:293497734839:ticketing_notification/messages"
sms_url = "https://sens.apigw.ntruss.com" + sms_uri
sms_type = "SMS"
sms_from_countrycode = ""
sms_from_number = "01084456318"
sms_to_number = "01084456318"
sms_access_key = "Jsptxk9idsTZpTevZv3c"
sms_secret_key = "C63gEi4OnpLGsFrPBRTH90XhzLV3ObTPHexx16JT"

class Notification():
    def	make_signature(self, access_key, secret_key, method, uri):
        timestamp = str(int(time.time() * 1000))
        secret_key = bytes(secret_key, 'UTF-8')

        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def send_sms(self, phone_number, message):
        timestamp = str(int(time.time() * 1000))
        body = {
            "type":sms_type,
            "from":sms_from_number,
            "content":message,
            "messages":[
                {
                    "to":phone_number,
                    "content":message
                }
            ]
        }

        key = self.make_signature(sms_access_key, sms_secret_key, "POST", sms_uri)
        
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': sms_access_key,
            'x-ncp-apigw-signature-v2': key
        }

        res = requests.post(sms_url, json=body, headers=headers)
        return res.json()