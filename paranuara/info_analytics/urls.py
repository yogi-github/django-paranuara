from django.urls import re_path

from info_analytics.views import GetPeoplePerCompany, GetCommonFriends, GetFavouriteFood

app_name = 'info_analytics'

urlpatterns = [
    re_path(r'^get-people/company/(?P<company_id>\d+)$', GetPeoplePerCompany.as_view(), name='info-analytics.get-people'),
    re_path(r'^common-friends/(?P<first_person>\d+)/(?P<second_person>\d+)$', GetCommonFriends.as_view(), name='info-analytics.common-friends'),
    re_path(r'^person-food/(?P<person_id>\d+)$', GetFavouriteFood.as_view(),name='info-analytics.person-food'),

]
