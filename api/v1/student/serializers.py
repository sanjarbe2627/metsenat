from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError

from api.v1.base.utils.validators import validate_phone_number
from senat.models import University, Student, Sponsorship, Sponsor


class StudentUniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"


class StudentSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ["pk", "fullname", "phone_number", "sponsor_type", "company_name"]


class StudentSponsorshipSerializer(serializers.ModelSerializer):
    sponsor = StudentSponsorSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Sponsorship
        fields = ["pk", "sponsor", "money", "created_at"]


class StudentSerializer(serializers.ModelSerializer):
    contract = serializers.IntegerField(min_value=0)
    phone_number = serializers.CharField(max_length=13, validators=[validate_phone_number])
    paid_money = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Student
        fields = [
            "pk", "fullname", "phone_number", "university", "student_type", "contract", "paid_money", "created_at"
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.university:
            representation['university'] = {
                'id': instance.university.id,
                'name': instance.university.name
            }
        return representation

    @staticmethod
    def get_paid_money(student):
        paid_sum = student.sponsorship.aggregate(money_sum=Coalesce(Sum('money'), 0))
        return paid_sum['money_sum']


class StudentDetailUpdateSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=100, required=False)
    phone_number = serializers.CharField(
        max_length=13, validators=[validate_phone_number], required=False
    )
    paid_money = serializers.SerializerMethodField(read_only=True)
    sponsorships = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Student
        fields = [
            "pk", "fullname", "phone_number", "university", "student_type", "contract",
            "paid_money", "sponsorships", "created_at"
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.university:
            representation['university'] = {
                'id': instance.university.id,
                'name': instance.university.name
            }
        return representation

    @staticmethod
    def get_sponsorships(student):
        sponsorship = StudentSponsorshipSerializer(student.sponsorship.all(), many=True)
        return sponsorship.data

    @staticmethod
    def get_paid_money(student):
        paid_sum = student.sponsorship.aggregate(money_sum=Coalesce(Sum('money'), 0))
        return paid_sum['money_sum']

    def validate_contract(self, contract):
        paid_money = self.get_paid_money(self.instance)
        if (paid_money - self.instance.contract + contract) > self.instance.contract:
            raise ValidationError(_("The money exceeded the contract amount"))

        return contract
