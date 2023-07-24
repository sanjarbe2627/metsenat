from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.dashboard import serializers


class DashboardView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        dashboard_money = serializers.DashboardMoneySerializer()
        dashboard_day_count = serializers.DashboardDayCountSerializer()
        return Response({
                'result': {
                    'moneys': dashboard_money.result,
                    'counts':  dashboard_day_count.result.get('days')
                }
             }, status=status.HTTP_200_OK)
