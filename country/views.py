
'''
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Country
from .serializers import countrySerializer

@api_view(['GET'])
def get_countries(request):
    countries = Country.objects.all()
    serializer = countrySerializer(countries,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_countries(request):
    serializer = countrySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET','PUT','DELETE'])
def countries_detail(request,id):
    try:
        countries = Country.objects.get(country_id=id)
    except Country.DoesNotExist:
        return Response({
            "message":"Country Not Found"
        },status=status.HTTP_400_BAD_REQUEST)
    
    if request.method =='GET':
        serializer=countrySerializer(countries)
        return Response(serializer.data)

    elif request.method =='PUT':
        serializer=countrySerializer(countries,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        countries.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(
            {
                "message": "Method not allowed"
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
'''

# from rest_framework.generics import (
#     ListCreateAPIView,
#     RetrieveUpdateDestroyAPIView
# )
# from .models import Country
# from .serializers import countrySerializer

# class CountryListCreateView(ListCreateAPIView):
#     queryset=Country.objects.all()
#     serializer_class=countrySerializer

# class CountryDetailsView(RetrieveUpdateDestroyAPIView):
#     queryset=Country.objects.all()
#     serializer_class=countrySerializer


from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework.response import Response
from .models import Country
from .serializers import countrySerializer
from rest_framework import status

class CountryListCreate(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    queryset=Country.objects.all()
    serializer_class=countrySerializer

    def get(self,request,*args,**kwargs):
        country_id=request.query_params.get('country_id')
        country_name=request.query_params.get('country_name')

        allowed_params = [
            "country_id",
            "country_name"
            ]
        
        for param in request.query_params:
            if param not in allowed_params:
                return Response(
                    {
                        "message": "Invalid Parameter"
                    },
                    status=400
                )
            
        if country_id:
            queryset=self.get_queryset().filter(country_id=country_id)

        elif country_name:
            queryset=self.get_queryset().filter(name=country_name)

        # elif request.query_params:
        #     return Response(
        #         {
        #             "message":"Invalid Parameter"
        #         },status=400
        #     )
        else:
            queryset=self.get_queryset()

        if not queryset.exists():
            return Response({
                "message":"No Country found matching your search criteria."
            },status=404
            )
        
        serializer=self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class CountryUpdateView(
    mixins.UpdateModelMixin,
    GenericAPIView,
):
    queryset=Country.objects.all()
    serializer_class=countrySerializer
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    

class CountryDeleteiew(
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    queryset=Country.objects.all()
    serializer_class=countrySerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



