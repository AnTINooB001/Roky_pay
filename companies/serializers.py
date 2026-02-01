from rest_framework import serializers
from . import models as comp_models

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=comp_models.Companies
        fields='__all__'