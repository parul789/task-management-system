from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework.authtoken.models import Token
from django.http import HttpResponseForbidden
from .models import Process, Project, Task, Stage, Status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ProjectSerializer,
    ProcessSerializer,
    TaskSerializer,
    StageSerializer,
    # UpdateStatusSerializer,
    StatusSerializer,
    TaskUpdateSerializer,
    ProcessCreateSerializer,
    ProjectCreateSerializer,
    TaskListSerializer,
    ProjectUpdateSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserListSerializer,
)
from django.contrib.auth import authenticate
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from django.db.models import Q
from .permissions import IsUserEdit


class ProjectCreateAPIView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectListAPIView(ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('q', None)
        if user.is_authenticated:
            result = Project.objects.filter(
                Q(user=user) | Q(process_q__user=user) | Q(process_q__task_q__user_assignedto=user) | Q(
                    process_q__task_q__user_createdby=user)).distinct()
            if query:
                result = result.filter(title__icontains=query)
            return result


class ProjectDetailAPIView(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        print('fgfgdfg')
        if user.is_authenticated:
            return Project.objects.filter(Q(user=user) | Q(process_q__user=user)).distinct()
        else:
            raise HttpResponseForbidden


class ProjectUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ProjectUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Project.objects.filter(user=user)
        else:
            raise Http404


class ProjectDeleteAPIView(DestroyAPIView):
    serializer_class = ProjectSerializer

    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Project.objects.filter(user=user)
        else:
            raise HttpResponseForbidden


# Process views

class ProcessCreateAPIView(CreateAPIView):
    queryset = Process.objects.all()
    serializer_class = ProcessCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProcessListAPIView(ListAPIView):
    serializer_class = ProcessSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Process.objects.filter(
                Q(user=user) | Q(project__user=user) | Q(task_q__user_assignedto=user) | Q(
                    task_q__user_createdby=user)).distinct()
        else:
            raise HttpResponseForbidden


class ProcessDetailAPIView(RetrieveAPIView):
    serializer_class = ProcessSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Process.objects.filter(
                Q(user=user) | Q(project__user=user) | Q(task_q__user_assignedto=user) | Q(
                    task_q__user_createdby=user)).distinct()
        else:
            raise HttpResponseForbidden


class ProcessUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ProcessCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Process.objects.filter(Q(user=user) | Q(project__user=user))
        else:
            raise HttpResponseForbidden


class ProcessDeleteAPIView(DestroyAPIView):
    serializer_class = ProcessSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Process.objects.filter(Q(user=user) | Q(project__user=user))
        else:
            raise HttpResponseForbidden


# Task views

class TaskCreateAPIView(CreateAPIView):
    # if created < end_date & created >= process__project__start_date & end_date >= process__project__start_date & created >= process__project__end_date & created >= process__project__end_date:
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user_createdby=self.request.user)
        instance = serializer.save()
        email = []
        for i in instance.user_assignedto.all():
            print(i.email)
            email.append(i.email)
        info = 'You have been assigned a new task.Login into Task Management System to see details.'
        return send_mail('Poll', info, 'creofridaygames@gmail.com', email,
                         fail_silently=False)


class TaskListAPIView(ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Task.objects.filter(Q(user_assignedto=user) | Q(user_createdby=user)).distinct()
        else:
            raise HttpResponseForbidden


class TaskDetailAPIView(RetrieveAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Task.objects.filter(Q(user_assignedto=user) | Q(user_createdby=user)).distinct()
        else:
            raise HttpResponseForbidden


class TaskUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserEdit]
    queryset = Task.objects.all()
    print('fghjdsjhgh1234354')

    def perform_update(self, serializer):
        print('hello')
        instance = serializer.save()
        if instance.status == 'Finished':
            data = serializer.data
            print(data['order'])
            orders = list(Task.objects.values_list("order", flat=True))
            print(orders)
            a = data['order']
            for j in orders:
                a = a + 1
                print(j)
                if a in orders:
                    p = Task.objects.get(order=a)
                    users = p.user_assignedto.all()
                    email_id = []
                    for i in users:
                        print(i.email)
                        email_id.append(i.email)
                    info = "Previous order task completed, You may start your task, Login to see the details"
                    return send_mail('Poll', info, 'creofridaygames@gmail.com', email_id,
                                     fail_silently=False)
                    break


class TaskDeleteAPIView(DestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Task.objects.filter(process__project__user=user)
        else:
            raise HttpResponseForbidden


# Stage views

class StageCreateAPIView(CreateAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StageListAPIView(ListAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StageDetailAPIView(RetrieveAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StageUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StageDeleteAPIView(DestroyAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Status views

class StatusCreateAPIView(CreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StatusListAPIView(ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StatusDetailAPIView(RetrieveAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StatusUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StatusDeleteAPIView(DestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# UPDATE TASK STATUS of another user

class UpdateInReviewStatusAPIView(RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'order'

    def perform_update(self, serializer):
        serializer.save(status='InReview')
        instance = serializer.save()
        email = []
        for i in instance.user_assignedto.all():
            email.append(i.email)
        info = "Found bug in the task of order, kindly debug it."
        return send_mail('Poll', info, 'creofridaygames@gmail.com', email,
                         fail_silently=False)


class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response = {}
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            # if User.objects.filter(email=data.get('email')):
            user = User.objects.filter(email=data.get('email')).first()
            if user.check_password(data.get('password')):
                Token.objects.filter(user=user).delete()
                token = Token.objects.create(user=user)
                print(token)
                response.update({'token': "Token {}".format(token.key),
                                 'username': user.first_name, 'email': user.email})

            print("Login:", response)
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    queryset = User.objects.all()

    def post(self, request):
        return self.logout(request)

    def logout(self, request, format=None):
        try:
            request.user.auth_token.delete()
        except:
            pass
        # logout(request)
        return Response(status=status.HTTP_200_OK)


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
