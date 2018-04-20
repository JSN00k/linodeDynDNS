#!/usr/local/bin/python3

#TODO: update this to support IPv6 as well.

import requests
import json

token = ""
domain = ""
subdomain = ""

# Change this if I've removed my IP getter website, or you want to
# use a different one that you're sure won't change. My website
# and this script will change to support IPv6 at some indefinite
# point.
ip_getter_domain = "https://tools.twistedape.me.uk/get_ip.php"

linode_api_root = "https://api.linode.com/v4/"

if token == "" || domain == "":
    print("To run this script it is required that you set the token and "
          + "domain. You can generate a token at https://cloud.linode.com/profile/tokens"

def failed_request(status_code):
    print("The http request failed with status code: " + str(status_code))
    exit(0)

ip_req = requests.get(ip_getter_domain)
if ip_req.status_code != 200:
    failed_request(ip_req.status_code)


current_ip = ip_req.text



filter_dict = { "domain" : domain }

headers = { "Authorization" : "Bearer " + token,
            "X-Filter" : json.dumps(filter_dict)  }

get_domains_url = linode_api_root + "domains/"
domain_request = requests.get(get_domains_url, headers=headers)
if domain_request.status_code != 200:
    failed_request(domain_request.status_code)

domain_id = str(domain_request.json()["data"][0]["id"])

# Get the subdomain ID.

filter_dict = { "name" : subdomain, "type" : "A" }

headers = { "Authorization" : "Bearer " + token,
            "X-Filter" : json.dumps(filter_dict) }

get_subdomains_url = get_domains_url + domain_id + "/records/"
subdomain_request = requests.get(get_subdomains_url, headers=headers)

if subdomain_request.status_code != 200:
    failed_request(subdomain_request.status_code)

subdom_json = subdomain_request.json()

if subdom_json["data"][0]["target"] == current_ip:
    print("The current ip is " + current_ip + ". There is no need to update")
    exit(0)

subdom_id = str(subdom_json["data"][0]["id"])

# Update the IP Address to the current address.

headers = { "Authorization" : "Bearer " + token }

update_sub_url = get_subdomains_url + subdom_id

json_body = { "target" : current_ip }

update_request = requests.put(update_sub_url, headers=headers, json=json_body)
if update_request.status_code != 200:
    failed_request(update_request.status_code)

json_response = update_request.json()

if json_response["target"] != current_ip:
    print("Failed to update ip, unknown reason please investigate")
else:
    print("ip updated to " + current_ip)

