import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
class OpsmanClient:
    def __init__(self, host, ops_user, ops_password, client_user, client_password):
        self.host = host
        self.ops_user = ops_user
        self.ops_password = ops_password
        self.client_user = client_user
        self.client_password = client_password
        self.token = self.get_uaa_token()

    #---------------available_products----------------------
    def upload_tile(self, file_path):
        files = {'product[file]': open(file_path, 'r')}
        r = requests.post(
            self.api_uri("/api/v0/available_products"),
            files=files,
            verify=False,
            headers=self.get_headers()
        )
        return r.json()

    def list_available_products(self):
        r = requests.get(
            self.api_uri("/api/v0/available_products"),
            verify=False,
            headers = self.get_headers()
        )
        return r.json()

    def delete_available_product(self, name, version):
        headers = self.get_headers()
        headers["Content-Type"] = "application/json"
        r = requests.delete(
            self.api_uri("/api/v0/available_products?product_name={}&version={}".format(name, version)),
            verify=False,
            headers=self.get_headers()
        )
        return r.status_code
    #---------------staged products---------------------------
    def stage_product(self, name, product_version):
        r = requests.post(
            self.api_uri("/api/v0/staged/products?name={}&product_version={}".format(name, product_version)),
            verify=False,
            headers=self.get_headers()
        )
        return r.json()

    def list_staged_products(self):
        r = requests.get(
            self.api_uri("/api/v0/staged/products"),
            verify=False,
            headers=self.get_headers()
        )
        return r.json()

    def list_staged_product_properties(self, product_guid):
        r = requests.get(
            self.api_uri("/api/v0/staged/products/{}/properties".format(product_guid)),
            verify=False,
            headers=self.get_headers()
        )
        return r.json()

    def fill_staged_product_properties(self, product_guid, propertiesJson):
        headers = self.get_headers()
        headers["Content-Type"] = "application/json"
        r = requests.put(
            self.api_uri("/api/v0/staged/products/{}/properties".format(product_guid)),
            verify=False,
            data = propertiesJson,
            headers=headers
        )
        return r.status_code
    def get_staged_product_id_by_name(self, product_name):
        products = self.list_staged_products()
        return self.find_product_guid_by_name(products, product_name)
    def delete_staged_product(self, product_guid):
        headers = self.get_headers()
        headers["Content-Type"] = "application/json"
        r = requests.delete(
            self.api_uri("/api/v0/staged/products/{}".format(product_guid)),
            verify=False,
            headers=self.get_headers(),
            data = {}
        )
        return r.status_code

    #----------------deployed products------------------------
    def list_deployed_products(self):
        r = requests.get(
            self.api_uri("/api/v0/deployed/products"),
            verify=False,
            headers=self.get_headers()
        )
        return r.json()

    def get_deployed_product_id_by_name(self, product_name):
        products = self.list_deployed_products()
        return self.find_product_guid_by_name(products, product_name)

    #----------------installation-----------------------------
    def apply_change(self):
        headers = self.get_headers()
        headers["Content-Type"] = "application/json"
        r = requests.post(
            self.api_uri("/api/v0/installations"),
            verify=False,
            data = {},
            headers=headers
        )
    #-------------------HELPERS-------------------------
    def api_uri(self, api_endpoint):
        return "{}{}".format(self.host, api_endpoint)

    def get_uaa_token(self):
        payload = {"grant_type":"password", "username": self.ops_user,"password": self.ops_password}
        r = requests.post(
            self.api_uri("/uaa/oauth/token"),
            verify=False,
            data = payload,
            auth=(self.client_user, self.client_password)
        )
        return r.json()['access_token']

    def get_headers(self):
        return {'Authorization': 'Bearer {}'.format(self.token)}

    def find_product_guid_by_name(self, products, product_name):
        for product in products:
            if product['type'].lower() == product_name.lower():
                return product['guid']
        return ""
