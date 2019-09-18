import json
import boto3
import os
from datetime import datetime, tzinfo
# import pytz

# utc=pytz.UTC

BUCKET = os.environ['S3_BUCKET']
LOG_LEVEL = os.environ['LOG_LEVEL']
TTL_HOURS = os.environ['TTL_HOURS']

s3 = boto3.resource('s3')

bucket = s3.Bucket(BUCKET)

def conv_secs_to_hours(seconds):
    return seconds/60/60

def should_delete(last_modified, ttl):
    now = datetime.utcnow()
    # print(f'\tnow - ts > ttl   {now} - {last_modified} > {ttl}')
    diff = now.replace(tzinfo=None) - last_modified.replace(tzinfo=None)
    diffseconds = diff.total_seconds()
    diffhours = conv_secs_to_hours(diffseconds)
    # print(f'\tdiff hours: {diffhours}')
    return diffhours > int(ttl)

def handler(event, context):
    print(event)
    object_summary_iterator = bucket.objects.all()
    print('')
    things_to_delete = []
    for item in object_summary_iterator:
        print(item)
        # print(f'\tlast_modified: {item.last_modified}')
        yesno = should_delete(item.last_modified, TTL_HOURS)
        print(f'\tshould delete? {yesno}')
        if yesno:
            print(f'deleting {item.key} from {item.bucket_name}')
            item.delete()
