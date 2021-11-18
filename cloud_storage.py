import os
from os import listdir
from os.path import isfile, join
from pprint import pprint
from google.cloud import storage

credential_path = 'E:\Project\VideoStore\ServiceKey_GoogleCloud.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

storage_client = storage.Client()

#dir(storage_client)

bucket_name = 'cloud_storage_bucket'

# create a new bucket
bucket = storage_client.bucket(bucket_name)
bucket.storage_class = 'COLDLINE' # Archive | Nearline | Standard
bucket.location = 'US' 
bucket = storage_client.create_bucket(bucket) 

pprint(vars(bucket))

bucket.name
bucket._properties['selfLink']
bucket._properties['id']
bucket._properties['location']
bucket._properties['timeCreated']
bucket._properties['storageClass']
bucket._properties['timeCreated']
bucket._properties['updated']

"""
Get Bucket
"""
my_bucket = storage_client.get_bucket(bucket_name)
#pprint(vars(my_bucket))

"""
Upload File
"""
def upload_to_bucket(blob_name, file_path, bucket_name):
    '''
    Upload file to a bucket
    : blob_name  (str) - object name
    : file_path (str)
    : bucket_name (str)
    '''
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)
    return blob

mypath = 'E:\Project\VideoStore'

#onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath, f))]
#print(onlyfiles)

for f in listdir(mypath):
    if isfile(join(mypath, f)):
        bucketpath = 'videos/'+f
        response = upload_to_bucket(bucketpath, join(mypath, f), bucket_name)


"""
Download File By Blob Name
"""
def download_file_from_bucket(blog_name, file_path, bucket_name):
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blog_name)
    with open(file_path, 'wb') as f:
        storage_client.download_blob_to_file(blob, f)
    print('Saved')

download_file_from_bucket('videos/ab-03-08-2021-20-30-46.avi', os.path.join(mypath, 'ab-03-08-2021-20-30-46.avi'), bucket_name)


"""
List Buckets
list_buckets(max_results=None, page_token=None, prefix=None, projection='noAcl', fields=None, project=None, timeout=60, retry=<google.api_core.retry.Retry object>)
"""
for bucket in storage_client.list_buckets(max_results=100):
    print(bucket)