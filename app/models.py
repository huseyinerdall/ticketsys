import os
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models import Count
from django.db.models import Q

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,username=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            username=email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    department = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_superuser = models.BooleanField(default=False) # a superuser
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to ='user/')
    title = models.CharField(max_length=100,blank=True,null=True)
    bio = models.TextField()

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return str(self.id)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_manager(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    symbol = models.FileField(upload_to ='uploads/')
    created_at = models.DateTimeField(default=timezone.now)
    members = models.ManyToManyField(User, related_name='department_members')

class Attachment(models.Model):
    file = models.FileField(upload_to ='uploads/')

    def __str__(self):
        return str(self.file)

    def get_filename(self):
        return os.path.basename(str(self.file))

    def get_ext(self):
        return  self.get_filename().split(".")[-1]

class CommentManager():
    def add_comment(self, ticket_id,comment, **extra_fields):
        ticket = Ticket.model(comment=comment)
        ticket.save()
        print(ticket,**extra_fields)
        return commentsm

class Comment(models.Model):
    user = models.ForeignKey(User,related_name='comment_owner',on_delete=models.PROTECT)
    comment = models.TextField(blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    objects = CommentManager()

    def __str__(self):
        return str(self.comment)



class Ticket(models.Model):

    type_options = (
        ('1', 'Epic'),
        ('2', 'Bug'),
        ('3', 'Task'),
        ('4', 'Subtask'),
        ('5', 'Change'),
        ('6', 'IT help'),
        ('7', 'Incident'),
        ('8', 'New feature'),
        ('9', 'Problem'),
        ('10', 'Service request'),
        ('11', 'Support'),
    )
    status_options = (
        ('1', 'Open'),
        ('2', 'In Progress'),
        ('3', 'Done'),
        ('4', 'To Do'),
        ('5', 'In Review'),
        ('6', 'Under review'),
        ('7', 'Approved'),
        ('8', 'Cancelled'),
        ('9', 'Rejected'),
        ('10', 'Draft'),
        ('11', 'Published'),
        ('12', 'Interviewing'),
        ('13', 'Accepted'),
        ('14', 'Purchased'),
        ('15', 'Requested'),
    )

    severity_options = (
        ('1', "Extraordinary"),
        ('2', "High"),
        ('3', "Moderate"),
        ('4', "Low")
    )

    class TicketObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='open')


    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1,null=True)
    owner = models.ForeignKey(User, related_name='ticket_owner',on_delete=models.PROTECT)
    assignee = models.ManyToManyField(User, related_name='ticket_to_assign',db_constraint=False)
    type = models.CharField(max_length=50,choices=type_options)
    subject = models.CharField(max_length=250)
    status = models.CharField(max_length=10,choices=status_options, default=1)
    detail = models.TextField()
    labels = models.TextField()
    #labels = models.ForeignKey(Label,on_delete=models.SET_NULL,blank=True,null=True)
    severity = models.IntegerField(choices=severity_options)
    attachments = models.ManyToManyField(Attachment)
    comments = models.TextField(default=[])
    created_at = models.DateTimeField(default=timezone.now)
    objects = models.Manager()
    ticketobjects = TicketObjects()

    #@property
    #def owner(self):
    #    return self.owner

    def __str__(self):
        return self.subject

    def label_search(self, search):
        s1 = search + ','.strip()
        s2 = ',' + search + ','.strip()
        s3 = ',' + search.strip()
        q = Q(labels__istartswith=s1) | Q(labels__icontains=s2) | Q(labels__iexact=search) | Q(labels__iendswith=s3)
        # WHERE labels LIKE 'search,%' OR labels LIKE '%,search,%' OR labels='search'
        filtered = Ticket.objects.filter(q)
        return filtered

    def get_user_tickets(self, user):
        q = Q()
        q &= Q(assignee=user)
        filtered = Ticket.objects.filter(q).values('id', 'type', 'subject', 'severity', 'created_at', 'detail', 'status')
        return filtered


#class Logger(models.Model):
