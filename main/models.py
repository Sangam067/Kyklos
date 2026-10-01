from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class StudentManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('credit_score', 0)
        user = self.create_user(username, email, password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Hostel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Student(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    interest = models.CharField(max_length=255, blank=True, null=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="students", null=True, blank=True)
    credit_score = models.IntegerField(default=0)
    location = models.CharField(max_length=100, blank=True, default='')
    
    objects = StudentManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} (Score: {self.credit_score})"

class Warden(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="warden", null=True, blank=False)
    gmail = models.CharField(max_length=300)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"Warden {self.username} ({self.hostel.name if self.hostel else 'No Hostel'})"

class Discussion(models.Model):
    topic = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    content = models.TextField()
    category = models.TextField()
    username = models.CharField(max_length=150)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.title} - by {self.username}"

class Resource(models.Model):
    thumbnail = models.ImageField(upload_to="images/")
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=150)
    resourceurl = models.CharField(max_length=1000)
    username = models.CharField(max_length=300)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.title} ({self.category})"

class Complaint(models.Model):
    roomno = models.CharField(max_length=10)
    studentname = models.CharField(max_length=100)
    priority = models.CharField(max_length=50)
    complaint_type = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='complaints/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hostelid = models.IntegerField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Complaint by {self.studentname} - {self.complaint_type}"

