from pmc_client import PMC_Client
import csv
import json
import os

key_id = input("Enter your API Key ID: ")
key = input("Enter your API Private Key: ")

pmc = PMC_Client(key, key_id, 'https://console.parkmycloud.com')

team_name = input("Enter Default Team (cloud credential resources will be associated with team)")
teams = pmc.get_teams()
team = next((team for team in teams if team.get('name') == team_name), None)

if(team is None):
     raise SystemExit(f'Team with name {team_name} could not be found')

team_id = team.get('id')


# open file in read mode
with open('azure_service_principals.csv', 'r') as read_obj:
    # pass the file object to DictReader() to get the DictReader object
    csv_dict_reader = csv.DictReader(read_obj)
    # iterate over each line as a ordered dictionary
    for azure_sp in csv_dict_reader:
        # row variable is a dictionary that represents a row in csv
        print(azure_sp)
        azure_sp['provider_id'] = 3
        azure_sp['iam_cred_type'] = "az_sp"
        azure_sp['default_ingest_team_id'] = team_id
        azure_sp['discoverable'] = True

        response = pmc.post_azure_credential(azure_sp.get('name'),
                        team_id,
                        azure_sp.get('az_subscription_id'),
                        azure_sp.get('az_tenant_id'),
                        azure_sp.get('az_client_id'),
                        azure_sp.get('az_client_secret'))
        print(response)
