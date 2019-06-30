"""
Author      : Pratik Gawand
Created At  : 30 June 2019
Description : This file provides implementation for REST API  for creation of logo
"""

from flask import Flask, request, jsonify
import requests
import requests_cache
import json
import os

app = Flask(__name__)
app.config["DEBUG"] = True
COMPANY_LOGO_LENGTH = 3 # Configure Logo length 
SUCCESS_OK = 0 # Success
FAILURE = 2 # Something went wrong

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({ "status": "404","data" : "Page Not Found!" })

@app.route('/api/v1/company/generate_logo', methods=['GET'])
def get_logo_name():
    requests_cache.install_cache('cache_company_list') #cache for web request
   
    if 'id' in request.args:
        id = request.args['id']
    else:
        return jsonify({ "status": "200","data" : "Please specify company ID!" })
    
    # request web service for company list
    res = requests.get("https://next.json-generator.com/api/json/get/4JlWH4WlD")  

    # find matching company id
    company_info = find_company_info(id, res.json()) 
    if company_info == None:
        return jsonify(generate_op_repsonse(None,None))
    else:    
        sorted_company_name = generate_sorted_company_name(company_info)

        logo_name = generate_logo_str(sorted_company_name)

        return jsonify(generate_op_repsonse(company_info,logo_name))

def find_company_info(id, company_info):
    company_details = None
    for company in company_info:
        if company['CompanyId'] == id:
            company_details = company
            break

    return company_details


def generate_sorted_company_name(company_info):
    company_name = company_info['Company Name'].replace(" ", "").upper()
    return ''.join(sorted(company_name))

def generate_logo_str(sorted_company_name):
    sorted_company_name_list={}
    list_of_character = []

    for s in sorted_company_name:
        if s in sorted_company_name_list.keys():
            sorted_company_name_list[s]+=1
        else:
            sorted_company_name_list[s]=1

    weighted_company_name_tuple = sorted(sorted_company_name_list.items(), key=lambda x: x[1], reverse=True)
    if len(weighted_company_name_tuple)>3:
        i = 0
        logo_arr = []
        while (i < COMPANY_LOGO_LENGTH):
            logo_arr.append(weighted_company_name_tuple[i][0])
            i = i+1   
        return ", ".join(logo_arr)
    else:
        return None

def generate_op_repsonse(company_info, logostr):
    response = {}
    if company_info == None and logostr == None:
        response['status'] = FAILURE
        response['message'] = "Something went wrong!!"
    else:
        response['status'] = SUCCESS_OK
        response['companyId'] = company_info['CompanyId']
        response['companyName'] = company_info['Company Name']
        response['logoCharacters'] = logostr
        response['message'] = "Logo generated!!"

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
