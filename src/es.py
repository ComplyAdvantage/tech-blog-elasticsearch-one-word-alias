from elasticsearch import Elasticsearch

INDEX = "entities"

ES_CLIENT = Elasticsearch(
    "http://elasticsearch:9200",
    timeout=600, retry_on_timeout=True
)
