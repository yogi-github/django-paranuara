from rest_framework import status
from rest_framework.views import APIView

from helpers.app_response import AppResponse
from helpers.custom_paginator import AppPaginator
from info_analytics.models import Person, Company
from info_analytics.serializers import PeoplePagedSerializer, CommonFriendsSerializer, FavouriteFoodSerializer
from info_analytics.view_models import PeopleViewModel, CommonFriendsViewModel, FavouriteFoodViewModel


class GetPeoplePerCompany(APIView):

    def get(self, request, company_id):

        try:
            company = Company.objects.get(id=company_id)

        except Company.DoesNotExist as ex:
            return AppResponse(status=status.HTTP_400_BAD_REQUEST, message=str(ex))

        args = request.query_params
        page_size = int(args.get('page_size', 0))
        page_number = int(args.get('page_number', 1))

        people = Person.objects.filter(company=company).order_by('name')
        people_list, num_people = AppPaginator(people, page_size, page_number).paginate_objects()
        vm = PeopleViewModel(people=people_list, num_people=num_people)
        serializer = PeoplePagedSerializer(vm)

        return AppResponse(status=status.HTTP_200_OK, data=serializer.data)


class GetCommonFriends(APIView):

    def get(self, request, first_person, second_person):

        try:
            first_person = Person.objects.get(id=first_person)
            second_person = Person.objects.get(id=second_person)

        except Person.DoesNotExist as ex:
            return AppResponse(status=status.HTTP_400_BAD_REQUEST, message=str(ex))

        vm = CommonFriendsViewModel(first_person, second_person)
        serializer = CommonFriendsSerializer(vm)

        return AppResponse(status=status.HTTP_200_OK, data=serializer.data)


class GetFavouriteFood(APIView):

    def get(self, request, person_id):

        try:
            person = Person.objects.get(id=person_id)

        except Person.DoesNotExist as ex:
            return AppResponse(status=status.HTTP_400_BAD_REQUEST, message=str(ex))

        vm = FavouriteFoodViewModel(person)
        serializer = FavouriteFoodSerializer(vm)

        return AppResponse(status=status.HTTP_200_OK, data=serializer.data)
