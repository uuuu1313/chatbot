from django.contrib import admin
from .models import FineTunedModel, TrainingData

# Register your models here.

@admin.register(FineTunedModel)
class FineTunedModelAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'base_name')
    search_fields = ('model_name', 'base_name')

@admin.register(TrainingData)
class TrainingDataAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'completion', 'fine_tuned_model', 'is_fine_tuned', 'will_be_fine_tuned')
    # list_display 튜플은 TrainingData 모델에대한 Django admin의 목록 보기에서 표기할 필드 정의
    search_fields = ('prompt', 'completion', 'fine_tuned_model__model_name')
    # search_fields 튜플은 Django admin 인터페이스에서 검색 상자를 사용할때 검색 할 필드
    list_filter = ('fine_tuned_model', 'is_fine_tuned', 'will_be_fine_tuned')
    # list_filter 튜플은 Django admin 인터페이스에서 사용할 수 있는 필터를 정의
