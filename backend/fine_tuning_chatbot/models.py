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

    def __str__(self):
        return self.model_name

class TrainingData(models.Model):
    fine_tuned_model = models.ForeignKey(FineTunedModel, on_delete=models.CASCADE, related_name='training_data')
    # relate_name은 FineTuneModel 객체에서 TrainingData 객체에 접근할 때 사용할 역참조 이름을 정의

    prompt = models.TextField()
    completion = models.TextField()

    def __str__(self):
        return f"{self.fine_tuned_model.model_name}의 훈련 데이터"