
import requests
import json

class MainRun():

    def __init__(self):
        pass

    def run(self,url,method,data,headers=None):
        self.url = url
        self.payload = data
        if headers:
            self.headers = headers
        else:
            self.headers = {"Content-Type":"application/json"}
        # 测试步骤
        if method == "POST":
            response = requests.post(self.url,headers=self.headers,json=self.payload)
            res = response.json()
            return res
        elif method == "GET":
            response = requests.get(self.url,headers=self.headers,json=self.payload)
            res = response.json()
            return res
