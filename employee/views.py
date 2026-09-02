# '''
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Employees,PersonalDetails
# from .serializers import PersonalDetailsSerializer,EmpSerializer

# @api_view(['GET'])
# def get_employess(request):
#     emps = Employees.objects.all()
#     serializer = EmpSerializer(emps,many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def create_employees(request):
#     serializer = EmpSerializer(data=request.data, context={"data": request.data})
#     if serializer.is_valid():
#         employee = serializer.save()
#         return Response(EmpSerializer(employee).data,status=status.HTTP_201_CREATED)
#     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def employee_detail(request,id):
#     try:
#         emps = Employees.objects.get(id=id)
#     except Employees.DoesNotExist:
#         return Response({
#             "message":"Employee Not Found"
#         },status=status.HTTP_404_NOT_FOUND)
    
#     if request.method =='GET':
#         serializer=EmpSerializer(emps)
#         return Response(serializer.data)

#     elif request.method =='PUT':
#         serializer=EmpSerializer(emps,data=request.data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         emps.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     else:
#         return Response(
#             {
#                 "message": "Method not allowed"
#             },
#             status=status.HTTP_405_METHOD_NOT_ALLOWED
#         )
# '''
# # from rest_framework.generics import (
# #     ListCreateAPIView,
# #     RetrieveUpdateDestroyAPIView
# # )
# # from .models import Employees,PersonalDetails
# # from .serializers import PersonalDetailsSerializer,EmpSerializer
# # from rest_framework.response import Response

# # class EmployeeListCreateView(ListCreateAPIView):
# #     queryset=Employees.objects.all()
# #     serializer_class=EmpSerializer

# #     def get_serializer_context(self):
# #         context= super().get_serializer_context()
# #         context.update({
# #             'data':self.request.data
# #         })
# #         return context

# # class EmployeeDetailView(RetrieveUpdateDestroyAPIView):
# #     queryset=Employees.objects.all()
# #     serializer_class=EmpSerializer

# #     def get_serializer_context(self):
# #         context=super().get_serializer_context()
# #         context.update({
# #             'data':self.request.data
# #         })
# #         return context
# #     def update(self,request,*args,**kwargs):
# #         kwargs['partial']=True
# #         return super().update(request,*args,**kwargs)

# from rest_framework import mixins
# from rest_framework.generics import GenericAPIView
# from rest_framework.response import Response  
# from .serializers import PersonalDetailsSerializer,EmpSerializer
# from .filters import employee_filter
# from django_filters.rest_framework import DjangoFilterBackend

# from .models import PersonalDetails,Employees
# from rest_framework import status


# class EmpListCreateView(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     GenericAPIView,
# ):
#     queryset=Employees.objects.all()
#     serializer_class=EmpSerializer
#     # filter_backends=[DjangoFilterBackend]
#     # filterset_class=[EmpFieldFilterView]

#     def get(self,request,*args,**kwargs):
#             # print(request.query_params)
#             queryset = self.get_queryset()
#             emp_id=request.query_params.get('emp_id')
#             emp_name=request.query_params.get('emp_name')

#             allowed_params = [
#                 "emp_id",
#                 "emp_name",
#                 "name_exact",
#                 "name_iexact",
#                 "name_contains",
#                 "name_icontains",
#                 "name_startswith",
#                 "name_istartswith",

#                 #Email 
#                 "email_exact",
#                 "email_iexact",

#                 #DOB 
#                 "dob_exact",
#                 "dob_in",
#                 "dob_range",
#                 "dob_gt",
#                 "dob_lt",
#                 "dob_gte",
#                 "dob_lte",
#                 "dob_year",

#                 #Salary 
#                 "salary_exact",
#                 "salary_in",
#                 "salary_range",
#                 "salary_gt",
#                 "salary_lt",
#                 "salary_gte",
#                 "salary_lte",
#                 "dob_date"
#             ]
            
#             for param in request.query_params:
#                 if param not in allowed_params:
#                     return Response(
#                         {
#                             "message":"Invalid Parameter"
#                         },status=400
#                     )
#             queryset = employee_filter(request.query_params, queryset)

#             if emp_id:
#                 queryset=queryset.filter(id=emp_id)
                            
#             elif emp_name:
#                 queryset=queryset.filter(name=emp_name)

#             else:
#                 queryset=self.get_queryset()

#             if not queryset.exists():
#                 return Response(
#                     {
#                     "message":"No Employee found matching your search criteria."
#                     },status=404
#                 )
#             serializer=self.get_serializer(queryset,many=True)
#             return Response(serializer.data)
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

# class EmployeeUpdateView(
#     mixins.UpdateModelMixin,
#     GenericAPIView,
# ):
#     queryset=Employees.objects.all()
#     serializer_class=EmpSerializer
#     # filter_backends=[DjangoFilterBackend]
#     # filterset_class=EmpFieldFilterView]
    
