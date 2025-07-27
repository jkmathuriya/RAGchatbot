import requests
from config import API_URL


def upload_docs_api(files):
    files_payload=[ ("files",(f.name,f.read(),"application/pdf")) for f in files]

    return requests.post(f"{API_URL}/upload_files/", files=files_payload)



def chat(query):
    return requests.post(f"{API_URL}/chat/",data={"query":query})

