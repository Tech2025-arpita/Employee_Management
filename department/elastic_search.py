from django.conf import settings
from elasticsearch import Elasticsearch

es=Elasticsearch(
    settings.ELASTICSEARCH_HOST
)

INDEX_NAME="departments"

def create_department_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)

#To save department
def save_department_elasticsearch(department):
    es.index(
        index="departments",
        id=department.id,
        document={
            "name":department.name
        }
    )
