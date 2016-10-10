#!/usr/bin/env python3

import os
import boto3
import requests
import shutil
from jinja2 import Environment, FileSystemLoader
from subprocess import call

def main():
    aws_client = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
        aws_secret_access_key=os.environ['AWS_SECRET_KEY']
    )
    libstorage_release_name=os.environ['LIBSTORAGE_RELEASE_NAME']
    persistence_release_name=os.environ['PERSISTENCE_RELEASE_NAME']
    routing_release_name=os.environ['ROUTING_RELEASE_NAME']
    download_s3_file(aws_client, 'libstorage', libstorage_release_name, libstorage_release_name)
    download_file(os.environ['PERSISTENCE_URI'], persistence_release_name)
    download_file(os.environ["ROUTING_URI"], routing_release_name)
    build_tile(libstorage_release_name, persistence_release_name, routing_release_name)

def download_s3_file(client, bucket, bucket_file, file_name):
    client.download_file(bucket, bucket_file, "releases/{}".format(file_name))

def download_file(release_uri, release_name):
    print("Downloading {}".format(release_name))
    r = requests.get(release_uri, stream=True)
    if r.status_code == 200:
        with open("releases/{}".format(release_name), 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def build_tile(libstorage_release_name, persistence_release_name, routing_release_name):
    template = get_template_file("persistence-broker.template.yml")
    rendered = template.render(
        libstorage_release_name=libstorage_release_name,
        persistence_release_name=persistence_release_name,
        routing_release_name=routing_release_name
    )
    cwd = os.getcwd()
    with open("metadata/persistence-broker.yml", 'w') as f:
        f.write(rendered)

    tile_name='persistence-storage.pivotal'
    call(['zip', '-r', tile_name, 'metadata/', 'releases/'])

    return os.path.join(cwd, tile_name)

def get_template_file(file_name):
    template_folder='ci/templates'
    env = Environment(loader=FileSystemLoader(template_folder))
    return env.get_template(file_name)

if __name__ == '__main__':
    main()
