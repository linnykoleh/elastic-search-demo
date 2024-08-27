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
