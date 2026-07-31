from rest_framework import serializers
from .models import Employees, PersonalDetails
from rest_framework.validators import UniqueValidator
from department.serializers import DeptSmallSerializer
from department.models import Department
from country.models import Country
from country.serializers import CountrySmallSerializer

class PersonalDetailsSerializer(serializers.ModelSerializer):
    country=CountrySmallSerializer(read_only=True)
    # countryid = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),source="country",write_only=True)
    employee_id  = serializers.IntegerField(source="employee.id", read_only=True)
    employee_name = serializers.CharField(source="employee.name", read_only=True)
    phone_number=serializers.CharField(max_length=15,validators=[UniqueValidator(
            queryset=PersonalDetails.objects.all(),
            message="This Phone Number is Already Exists")
        ])
    class Meta:
        model = PersonalDetails
        fields = [
            "id",
            "employee_id",
            "employee_name",
            "address",
            "phone_number",
            "zip_code",
            "country",
            # "country_id"
            # "countryid"
        ]

class EmpSerializer(serializers.ModelSerializer):
    
    department = DeptSmallSerializer(read_only=True)
    # department_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Department.objects.all(),
    #     source="department",
    #     write_only=True
    # )
    personal_details = serializers.SerializerMethodField(read_only=True)
    # personal_details = PersonalDetailsSerializer(required=False)

    email=serializers.EmailField(
        max_length=100,validators=[UniqueValidator(queryset=Employees.objects.all(),
                                                   message="This Name is Already Exists")])
    
    def get_personal_details(self, obj):
        if PersonalDetails.objects.filter(employee=obj.id).exists():
            return PersonalDetailsSerializer(PersonalDetails.objects.filter(employee=obj.id).first()).data

    # def get_personal_details(self, obj):
    #     personal_details = PersonalDetails.objects.filter(employee=obj).first()
    #     if personal_details:
    #         return PersonalDetailsSerializer(personal_details).data

    #     return None

    class Meta:
        model = Employees
        fields = [
            "id",
            "name",
            "email",
            "dob",
            "department",
            # "department_id",
            "salary",
            "personal_details",
            "createdby",
            "createddate",
            "updatedby",
            "updateddate",
        ]
        extra_kwargs = {
            "id": {
                "read_only": True
            },
            "createdby": {
                "read_only": True
            },
            "createddate": {
                "read_only": True
            },
            "updatedby": {
                "read_only": True
            },
            "updateddate": {
                "read_only": True
            }
        }
    def create(self, validated_data):
        personal_data = self.initial_data.get('personal_details')
        department_id = self.initial_data.get('department') 
        dept_instance = Department.objects.get(id=department_id)
        country_instance = Country.objects.get(country_id=personal_data["country"])

        print(validated_data)
        employee = Employees.objects.create(
            name=validated_data["name"],
            email=validated_data["email"],
            dob=validated_data.get("dob"),
            department=dept_instance,
            salary=validated_data.get('salary'),
            createdby=validated_data.get("createdby"),
            updatedby=validated_data.get("updatedby")
        )

        PersonalDetails.objects.create(
            employee=employee,
            address=personal_data.get("address"),
            phone_number=personal_data.get("phone_number"),
            zip_code=personal_data.get("zip_code"),
            country=country_instance,
            createdby=personal_data.get("createdby"),
            updatedby=personal_data.get("updatedby")
        )
        employee.refresh_from_db()
        return employee
    
    def update(self, instance, validated_data):
        # print(self.context['request'].data)
        personal_data = self.initial_data.get("personal_details", None)
        print("Personal Details: ", personal_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if personal_data is not None:
            personal_details_instance, _ = PersonalDetails.objects.get_or_create(employee=instance)
            if "country" in personal_data:
                country_id = personal_data.pop("country")
                personal_details_instance.country = Country.objects.get(country_id=country_id)
            for attr, value in personal_data.items():
                setattr(personal_details_instance, attr, value)
            personal_details_instance.save()
        return instance


