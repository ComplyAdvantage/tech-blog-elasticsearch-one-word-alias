# Elasticsearch for Reference Text Screening
A companion repository to the blog "Four Concepts to Get Started with Elasticsearch". It builds an example Elasticsearch cluster that can be used to test queries.

## Getting Started
After cloning the repository, build the Elasticsearch index with:
```bash
docker compose run setup
```

This will create a set of fake entity documents and index these to Elasticsearch. After, you can query the cluster with the examples in the companion blog. If you have already indexed the documents, you can start the cluster with `docker compose up -d`.

## Next Steps
Feel free to experiment with the [index mapping](src/mapping.json) and the [generated data](src/entity.py) to learn more about Elasticsearch. The [official documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-with-elasticsearch.html) is a useful resource.
