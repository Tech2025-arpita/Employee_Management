# from django_filters import rest_framework as filters
# from .models import Employees

# class EmpFieldFilterView(filters.FilterSet):
#     # exact_name=filters.CharFilter(field_name='name',lookup_expr='exact')
#     # iexact_name=filters.CharFilter(field_name='name',lookup_expr='iexact')

#     # exact_email=filters.CharFilter(field_name='email',lookup_expr='exact')
#     # iexact_email=filters.CharFilter(field_name='email',lookup_expr='iexact')

#     # start_name=filters.CharFilter(field_name='name',lookup_expr='startswith')
#     # istart_name=filters.CharFilter(field_name='name',lookup_expr='istartswith')
#     class Meta:
#         model=Employees
#         fields={
#             "name":['exact','iexact','contains','icontains','startswith','istartswith'],
#             "email":['exact','iexact'],
#             "dob":["exact","in","range","gt","lt","gte","lte","year"],
#             "salary":["exact","in","range","gt","lt","gte","lte"],
#         }

from django.db.models import Q
from .models import Employees

def employee_filter(request_data,queryset):
    filterquery = Q()

    if "name_exact"in request_data:
        filterquery &= Q(name__exact=request_data['name_exact'])

    if "name_iexact" in request_data:
        filterquery &=Q(name__iexact=request_data['name_iexact'])

   
    if 'name_contains' in request_data:
        filterquery &= Q(name__contains=request_data['name_contains'])


    if 'name_icontains' in request_data:
        filterquery &= Q(name__icontains=request_data['name_icontains'])

    if 'name_startswith' in request_data:
        filterquery &= Q(name__startswith=request_data['name_startswith'])

    if 'name_istartswith' in request_data:
        filterquery &= Q(name__istartswith=request_data['name_istartswith'])



    #email
    if "email_exact" in request_data:
        filterquery &= Q(email__exact=request_data["email_exact"])

    if "email_iexact" in request_data:
        filterquery &= Q(email__iexact=request_data["email_iexact"])



    #DOB
    if 'dob_exact' in request_data:
        filterquery &= Q(dob__exact=request_data['dob_exact'])

    if 'dob_in' in request_data:
        dob_list = request_data['dob_in'].split(',')
        filterquery &= Q(dob__in=dob_list)

    if 'dob_range' in request_data:
        start_date, end_date = request_data['dob_range'].split(',')
        filterquery &= Q(dob__range=(start_date, end_date))

    if 'dob_gt' in request_data:
            filterquery &= Q(dob__gt=request_data['dob_gt'])

    if 'dob_lt' in request_data:
        filterquery &= Q(dob__lt=request_data['dob_lt'])

    # if 'dob_date' in request_data:
    #     filterquery &= Q(dob__year=request_data['dob_date'])

    if 'dob_gte' in request_data:
        filterquery &= Q(dob__gte=request_data['dob_gte'])

    if 'dob_lte' in request_data:
        filterquery &= Q(dob__lte=request_data['dob_lte'])

    if 'dob_year' in request_data:
        filterquery &= Q(dob__year=request_data['dob_year'])


    #salary
    if 'salary_exact' in request_data:
        filterquery &= Q(salary__exact=request_data['salary_exact'])

    if 'salary_in' in request_data:
        salary_list = request_data['salary_in'].split(',')
        filterquery &= Q(salary__in=salary_list)

    if 'salary_range' in request_data:
        start_salary, end_salary = request_data['salary_range'].split(',')
        filterquery &= Q(salary__range=(start_salary, end_salary))

    if 'salary_gt' in request_data:
        filterquery &= Q(salary__gt=request_data['salary_gt'])

    if 'salary_lt' in request_data:
        filterquery &= Q(salary__lt=request_data['salary_lt'])

    if 'salary_gte' in request_data:
        filterquery &= Q(salary__gte=request_data['salary_gte'])

    if 'salary_lte' in request_data:
        filterquery &= Q(salary__lte=request_data['salary_lte'])

    return queryset.filter(filterquery)