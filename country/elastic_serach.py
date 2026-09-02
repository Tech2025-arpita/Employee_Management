from django.conf import settings
from elasticsearch import Elasticsearch 

es=Elasticsearch(
    settings.ELASTICSEARCH_HOST
)

INDEX_NAME="country"

def create_country_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)

#To save country
def save_country_elasticsearch(country):
    es.index(
        index="country",
        id=country.id,
        document={
            "name":country.name
        }
    )