#     def put(self,request,*args,**kwargs):
#         kwargs['partial']=True
#         return self.update(request,*args,**kwargs)
    
# class EmpDeleteView(
#     mixins.DestroyModelMixin,
#     GenericAPIView,
# ):
#     queryset=Employees.objects.all()
#     serializer_class=EmpSerializer

#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)

#Here from PersonalDetails 

# class PersonalDetailsListCreateView(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     GenericAPIView,
# ):
#     queryset=PersonalDetails.objects.all()
#     serializer_class=PersonalDetailsSerializer

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

# class PersonalDetailsCompactView(
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     GenericAPIView,
# ):
#     queryset=PersonalDetails.objects.all()
#     serializer_class=PersonalDetailsSerializer

#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)

#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)

#     def patch(self,request,*args,**kwargs):
#         return self.partial_update(request,*args,**kwargs)

#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)
        

from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response  
from .serializers import PersonalDetailsSerializer,EmpSerializer
from .filters import employee_filter
from django_filters.rest_framework import DjangoFilterBackend

from .models import PersonalDetails,Employees
from rest_framework import status
from .elastic_search import es,save_employee_elasticsearch

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class EmpListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Employees.objects.all()
    serializer_class=EmpSerializer
    # filter_backends=[DjangoFilterBackend]
    # filterset_class=[EmpFieldFilterView]

    def get(self,request,*args,**kwargs):
            # print(request.query_params)
            queryset = self.get_queryset()
            emp_id=request.query_params.get('emp_id')
            emp_name=request.query_params.get('emp_name')

            allowed_params = [
                "emp_id",
                "emp_name",
                "name_exact",
                "name_iexact",
                "name_contains",
                "name_icontains",
                "name_startswith",
                "name_istartswith",

                #Email 
                "email_exact",
                "email_iexact",

                #DOB 
                "dob_exact",
                "dob_in",
                "dob_range",
                "dob_gt",
                "dob_lt",
                "dob_gte",
                "dob_lte",
                "dob_year",

                #Salary 
                "salary_exact",
                "salary_in",
                "salary_range",
                "salary_gt",
                "salary_lt",
                "salary_gte",
                "salary_lte",
                "dob_date"
            ]
            
            for param in request.query_params:
                if param not in allowed_params:
                    return Response(
                        {
                            "message":"Invalid Parameter"
                        },status=400
                    )
            queryset = employee_filter(request.query_params, queryset)

                        
            if emp_id:
                result = es.search(
                    index="employees",
                    body={
                        "query": {
                            "term": {
                                "id": emp_id
                            }
                        }
                    }
                )
                data=[]

                for hit in result["hits"]["hits"]:
                    data.append(
                        {
                            "id":hit["_id"],
                            **hit["_source"]
                        }
                    )
                if not data:
                    return Response(
                        {
                            "message": "No employee id found matching your search criteria."
                        },
                        status=404
                    )

                return Response(data)

            elif emp_name:
                result = es.search(
                        index="employees",
                        body={
                            "query": {
                            "match": {
                                "name": emp_name
                                }
                                }
                            }
                            )
                data=[]
                
                for hit in result["hits"]["hits"]:
                    data.append(
                        {
                            "id":hit["_id"],
                            **hit["_source"]
                        }
                        )
                if not data:
                    return Response(
                        {
                            "message": "No employee name found matching your search criteria."
                        },status=404
                    )
                
                return Response(data)
            
            # elif deptname:
            #   queryset=self.get_queryset().filter(name=deptname)
                
            else:
                queryset=self.get_queryset()
        
            serializer=self.get_serializer(queryset,many=True)

            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
    
        response = self.create(request, *args, **kwargs)
    
        if response.status_code == 201:
    
            employee = Employees.objects.get(
                id=response.data["id"]
            )
    
            save_employee_elasticsearch(employee)
    
        return response

class EmployeeUpdateView(
    mixins.UpdateModelMixin,
    GenericAPIView,
 ):
        authentication_classes=[JWTAuthentication]
        permission_classes=[IsAuthenticated]
        queryset=Employees.objects.all()
        serializer_class=EmpSerializer

        def put(self,request,*args,**kwargs):
            kwargs['partial'] = True
            response = self.update(request, *args, **kwargs)

            if response.status_code == 200:
                employee = Employees.objects.get(
                    id=kwargs["pk"]
                )

                save_employee_elasticsearch(employee)

            return response

class EmpDeleteView(
    mixins.DestroyModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Employees.objects.all()
    serializer_class=EmpSerializer

    def delete(self,request,*args,**kwargs):
        emp_id = kwargs["pk"]
        response=self.destroy(request,*args,**kwargs)

        if response.status_code == 204:
            try:
                es.delete(index="employees", id=str(emp_id))
            except Exception as e:
                    print(f"Delete failed: {e}")
            return Response(
                    {
                        "message": "Employee successfully deleted ."
                    },
                    status=204
                )
        
        return response





