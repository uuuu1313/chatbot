from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import FineTunedModel, TrainingData
from .serializers import FineTunedModelSerializer, TrainingDataSerializer


# Create your views here.

@api_view(['GET'])
def hello_world(request):
    return Response('Hellow, World!@')

# 각 클래스는 viewsets.ModelViewSet을 상속받음
class FineTunedModelViewSet(viewsets.ModelViewSet): # FineTunedModel 모델에 대한 CRUD API 엔드포인트 제공 뷰셋
    permission_classes = (IsAuthenticated,)         # 인증된 사용자만 접근 가능
    queryset = FineTunedModel.objects.all()         # FineTunedModel의 모든 객체를 가져옴
    serializer_class = FineTunedModelSerializer     # 뷰셋에서 사용할 Serializer 클래스를 정의

class TrainingDataViewSet(viewsets.ModelViewSet):   # TrainingData 모델에 대한 CRUD API 엔드포인트 제공 뷰셋
    permission_classes = (IsAuthenticated,)         # 인증된 사용자만 접근 가능
    queryset = TrainingData.objects.all()           # TrainingData 모델의 모든 객체를 가져옴
    serializer_class = TrainingDataSerializer       # 뷰셋에서 사용할 Serializer 클래스를 정의