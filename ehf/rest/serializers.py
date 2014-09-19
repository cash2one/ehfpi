# our rest serializers
from browse.browse_view_models import allEHFPI
from rest_framework import serializers

class EhfpiSerializer(serializers.ModelSerializer):
     class Meta:
        model = allEHFPI
        #fields = ('id', 'title', 'code', 'linenos', 'language', 'style')