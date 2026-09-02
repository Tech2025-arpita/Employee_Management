'''
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Department
from .serializers import DeptSerializer

@api_view(['GET'])
def get_departments(request):
    departments = Department.objects.all()
    serializer = DeptSerializer(departments,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_department(request):
    serializer = DeptSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def department_detail(request,id):
    try:
        department = Department.objects.get(id=id)
    except Department.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method =='GET':
        serializer=DeptSerializer(department)
        return Response(serializer.data)

    elif request.method =='PUT':
        serializer=DeptSerializer(department,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(
            {
                "message": "Method not allowed"
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
'''
'''
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import Department
from .serializers import DeptSerializer

class DepartmentListCreateView(ListCreateAPIView):
    queryset=Department.objects.all()
    serializer_class=DeptSerializer
    # def get(self, request, *args, **kwargs):
    #     print(self.serializer_class)
    #     return super().get(request, *args, **kwargs)

class DepartmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset=Department.objects.all()
    serializer_class=DeptSerializer
'''
# from rest_framework.generics import GenericAPIView
# from rest_framework import mixins
# from rest_framework.response import Response
# from .models import Department
# from .serializers import DeptSerializer
# from rest_framework import status

# class DepartmentListCreateView(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     GenericAPIView
# ):
#     queryset=Department.objects.all()
#     serializer_class=DeptSerializer

#     def get(self,request,*args,**kwargs):
#         # print(request.query_params)

#         deptid=request.query_params.get('deptid')
#         deptname=request.query_params.get('deptname')

#         allowed_params = [
#             "deptid",
#             "deptname"
#         ]

#         for param in request.query_params:
#             if param not in allowed_params:
#                 return Response(
#                     {
#                         "message": "Invalid Parameter"
#                     },
#                     status=400
#                 )
#         if deptid:
#             queryset=self.get_queryset().filter(id=deptid)
                    
#         elif deptname:
#             queryset=self.get_queryset().filter(name=deptname)
            
#         else:
#             queryset=self.get_queryset()

#         if not queryset.exists():
#             return Response(
#                 {
#                 "message":"No department found matching your search criteria."
#                 },status=404
#             )
    
#         serializer=self.get_serializer(queryset,many=True)

#         return Response(serializer.data)

#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

#         # name = request.data.get("name").strip()

#         # for department in Department.objects.all():
#         #     if department.name.strip() == name:
#         #         return Response(
#         #             {
#         #                 "message": "Department already exists."
#         #             },
#         #             status=400
#         #         )

#         # return self.create(request, *args, **kwargs)


# class DepartmentUpdateView(
#     mixins.UpdateModelMixin,
#     GenericAPIView,
# ):
#     queryset=Department.objects.all()
#     serializer_class=DeptSerializer

#     def put(self,request,*args,**kwargs):
#         return self.update(request, *args, **kwargs)
            
    
# class DepartmentDestroyView(
#     mixins.DestroyModelMixin,
#     GenericAPIView
# ):
#     queryset=Department.objects.all()
#     serializer_class=DeptSerializer

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework.response import Response
from .models import Department
from .serializers import DeptSerializer
from rest_framework import status
from .elastic_search import es,save_department_elasticsearch,create_department_index
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class DepartmentListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Department.objects.all()
    serializer_class=DeptSerializer

    def get(self,request,*args,**kwargs):
        deptid=request.query_params.get('deptid')
        deptname=request.query_params.get('deptname')

        allowed_params = [
            "deptid",
            "deptname"
        ] 

        for param in request.query_params:
            if param not in allowed_params:
                return Response({
                    "Invalid Parameter"
                },status=400
                )
            
        if deptid:
            result = es.search(
                index="departments",
                body={
                    "query": {
                        "term": {
                            "id": deptid
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
                        "message": "No department id found matching your search criteria."
                    },
                    status=404
                )

            return Response(data)

        elif deptname:
            result = es.search(
                    index="departments",
                    body={
                        "query": {
                        "term": {   #term--> means exactly match with the given output  
                                                #Jemon: deptname jodi hoy "HR", mool database-eo "HR"-i thakte hobe, "hr" ba 
                                                # "Human Resource" hole cholbe na
                            "name": deptname

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
                        "message": "No department name found matching your search criteria."
                    },status=404
                )
            
            return Response(data)
        
        # elif deptname:
        #   queryset=self.get_queryset().filter(name=deptname)
            
        else:
          queryset=self.get_queryset()

        # if not queryset.exists():
        #     return Response(
        #         {
        #        "message":"No department found matching your search criteria."
        #        },status=404
        #     )
    
        serializer=self.get_serializer(queryset,many=True)

        return Response(serializer.data)


    def post(self, request, *args, **kwargs):

        response = self.create(request, *args, **kwargs)

        if response.status_code == 201:
            
            create_department_index() 
            department = Department.objects.get(
                id=response.data["id"]
            )

            save_department_elasticsearch(department)

        return response

class DepartmentUpdateView(
    mixins.UpdateModelMixin,
    GenericAPIView,
 ):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Department.objects.all()
    serializer_class=DeptSerializer

    def put(self,request,*args,**kwargs):
        kwargs['partial'] = True
        response = self.update(request, *args, **kwargs)
      
        if response.status_code == 200:
            department = Department.objects.get(
                id=kwargs["pk"]
            )

            save_department_elasticsearch(department)

        return response


class DepartmentDestroyView(
    mixins.DestroyModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Department.objects.all()
    serializer_class=DeptSerializer

    def delete(self,request,*args,**kwargs):
        department_id = kwargs["pk"]
        response=self.destroy(request,*args,**kwargs)

        if response.status_code == 204:
            try:
                es.delete(index="departments", id=str(department_id))
            except Exception as e:
                    print(f"Delete failed: {e}")
            return Response(
                    {
                        "message": "Department successfully deleted ."
                    },
                    status=204
                )
        
        return response





