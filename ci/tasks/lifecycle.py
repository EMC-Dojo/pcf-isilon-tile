#!/usr/bin/env python
import opsman_client
from jinja2 import Environment, FileSystemLoader
import unittest
import os
import urllib
import create_tile

class Test(unittest.TestCase):
    def setUp(self):
        os.chdir('persistence-tile')
        ops_host = os.environ['OPSMAN_HOST']
        ops_user = os.environ['OPSMAN_USER']
        ops_password = os.environ['OPSMAN_PASSWORD']
        ops_client_id = os.environ['OPSMAN_CLIENT_ID']
        ops_client_secret = os.environ['OPSMAN_CLIENT_SECRET']
        self.tile_path = os.environ['OPSMAN_TILE_PATH']
        self.product_name = os.environ['OPSMAN_PROD_NAME']
        self.product_version = os.environ['OPSMAN_PROD_VERSION']
        self.broker_port = os.environ['BROKER_PORT']
        self.isilon_endpoint = os.environ['ISILON_ENDPOINT']
        self.isilon_username = os.environ['ISILON_USERNAME']
        self.isilon_password = os.environ['ISILON_PASSWORD']
        self.isilon_port = os.environ['ISILON_PORT']
        self.skip_cert_verify = os.environ['SKIP_CERT_VERIFY']
        self.ops_client = opsman_client.OpsmanClient(
            ops_host, ops_user, ops_password, ops_client_id, ops_client_secret
        )
        create_tile.main()

    def tearDown(self):
        prod_id = self.ops_client.get_deployed_product_id_by_name(self.product_name)
        self.ops_client.delete_staged_product(prod_id)
        install_id = self.ops_client.apply_change()
        self.ops_client.wait_for_installation(install_id)
        self.ops_client.delete_available_product(self.product_name, self.product_version)

    def test_tile_lifecycle(self):
        try:
            self.ops_client.upload_tile(self.tile_path)
            self.ops_client.stage_product(self.product_name, self.product_version)
            prod_id = self.ops_client.get_staged_product_id_by_name(self.product_name)
            prod_properties = self.generate_isilon_tile_properties()
            self.ops_client.update_product_networks(prod_id, "az1", "PCF-Private")
            self.ops_client.fill_staged_product_properties(prod_id, prod_properties)
            install_id = self.ops_client.apply_change()
            self.ops_client.wait_for_installation(install_id)
            self.assertEqual(self.ops_client.get_install_status(install_id), "succeeded")
        except ValueError as e:
            self.fail('get http error {}'.format(str(e)))


    def generate_isilon_tile_properties(self):
        template = self.get_template_file("properties.template.json")
        rendered = template.render(
            port=self.broker_port,
            isilon_endpoint=self.isilon_endpoint,
            isilon_username=self.isilon_username,
            isilon_password=self.isilon_password,
            isilon_port=self.isilon_port,
            skip_cert_verify=self.skip_cert_verify
        )
        return rendered

    def get_template_file(self, file_name):
        template_folder='ci/templates'
        env = Environment(loader=FileSystemLoader(template_folder))
        return env.get_template(file_name)

if __name__ == '__main__':
    unittest.main()
