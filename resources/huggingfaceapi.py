import json
import requests


API_TOKEN = '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'
headers = {"Authorization": f"Bearer {API_TOKEN}"}

API_URL = 'https://api-inference.huggingface.co/models/BK-V/xlm-roberta-base-finetuned-arman-fa'
def query_ner(payload):

    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8")) , response.status_code



API_URL_ASR = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"
def query_asr(data):

    response = requests.request("POST", API_URL_ASR, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8")) , response.status_code