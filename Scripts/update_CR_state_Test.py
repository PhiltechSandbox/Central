import json
import sys
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

now = datetime.now()

auth_token = sys.argv[1]
hed = {'Authorization': 'Basic ' + auth_token}

# Reading from file
with open("change_info.json", "r") as f:
     change_data = json.load(f)

#print(change_data)
for key in change_data:
 starttime=datetime.strptime(change_data[key]['work_start'], '%Y-%m-%d %H:%M:%S')
 if now-timedelta(minutes=20) <= starttime < now+timedelta(minutes=20):    
  print(key)
  print('---------------')
  print('Getting Phase State of CR ' + key + ' from ServiceNow')
  get_url = 'https://safewayqa1.service-now.com/api/now/table/change_request?sysparm_query=number%3D' + key + '&sysparm_display_value=true&sysparm_exclude_reference_link=true&sysparm_fields=number%2Cphase_state&sysparm_limit=1'
  response = requests.get(get_url, headers=hed)
  data = response.json()
  phase_state = data['result'][0]['phase_state']
  print('Current Phase State: "' + phase_state + '", Updating CR info file...')
  change_data[key]['phase_state'] = phase_state

#print(change_data)
with open("change_info.json", "w") as f:
     json.dump(change_data, f,indent=2)
