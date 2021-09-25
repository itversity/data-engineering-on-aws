import boto3, os


def get_marker_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table('ghmarker')


def get_marker(marker_table, key):
    item = marker_table.get_item(Key={'tn': key})
    if item.get('Item'):
        marker_item = item['Item']
    else:
        baseline_marker = os.environ.get('BASELINE_SINCE')
        status = 'SUCCESS'
        marker_item = {
            'tn': key,
            'marker': baseline_marker,
            'status': status
        }
        marker_table.put_item(Item=marker_item)
    return marker_item


def update_marker(marker_table, key, marker, status):
    marker_item = get_marker(marker_table, key)
    marker_item['marker'] = marker
    marker_item['status'] = status
    marker_table.put_item(Item=marker_item)
    return marker
