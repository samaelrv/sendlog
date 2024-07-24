import requests
import time

unique_id ='sid001'
SPLUNK_API_URL = "https://localhost:8089/services/search/jobs"
USERNAME = ""
PASSWORD = ""
splunk_query = 'search index="order_api_dev"'
DYNATRACE_URL = "https://{environment}.live.dynatrace.com/api/v2/logs/ingest"
DYNATRACE_API_TOKEN = ""

post_data = { 'id' : unique_id,
              'max_count' : '200',
              'search' : splunk_query,
              'earliest_time' : '-24h',
              'latest_time' : 'now'
            }
splunk_search_base_url = 'https://localhost:8089/servicesNS/{}/search/search/jobs'.format(USERNAME)
resp = requests.post(splunk_search_base_url , data=post_data , verify=False ,auth=(USERNAME,PASSWORD))
print(resp.text)

is_job_completed =''

while(is_job_completed != 'DONE'):
    time.sleep(5)
    get_data = {'output_mode': 'json'}
    job_status_base_url = 'https://localhost:8089/servicesNS/{}/search/search/jobs/{}'.format(USERNAME,unique_id)
    resp_job_status = requests.post(job_status_base_url, data=get_data ,verify=False ,auth=(USERNAME,PASSWORD))
    resp_job_status_data = resp_job_status.json()
    is_job_completed = resp_job_status_data['entry'][0]['content']['dispatchState']
    print("Current Job Status is {}".format(is_job_completed))

splunk_summary_base_url = 'https://localhost:8089/servicesNS/{}/search/search/jobs/{}/results'.format(USERNAME,unique_id)
splunk_summary_results = requests.get(splunk_summary_base_url,data=get_data ,verify=False ,auth=(USERNAME,PASSWORD))
splunk_summary_data = splunk_summary_results.json()

#for data in splunk_summary_data['results']:
   # print(data)

headers = {
    'Authorization': f'Api-Token {DYNATRACE_API_TOKEN}',
    'Content-Type': 'application/json'
}
response = requests.post(DYNATRACE_URL, headers=headers, json=splunk_summary_data)
response.raise_for_status()
print("Logs successfully sent to Dynatrace")

