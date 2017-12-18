from pymongo import MongoClient
from elasticsearch import Elasticsearch
from pprint import pprint
import click
import json
import time
from bson import json_util
con = MongoClient('localhost', 24075)
db = con.oilbirddb_v5

es = Elasticsearch(
    ["http://fdd40cc6fe83a5bc8e41670d9f7afaa5.eu-west-1.aws.found.io:9200"])


@click.command()
@click.option('--es_index', help='Enter input collection name')
@click.option('--es_doc_type', help='Enter input collection name')
@click.option('--field1', default=None, help='Enter input field1')
@click.option('--field2', default=None, help='Enter input field2')
@click.option('--field3', default=None, help='Enter input field3')
def update_in_es(es_index, es_doc_type, field1, field2, field3):
    input_fields = []
    input_fields.append(field1)
    input_fields.append(field2)
    input_fields.append(field3)
    input_fields = filter(None, input_fields)


    all_data = c2.find(no_cursor_timeout=True)
    for document in all_data:
        search_query = {
            "query": {"match": {input_field: document[input_field]}}}
        try:
            d = {}
            for ip in input_fields:
                d.update({ip: document.get(ip, '')})

            update_query = {"doc": d}

            es_data = es.search(
                index=es_index,
                doc_type=es_doc_type,
                body=search_query)
            _id = es_data['hits']['hits'][0]['_id']
            es.update(
                index=es_index,
                doc_type=es_doc_type,
                id=_id, body=update_query)
        except Exception as e:
            print e


if __name__ == "__main__":
    update_in_es()
