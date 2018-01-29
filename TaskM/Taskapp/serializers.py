from rest_framework import serializers
from .models import Project, Process, Task, Stage, Status
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import date
from rest_framework.serializers import (
    EmailField,
    CharField, )
from django.core.validators import ValidationError
from django.db.models import Q
from rest_framework.authtoken.models import Token
from django.db.models.fields import CharField


### these serializer are for CRUD operations
class TaskSerializer(serializers.ModelSerializer):
    # process = serializers.SerializerMethodField()
    # user_assignedto = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id', 'user_assignedto', 'title', 'image', 'created', 'end_date', 'order', 'process',
            'status')


class TaskUpdateSerializer(serializers.ModelSerializer):
    process = serializers.ReadOnlyField(source='process.title')

    class Meta:
        model = Task
        fields = ('status', 'id', 'user_createdby', 'user_assignedto', 'title', 'image', 'created', 'end_date', 'order',
                  'process')
        read_only_fields = (
            'id', 'user_createdby', 'user_assignedto', 'title', 'image', 'created', 'end_date', 'order', 'process',
            'task_update'
        )


class user_assignedtoserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class TaskListSerializer(serializers.ModelSerializer):
    process = serializers.ReadOnlyField(source='process.title')
    user_assignedto = user_assignedtoserializer(read_only=True, many=True)
    user_createdby = serializers.ReadOnlyField(source='user_createdby.username')

    class Meta:
        model = Task
        fields = ('status', 'id', 'user_createdby', 'user_assignedto', 'title', 'image', 'created', 'end_date', 'order',
                  'process',
                  )
        read_only_fields = (
            'id', 'user_createdby', 'user_assignedto', 'title', 'image', 'created', 'end_date', 'order', 'process',
            'task_update'
        )


class StatusSerializer(serializers.ModelSerializer):
    task = serializers.ReadOnlyField(source='task.title')

    class Meta:
        model = Status
        fields = ('id', 'status', 'task')


class ProcessSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Process
        fields = ('id', 'title', 'priority', 'status', 'project', 'tasks')

    def get_tasks(self, obj):
        return TaskSerializer(obj.task.all(), many=True).data

    def get_project(self, obj):
        return {"title": obj.project.title, "id": obj.project.id}


class ProcessCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ('id', 'title', 'priority', 'status', 'project',)


class ProjectSerializer(serializers.ModelSerializer):
    stage = serializers.ReadOnlyField(source='stage.entry')
    processes = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'user', 'title', 'start_date', 'end_date', 'stage', 'processes')

    def get_processes(self, obj):
        return ProcessSerializer(obj.process.all(), many=True).data

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("finish must occur after start")
        return data


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'user', 'title', 'start_date', 'end_date', 'stage')
        # write_only_fields = ('stage',)

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("finish must occur after start")
        return data


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ('entry', 'id')


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('stage',)


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    email = EmailField(label="Email Address")
    email2 = EmailField(label="Confirm Email")

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'email2')
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        email = data['email']

        return data

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This email has already been registered.")
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.Serializer):
    email = EmailField(label="Email Address")

    # username = CharField()

    class Meta:
        model = User
        fields = ('email',)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
