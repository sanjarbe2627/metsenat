from django.db.models import Sum, Count
from django.db.models.functions import Coalesce, TruncDate

from senat.models import Sponsorship, Student, Sponsor


class DashboardMoneySerializer:
    def __init__(self):
        self.spent_money = Sponsorship.objects.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        self.contract_money = Student.objects.aggregate(money_sum=Coalesce(Sum('contract'), 0))['money_sum']
        self.need_money = self.contract_money - self.spent_money

    @property
    def result(self):
        return self.__dict__


class DashboardDayCountSerializer:
    def __init__(self):
        student_days = Student.objects.annotate(date=TruncDate('created_at')).values('date').annotate(
            count=Count('id')).order_by('date')
        sponsor_days = Sponsor.objects.annotate(date=TruncDate('created_at')).values('date').annotate(
            count=Count('id')).order_by('date')

        days = {}
        for student in student_days:
            days[student['date']] = {
                'date': student['date'],
                'sponsor_count': 0,
                'student_count': student['count']
            }
        for sponsor in sponsor_days:
            if sponsor['date'] in days:
                days[sponsor['date']]['sponsor_count'] = sponsor['count']
            else:
                days[sponsor['date']] = {
                    'date': sponsor['date'],
                    'student_count': 0,
                    'sponsor_count': sponsor['count']
                }
        self.days = sorted(days.values(), key=lambda x: x['date'])

    @property
    def result(self):
        return self.__dict__
