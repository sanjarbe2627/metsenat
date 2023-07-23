from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError

from api.v1.base.utils.validators import validate_phone_number
from api.v1.student.serializers import StudentUniversitySerializer
from senat.models import Sponsor, Sponsorship, Student


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"


class SponsorStudentSerializer(serializers.ModelSerializer):
    university = StudentUniversitySerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['pk', 'fullname', 'phone_number', 'university']


class SponsorSponsorshipSerializer(serializers.ModelSerializer):
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
            return value

        return ""

    @staticmethod
    def get_spent_money(sponsor):
        spent_money = sponsor.sponsorship.aggregate(money_sum=Coalesce(Sum('money'), 0))
        return spent_money['money_sum']


class SponsorDetailUpdateSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=100, required=False)
    phone_number = serializers.CharField(max_length=13, validators=[validate_phone_number], required=False)
    spent_money = serializers.SerializerMethodField(read_only=True)
    sponsorships = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Sponsor
        fields = [
            "id", "sponsor_type", "fullname", "phone_number", "money", "spent_money", "company_name", "status",
            "sponsorships", "created_at"
        ]

    @staticmethod
    def get_spent_money(sponsor):
        spent_money = sponsor.sponsorship.aggregate(money_sum=Coalesce(Sum('money'), 0))
        return spent_money['money_sum']

    @staticmethod
    def get_sponsorships(sponsor):
        serializer = SponsorSponsorshipSerializer(sponsor.sponsorship.all(), many=True)
        return serializer.data

    def validate_money(self, money):
        spent_money = self.get_spent_money(self.instance)
        if (spent_money - self.instance.money + money) > self.instance.money:
            raise ValidationError(_("The money spent exceeded the sponsorship amount"))
        return money


# for Sponsorship model
class SponsorshipSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['pk', 'fullname', 'phone_number']


class SponsorshipSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Sponsorship
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sponsor'] = SponsorshipSponsorSerializer(instance.sponsor, many=False).data
        representation['student'] = SponsorStudentSerializer(instance.student, many=False).data
        return representation

    def validate_money(self, money):
        request = self.context['request']
        sponsor = Sponsor.objects.get(pk=self.initial_data.get('sponsor'))
        student = Student.objects.get(pk=self.initial_data.get('student'))

        spent_money = sponsor.sponsorship.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        paid_money = student.sponsorship.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']

        if request.method != 'POST':
            spent_money -= self.instance.money
            paid_money -= self.instance.money

        if (sponsor.money - spent_money) < money:
            raise ValidationError(_("Sponsor's account does not have this amount of money. The rest of the money"))
        else:
            if (student.contract - paid_money) < money:
                raise ValidationError(_("Sponsorship money exceeded the contract amount!"))

        return money
