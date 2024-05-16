from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class FineTunedModel(models.Model): # 클래스 명이 DB에 담길 테이블 명이 됨
    MODEL_CHOICES = [
        ('ada', 'Ada'),
        ('babbage', 'Babbage'),
        ('curie', 'Curie'),
        ('davinci', 'Davinci'),
    ]

    model_name = models.CharField(max_length=100)                       # 필드명이 테이블안의 컬럼명이 됨
    base_name = models.CharField(max_length=100, choices=MODEL_CHOICES) # 필드명이 테이블안의 컬럼명이 됨
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fine_tuned_models', null=True)
    # related_name은 역참조시 사용 ex) data = user.fine_tuned_models.all()
    file_id = models.CharField(max_length=200, null=True, blank=True) # OpenAi API가 반환하는 파일 ID 저장
    fine_tune_id = models.CharField(max_length=200, null=True, blank=True) # OpenAI API가 반환하는 ID 저장
    fine_tuned_model = models.CharField(max_length=200, null=True, blank=True) # OpenAI API가 반환하는 세부 조정된 모델 식별자
    status = models.CharField(max_length=50, null=True, blank=True) # 프로세스의 상태 저장(processing, complete, failed)

    def __str__(self):
        return self.model_name

class TrainingData(models.Model):
    fine_tuned_model = models.ForeignKey(FineTunedModel, on_delete=models.CASCADE, related_name='training_data')
    # relate_name은 FineTuneModel 객체에서 TrainingData 객체에 접근할 때 사용할 역참조 이름을 정의
    prompt = models.TextField()
    completion = models.TextField()
    is_fine_tuned = models.BooleanField(default=False) # 훈련 데이터가 세부조정에 사용 되었는지 여부
    will_be_fine_tuned = models.BooleanField(default=False) # 훈련 데이터가 나중에 모델의 세부 조정에 사용될지 여부
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_datas', null=True)

    def __str__(self):
        return f"{self.fine_tuned_model.model_name}의 훈련 데이터"