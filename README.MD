# Index & Autocomplete with Elasticsearch

## 1. Create docker-compose.yml

```yaml
version: '3.7'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.10
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - esdata:/usr/share/elasticsearch/data
    networks:
      - esnet

  kibana:
    image: docker.elastic.co/kibana/kibana:7.17.10
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    networks:
      - esnet

volumes:
  esdata:
    driver: local

networks:
  esnet:
    driver: bridge
```

## 2. Run Elasticsearch and Kibana

```bash
docker-compose up -d
```

## 3. Create Index

```bash
curl -X PUT "localhost:9200/autocomplete_index?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "analysis": {
      "filter": {
        "autocomplete_filter": {
          "type":     "edge_ngram",
          "min_gram": 2,
          "max_gram": 20
        }
      },
      "analyzer": {
        "autocomplete": {
          "type":      "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "autocomplete_filter"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "suggest_field": {
        "type": "text",
        "analyzer": "autocomplete",
        "search_analyzer": "standard"
      }
    }
  }
}
'
```

## 4. Add Data to Index autocomplete_index

```bash
from elasticsearch import Elasticsearch, helpers

# Initialize the Elasticsearch client
es = Elasticsearch(
    hosts=[{
        'host': 'localhost',
        'port': 9200,
        'scheme': 'http'
    }]
)

def generate_data(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            yield {
                "_index": "autocomplete_index",
                "_source": {
                    "suggest_field": word
                }
            }

helpers.bulk(es, generate_data('words.txt'))

print("Bulk insert complete.")
```

## 5. Search Data #1
 
### I will search for the word "machene" spelled incorrectly.

```bash
curl -X GET "localhost:9200/autocomplete_index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "suggest_field": {
        "query": "machene",
        "fuzziness": "AUTO",
        "prefix_length": 1,
        "max_expansions": 50
      }
    }
  }
}
'
```

### Here is a result:

```json
{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 218,
      "relation" : "eq"
    },
    "max_score" : 22.795536,
    "hits" : [
      {
        "_index" : "autocomplete_index",
        "_type" : "_doc",
        "_id" : "fHluk5EBsBz0T2DqCFED",
        "_score" : 22.795536,
        "_source" : {
          "suggest_field" : "Machetes"
        }
      },
      {
        "_index" : "autocomplete_index",
        "_type" : "_doc",
        "_id" : "pXluk5EBsBz0T2DqCFED",
        "_score" : 22.795536,
        "_source" : {
          "suggest_field" : "machineable"
        }
      },
      {
        "_index" : "autocomplete_index",
        "_type" : "_doc",
        "_id" : "qXluk5EBsBz0T2DqCFED",
        "_score" : 22.795536,
        "_source" : {
          "suggest_field" : "machined"
        }
      },
      {
        "_index" : "autocomplete_index",
        "_type" : "_doc",
        "_id" : "rnluk5EBsBz0T2DqCFED",
        "_score" : 22.795536,
        "_source" : {
          "suggest_field" : "machineful"
        }
      },
      {
        "_index" : "autocomplete_index",
        "_type" : "_doc",
        "_id" : "tHluk5EBsBz0T2DqCFED",
        "_score" : 22.795536,
        "_source" : {
          "suggest_field" : "machineless"
        }
      },
      {
        "_index" : "autocomplete_index",
        "_type" : "_doc",
        "_id" : "tXluk5EBsBz0T2DqCFED",
        "_score" : 22.795536,
        "_source" : {
          "suggest_field" : "machinely"
        }
      },
      {
        "_index" : "autocomplete_index",
        "_type" : "_doc",
        "_id" : "tnluk5EBsBz0T2DqCFED",
        "_score" : 22.795536,
        "_source" : {
          "suggest_field" : "machinelike"
        }
      },
      {
        "_index" : "autocomplete_index",
        "_type" : "_doc",
        "_id" : "uHluk5EBsBz0T2DqCFED",
        "_score" : 22.795536,
        "_source" : {
          "suggest_field" : "machineman"
        }
      },
      {
        "_index" : "autocomplete_index",
        "_type" : "_doc",
        "_id" : "uXluk5EBsBz0T2DqCFED",
        "_score" : 22.795536,
        "_source" : {
          "suggest_field" : "machinemen"
        }
      },
      {
        "_index" : "autocomplete_index",
        "_type" : "_doc",
        "_id" : "u3luk5EBsBz0T2DqCFED",
        "_score" : 22.795536,
        "_source" : {
          "suggest_field" : "machinemonger"
        }
      }
    ]
  }
}
```

## 5. Search Data #2

```bash
curl -X GET "localhost:9200/autocomplete_index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "suggest_field": {
        "query": "oleh",
        "fuzziness": "AUTO",
        "prefix_length": 1,
        "max_expansions": 50
      }
    }
  }
}
'
```

### Here is a result:

```json
{
  "took": 4,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 246,
      "relation": "eq"
    },
    "max_score": 27.968891,
    "hits": [
      {
        "_index": "autocomplete_index",
        "_type": "_doc",
        "_id": "Hnluk5EBsBz0T2DqC_7Z",
        "_score": 27.968891,
        "_source": {
          "suggest_field": "Oletha"
        }
      },
      {
        "_index": "autocomplete_index",
        "_type": "_doc",
        "_id": "H3luk5EBsBz0T2DqC_7Z",
        "_score": 27.968891,
        "_source": {
          "suggest_field": "Olethea"
        }
      },
      {
        "_index": "autocomplete_index",
        "_type": "_doc",
        "_id": "IHluk5EBsBz0T2DqC_7Z",
        "_score": 27.968891,
        "_source": {
          "suggest_field": "Olethreutes"
        }
      },
      {
        "_index": "autocomplete_index",
        "_type": "_doc",
        "_id": "IXluk5EBsBz0T2DqC_7Z",
        "_score": 27.968891,
        "_source": {
          "suggest_field": "olethreutid"
        }
      },
      {
        "_index": "autocomplete_index",
        "_type": "_doc",
        "_id": "Inluk5EBsBz0T2DqC_7Z",
        "_score": 27.968891,
        "_source": {
          "suggest_field": "Olethreutidae"
        }
      },
      {
        "_index": "autocomplete_index",
        "_type": "_doc",
        "_id": "sn9uk5EBsBz0T2DqSesa",
        "_score": 27.968891,
        "_source": {
          "suggest_field": "Oletha"
        }
      },
      {
        "_index": "autocomplete_index",
        "_type": "_doc",
        "_id": "s39uk5EBsBz0T2DqSesa",
        "_score": 27.968891,
        "_source": {
          "suggest_field": "Olethea"
        }
      },
      {
        "_index": "autocomplete_index",
        "_type": "_doc",
        "_id": "tH9uk5EBsBz0T2DqSesa",
        "_score": 27.968891,
        "_source": {
          "suggest_field": "Olethreutes"
        }
      },
      {
        "_index": "autocomplete_index",
        "_type": "_doc",
        "_id": "tX9uk5EBsBz0T2DqSesa",
        "_score": 27.968891,
        "_source": {
          "suggest_field": "olethreutid"
        }
      },
      {
        "_index": "autocomplete_index",
        "_type": "_doc",
        "_id": "tn9uk5EBsBz0T2DqSesa",
        "_score": 27.968891,
        "_source": {
          "suggest_field": "Olethreutidae"
        }
      }
    ]
  }
}
```

