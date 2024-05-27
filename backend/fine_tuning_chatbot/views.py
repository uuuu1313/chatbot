import json
import os

import openai
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
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

# fintuned_model_id를 이용하여 TrainingData 객체를 검색하고 JSON 형식으로 파일 저장
def create_and_save_jsonl(finetuned_model_id):  # 인자는 finetuned_model_id를 받는다
    training_data = TrainingData.objects.filter(fine_tuned_model_id=finetuned_model_id) # TrainingData 모델에서 fine_tuned_model_id가 일치하는 모든 객체를 필터링하고 변수에 저장함

    file_name = f"fine_tuned_model_{finetuned_model_id}.jsonl" # 파일 이름 생성
    with open(file_name, 'w') as f: # w 모드로 해당 파일들을 연다
        for data in training_data:
            f.write(json.dumps({'prompt': data.prompt + '\n', 'completion': data.completion + '\n'}))
            f.write('\n')

        return file_name, training_data


# JSON Lines 형식으로 변환한 파일을 생성하고 API뷰에 반환
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def convert_jsonl_file(request, finetuned_model_id):
    try:
        FineTunedModel.objects.get(id=finetuned_model_id) # finetuned_model_id가 존재하지 않으면 FineTunedModel.DoesNotExsist 예외 발생

        file_name, training_data = create_and_save_jsonl(finetuned_model_id)

        file_info = os.stat(file_name) # 생성된 파일의 정보를 가져옴

        # 응답으로 보낼 JSON 객체 생성
        response = {
            'file_name' : file_name,
            'lines' : len(training_data),
            'file_size' : file_info.st_size,
        }
        return JsonResponse(response)

    except FineTunedModel.DoesNotExist:
        return JsonResponse({'error': 'FineTunedModel with the given id does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_jsonl_file(request, finetuned_model_id):
    try:
        finetuned_model = FineTunedModel.objects.get(id=finetuned_model_id)

        file_name, _ = create_and_save_jsonl(finetuned_model_id)

        with open(file_name, 'rb') as file:
            openai.api_key = settings.OPENAI_API_KYE
            result = openai.File.create(file=file, purpose='fine-tune')

        finetuned_model.file_id = result['id']
        finetuned_model.save()

        if default_storage.exsist(file_name):
            default_storage.delete(file_name)

        return JsonResponse(result)

    except FineTunedModel.DoesNotExist:
        return JsonResponse({'error': 'FineTunedModel with the given id does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_finetune(request, finetuned_model_id):
    try:
        finetuned_model = FineTunedModel.objects.get(id=finetuned_model_id)

        openai.api_key = settings.OPEN_API_KEY
        result = openai.FineTune.create(
            model = finetuned_model.base_model,
            training_file = finetuned_model.file_id,
        )

        finetuned_model.fine_tune_id = result['id']
        finetuned_model.save()

        return JsonResponse(result)

    except FineTunedModel.DoesNotExist:
        return JsonResponse({'error': 'FineTunedModel with the given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def retrieve_finetune(request, finetuned_model_id):
    try:
        finetuned_model = FineTunedModel.objects.get(id=finetuned_model_id)

        openai.api_key = settings.OPEN_API_KEY
        fine_tune_id = finetuned_model.fine_tune_id

        result = openai.FineTune.retrieve(id=fine_tune_id)

        finetuned_model.status = result['status']
        finetuned_model.fine_tuned_model = result['fine_tuned_model']
        finetuned_model.save()

        return JsonResponse(result)

    except FineTunedModel.DoesNotExist:
        return JsonResponse({'error': 'FineTunedModel with the given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









