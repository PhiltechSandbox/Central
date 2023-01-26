import json
import sys
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

now = datetime.now()

snow_auth_token = sys.argv[1]
snow_hed = {'Authorization': 'Basic ' + snow_auth_token}

git_auth_token = sys.argv[2]
git_hed = {'Authorization': 'Bearer ' + git_auth_token, 'Accept': 'application/vnd.github.v3+json'}

print('Reading CR data from central Json file')
with open("change_info.json", "r") as f:
     data_json = json.load(f)
print(data_json)

for key in data_json:
 print('.........')
 print('For CR ' + key + ':')
 starttime=datetime.strptime(data_json[key]['work_start'], '%Y-%m-%d %H:%M:%S')
 if now-timedelta(minutes=20) < starttime <= now+timedelta(minutes=2) and data_json[key]['phase_state'] == "Pending":
  print('Sheduled at: ' + data_json[key]['work_start'])

  print('Updating CR phase state to In-progress...')
  update_url = 'https://safewayqa1.service-now.com/api/now/table/u_change_request_staging'
  update_data = { "u_execution_type": "update", "u_change_request_number":  key , "u_phase_state": "In Progress" }
  update_response = requests.post(update_url, json=update_data, headers=snow_hed)

  print('Getting action id...')
  url = 'https://github.albertsons.com/api/v3/repos/albertsons/' + data_json[key]['repo_name'] + '/actions/workflows'
  response = requests.get(url, headers=git_hed)
  workflow_data = response.json()
  workflow_name = data_json[key]['workflow_name']
  print('Repo name is: ' + data_json[key]['repo_name'])
  print('workflow name is: ' + data_json[key]['workflow_name'])
  for keyval in workflow_data['workflows']:
    if workflow_name == keyval['name']:
      action_id = str(keyval['id'])
      print('action id is: ' + action_id)
  action_url = 'https://github.albertsons.com/api/v3/repos/albertsons/' + data_json[key]['repo_name'] + '/actions/workflows/'+str(action_id)+'/dispatches'
  print('action url is: ' + action_url)   
  print('Release Tag: ' +  data_json[key]['Tag'])
  data = {"ref":"master", "inputs": { "image_tagid": data_json[key]['Tag'] }}
  print('Triggering workflow...')
  action_response = requests.post(action_url, json=data, headers=git_hed)
  print(action_response)
  print('Workflow Triggered.')
 else:        
  print('Scheduled Time: ' + data_json[key]['work_start'])
  print('Phase state: ' + data_json[key]['phase_state'])
  print('This CR does not meet trigger Condition, Skipping..')
