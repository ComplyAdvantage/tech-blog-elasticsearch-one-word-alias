import json
import time

from elasticsearch.helpers import bulk
from elastic_transport import ConnectionError

from es import ES_CLIENT, INDEX
from entity import entity_builder

def wait_for_cluster():
    print("Waiting for cluster availability")
    max_wait_seconds = 60
    wait_for_seconds = 5
    for time_left in range(max_wait_seconds, -wait_for_seconds, -wait_for_seconds):
        try:
             ES_CLIENT.cat.health()
             return
        except ConnectionError as e:
            time.sleep(wait_for_seconds)
            if time_left <= 0:
                raise e

if __name__ == "__main__":

    wait_for_cluster()

    ES_CLIENT.indices.delete(
        index=INDEX,
        ignore=404,
    )

    with open("src/mapping.json", "r") as f:
        mapping = json.load(f)

    print("Creating index")
    ES_CLIENT.indices.create(
        index=INDEX,
        mappings=mapping,
        ignore=400,
    )

    print("Indexing entity documents")
    bulk(ES_CLIENT, entity_builder)

    print("Finished setup")
