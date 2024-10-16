from django.contrib import admin
from .models import User, Document, ProcessedData, TransformationLog, APIRequestLog

admin.site.register(User)
admin.site.register(Document)
admin.site.register(ProcessedData)
admin.site.register(TransformationLog)
admin.site.register(APIRequestLog)
