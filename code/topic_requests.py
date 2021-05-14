#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 18:29:41 2021

@author: cbadenes
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import time

base_name = "mesinesp-llda-desc-l"

for i in range(15):
    file_name = base_name+str(i)+".json"
    json_content = json.load(open(file_name, "r"))
    res = requests.post('https://librairy.linkeddata.es/api/topics', json=json_content, auth=HTTPBasicAuth('librAIry', 'l1brA1ry'))
    if res.ok:
        print(file_name,res.json())
        print("Waiting for 5secs..")
        time.sleep(5.0)
    else:
        print("Response error")
        break