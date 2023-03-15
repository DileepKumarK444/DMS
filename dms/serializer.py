from rest_framework import serializers
from masters.models import CustomerUser, PlanReport

class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'

class PlanReportSerializer(serializers.ModelSerializer):

    class Meta:

        # 'log__plan__plan','log__plan__project__project_name','log__plan__plan_date','log__plan__start_time','log__plan__end_time'
        model = PlanReport
        fields = '__all__'
        depth = 3

# class ReportSerializer(serializers.ModelSerializer):

#     class Meta:

#         # 'log__plan__plan','log__plan__project__project_name','log__plan__plan_date','log__plan__start_time','log__plan__end_time'
#         model = PlanReport
#         fields = '__all__'
#         depth = 3