from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_permissions',
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__ (self):
        return self.email

class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    source_name = models.CharField(max_length=255, null=True)
    publication_date = models.DateField(null=True)
    file_type = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)
    unstructured_data = models.TextField(null=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return self.file_name
    
class ProcessedData(models.Model):
    data_id = models.AutoField(primary_key=True)
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    structured_data = models.JSONField(null=True)
    processed_date = models.DateTimeField(auto_now_add=True)
    storage_location = models.CharField(max_length=50, default='Local')

    def __str__(self):
        return f"Data for Document ID: {self.document.document_id}"

class TransformationLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    transformation_step = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transformation Log for Document ID: {self.document.document_id}"

class APIRequestLog(models.Model):
    request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_endpoint = models.CharField(max_length=255)
    request_timestamp = models.DateTimeField(auto_now_add=True)
    response_status = models.CharField(max_length=50)

    def __str__(self):
        return f"API Request by User: {self.user.email} on {self.request_timestamp}"