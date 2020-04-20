from rest_framework import serializers

from info_analytics.models import Person


class PeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('id', 'name', 'age', 'email', 'address', 'phone', 'has_died')


class PeoplePagedSerializer(serializers.Serializer):

    people = PeopleSerializer(many=True)
    num_people = serializers.IntegerField()


class CommonFriendsSerializer(serializers.Serializer):

    first_person = PeopleSerializer()
    second_person = PeopleSerializer()
    common_friends = PeopleSerializer(many=True)


class FavouriteFoodSerializer(serializers.Serializer):

    username = serializers.CharField()
    age = serializers.IntegerField()
    fruits = serializers.ListField(child=serializers.CharField())
    vegetables = serializers.ListField(child=serializers.CharField())