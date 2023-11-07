import sys
import logging
import auth
import requests
import urllib.parse
from url import Url

logging.basicConfig(level=logging.INFO)

class PMC_Client():

    # Current version of the PMC API
    version = '/v2'

    # Allow users to specify a different url,
    # if not specified defualt to production PMC

    def __init__(self, key, key_id, client_url='https://console.parkmycloud.com'):
        self.url = Url(f'{client_url}')
        self.session = auth.login(key, key_id, self.url)

    # Customize the get request to iterate through
    # the total through multiple calls with limit and
    # offset defined

    def get(self, path):
        try:
            response = self.session.get(self.url + path)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        data = response.json()
        items = data.get("items")

        if not items:
            return data

        while (data.get('total') > (data.get('offset') + data.get('limit'))):
            offset = data.get('offset') + data.get('limit')
            response = self.session.get(self.url.next(path, offset))
            data = response.json()
            items.extend(data.get('items'))
        return items


    def post(self, path, payload):

        response = self.session.post(self.url + path, json=payload)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            return response.json()
        else:
            response.raise_for_status()

    def put(self, path, payload):
        response = self.session.put(self.url + path, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    ########             Credentials                   ########

    # Get All Credentials

    def get_creds(self):
        path = '/creds'
        body = self.get(path)
        return body.get('data')

    # Add GCP Credential

    def post_gcp_credential(self, name, default_ingest_team_id,
                            gcp_sa_key, gcp_project_id):
        path = '/creds'
        payload = {
            "name": name,
            "iam_cred_type": 'g_sa',
            "default_ingest_team_id": default_ingest_team_id,
            "provider_id": 2,
            "gcp_sa_key": gcp_sa_key,
            "gcp_project_id": gcp_project_id,
            "discoverable": True
        }
        return self.post(path, payload)

    # Update GCP Credential

    def update_gcp_credential(self, cred_id, name, default_ingest_team_id,
                            gcp_sa_key, gcp_project_id):
        path = f'/creds/{cred_id}'
        payload = {
            "name": name,
            "iam_cred_type": 'g_sa',
            "default_ingest_team_id": default_ingest_team_id,
            "provider_id": 2,
            "gcp_sa_key": gcp_sa_key,
            "gcp_project_id": gcp_project_id,
            "discoverable": True
        }
        return self.put(path, payload)


    # Post Azure Credential

    def post_azure_credential(self, name, default_ingest_team_id,
                            az_subscription_id, az_tenant_id,
                            az_client_id, az_client_secret,
                            az_offer_id=""):
        path = '/creds'
        payload = {
            "name": name,
            "iam_cred_type": 'az_sp',
            "default_ingest_team_id": default_ingest_team_id,
            "provider_id": 3,
            "az_subscription_id": az_subscription_id,
            "az_offer_id": az_offer_id,
            "az_tenant_id": az_tenant_id,
            "az_client_id": az_client_id,
            "az_client_secret": az_client_secret,
            "discoverable": True
        }

        return self.post(path, payload)

    ########             Policies                      ########

    # Get all policies

    def get_all_policies(self):
        path = '/creds'
        return self.get(path)
    ########             ResouceQuery                   ########

    # Return all resources defined in my scope

    def get_all_resources(self):
        path = self.version + '/resourcequery'
        return self.get(path)

    # Return all resources without a schedule in my scope

    def get_all_resources_without_schedule(self):
        path = self.version + '/resourcequery?schedule_name='
        return self.get(path)

    # Return all resources with a schedule in my scope

    def get_all_resources_with_schedule(self):
        path = self.version + '/resourcequery?schedule_name=-'
        return self.get(path)

    # Return all resources based a specific team

    def get_resources_by_team(self, team_id):
        url_encoded_team_id = urllib.parse.quote(team_id)
        path = self.version + f'/resourcequery?team_names={url_encoded_team_id}'
        return self.get(path)

    ########             Teams                   ########

    def get_teams(self, associated_only=False):
        path = self.version + f'/teams?associated_only={associated_only}'
        data = self.get(path)
        return data.get("teams")

    ########              Resources              ########

    def get_resource_tags(self, resource_id):
        path = self.version + f'/resource/{resource_id}/tags'
        return self.get(path)
