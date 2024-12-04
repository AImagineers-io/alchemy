from django.contrib import admin
from .models import User, Document, ProcessedData, TransformationLog, APIRequestLog, TaskLog, QAPair

admin.site.register(User)
admin.site.register(Document)
admin.site.register(ProcessedData)
admin.site.register(TransformationLog)
admin.site.register(APIRequestLog)
admin.site.register(TaskLog)
admin.site.register(QAPair)