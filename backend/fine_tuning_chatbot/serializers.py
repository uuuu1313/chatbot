from rest_framework import serializers
from .models import FineTunedModel, TrainingData


class FineTunedModelSerializer(serializers.ModelSerializer): # Serializer는 모델과 JSON 데이터간의 직렬화와 역직렬화를 수행
    class Meta:
        model = FineTunedModel
        fields = ['id', 'model_name', 'base_model']

class TrainingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingData
        fields = ['id', 'fine_tuned_model', 'prompt', 'completion', 'is_fine_tuned', 'will_be_fine_tuned']
