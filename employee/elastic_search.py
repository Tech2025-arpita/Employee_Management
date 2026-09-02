from django.conf import settings
from elasticsearch import Elasticsearch
es = Elasticsearch(
    settings.ELASTICSEARCH_HOST
)
INDEX_NAME = "employees"

def create_employee_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)

#save Employee
def save_employee_elasticsearch(employee):

    personal_details = None

    if hasattr(employee, "personal_details"):

        personal_details = {
            "address": employee.personal_details.address,
            "phone_number": employee.personal_details.phone_number,
            "zip_code": employee.personal_details.zip_code,

            "country": {
                "id": employee.personal_details.country.country_id,
                "name": employee.personal_details.country.name
            }
        }
    es.index(
        index=INDEX_NAME,
        id=employee.id,
        document={
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "dob": str(employee.dob),

            "department": {
                "id": employee.department.id,
                "name": employee.department.name
            },

            "salary": float(employee.salary),
            "personal_details": personal_details
        }
    )