import urllib.request
import pandas as pd
import json

from config.config_20171221 import DEFAULTS_API

import sys
import os
import time
import math


def get_api_id_secret(i):
    usage_num = i % 5
    api_id = DEFAULTS_API['API_ID']
    api_secret = DEFAULTS_API['API_SECRET']
    return api_id[usage_num], api_secret[usage_num]
        
        
def get_response_body_dict(api_id, api_secret, encQuery, display, start):
    url = "https://openapi.naver.com/v1/search/local.json?query={}&display={}&start={}".format(encQuery, display, start)
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", api_id)
    request.add_header("X-Naver-Client-Secret", api_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()    
    if(rescode==200):
        response_body = response.read()
        return json.loads(response_body.decode('utf-8'))
    else:
        return None
    

def get_api_dictlist(api_id, api_secret, local_category_query, display):
    encQuery = urllib.parse.quote(local_category_query)
    
    # check total result to set total trial number
    check_total_dict = get_response_body_dict(
        api_id, api_secret, encQuery, display, 1)
    total_num = check_total_dict['total']
    
    # get total trial number with ceil
    total_trial = int(math.ceil(total_num/display))  
    
    # get all results for a single query as dicts in a list
    count = 0
    query_result_dictlist = []
    for trial_num in range(1, total_trial+1):
        start = display * (trial_num-1) + 1
        try:
            temp_dict = get_response_body_dict(
                api_id, api_secret, encQuery, display, start)
            query_result_dictlist.extend(temp_dict['items'])
            count += 1
        except:
            pass
    return query_result_dictlist, total_trial, count