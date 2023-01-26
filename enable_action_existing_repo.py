import json
import sys
from bs4 import BeautifulSoup
import requests

repo_name = sys.argv[1]
auth_token = sys.argv[2]

hed = {'Authorization': 'Bearer ' + auth_token, 'Accept': 'application/vnd.github.v3+json'}
url = 'https://github.albertsons.com/api/v3/repos/albertsons/'+repo_name
response = requests.get(url, headers=hed)
repo_id = response.json()
action_id = repo_id['id']

hed_action = {'Authorization': 'Bearer ' + auth_token, 'Accept': 'application/vnd.github.v3+json'}
action_url = 'https://github.albertsons.com/api/v3/orgs/albertsons/actions/permissions/repositories/'+str(action_id)
action_response = requests.put(action_url, headers=hed_action)
