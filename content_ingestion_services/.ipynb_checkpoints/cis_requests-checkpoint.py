import requests

def deep_detect_classify(text, threshold=0.4):
    data = {
          "service": 'records',
          "parameters": {
            "input": {},
            "output": {
              "confidence_threshold": threshold
            },
            "mllib": {
              "gpu": False
            }
          },
          "data": [text]
        }
    server = 'https://ecms-cis-deepdetect-api-prod.edap-cluster.com/predict'
    r = requests.post(server,json=data)
    return r.json()['body']['predictions'][0]['classes'][0]

def nlp_buddy_analyze(text):
    data = { "text":  text }
    server = 'https://ecms-cis-nlpbuddy.edap-cluster.com/api/analyze'
    r = requests.post(server,json=data)
    return r.json()

def tika(file):
    files = {'file': file}
    headers = {
                "Cache-Control": "no-cache",
                "accept": "text/plain"
              }
    server = 'https://ecms-cis-tika-prod.edap-cluster.com/tika/form'
    r = requests.post(server, files=files, headers=headers)
    return r.text

def xtika(file):
    headers = {
              "Content-Type" : "application/pdf",
              "X-Tika-PDFOcrStrategy": "ocr_only",
              "Cache-Control": "no-cache",
              "accept": "text/plain"
            }
    server = "https://ecms-cis-tika-prod.edap-cluster.com/tika"
    r = requests.put(server, data=file, headers=headers)
    return r.text