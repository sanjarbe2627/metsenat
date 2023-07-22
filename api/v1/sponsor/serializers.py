from django.db.models import Sum
from rest_framework import serializers

from api.v1.base.utils.validators import validate_phone_number
from senat.models import Sponsor, Sponsorship, Student


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"


class SponsorStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['pk', 'fullname']


class SponsorshipSponsorSerializer(serializers.ModelSerializer):
    student = SponsorStudentSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Sponsorship
        fields = ['id', 'student', 'money', 'created_at']


class SponsorListCreateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=13, validators=[validate_phone_number]
    )
    money = serializers.IntegerField(min_value=0)
    spent_money = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Sponsor
        fields = [
            "id", "sponsor_type", "fullname", "phone_number", "money", "company_name", "status", "spent_money",
            "created_at"
        ]

    def validate_company_name(self, value):
        if self.initial_data.get('sponsor_type') == Sponsor.SponsorType.JURIDICAL:
            return self.initial_data.get('company_name')

        return ""

    @staticmethod
    def get_spent_money(sponsor):
        spent_money = sponsor.sponsorship.aggregate(money_sum=Sum('money'))
        return spent_money['money_sum'] or 0


class SponsorDetailUpdateSerializer(serializers.ModelSerializer):
    sponsorships = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Sponsor
        fields = [
            "id", "sponsor_type", "fullname", "phone_number", "money", "company_name", "status", "sponsorships",
            "created_at"
        ]

    @staticmethod
    def get_spent_money(sponsor):
        spent_money = sponsor.sponsorship.aggregate(money_sum=Sum('money'))
        return spent_money['money_sum']

    @staticmethod
    def get_sponsorships(sponsor):
        print("sponsor=", sponsor)
        serializer = SponsorshipSponsorSerializer(sponsor.sponsorship.all(), many=True)
        return serializer.data
