from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from .views import (
    ProjectCreateAPIView,
    ProjectListAPIView,
    ProjectDetailAPIView,
    ProjectUpdateAPIView,
    ProjectDeleteAPIView,
    ProcessCreateAPIView,
    ProcessListAPIView,
    ProcessDetailAPIView,
    ProcessUpdateAPIView,
    ProcessDeleteAPIView,
    TaskCreateAPIView,
    TaskListAPIView,
    TaskDetailAPIView,
    TaskUpdateAPIView,
    TaskDeleteAPIView,
    StageCreateAPIView,
    StageListAPIView,
    StageDetailAPIView,
    StageUpdateAPIView,
    StageDeleteAPIView,
    UpdateInReviewStatusAPIView,
    StatusCreateAPIView,
    StatusListAPIView,
    StatusDetailAPIView,
    StatusUpdateAPIView,
    StatusDeleteAPIView,
    # UserCreateAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserListAPIView,
)

urlpatterns = [
    ## Project api urls
    url(r'^project/create/$', ProjectCreateAPIView.as_view(), name='project-create'),
    url(r'^project/$', ProjectListAPIView.as_view(), name='project-list'),
    url(r'^project/detail/(?P<pk>[0-9]+)/$', ProjectDetailAPIView.as_view(), name='project-detail'),
    url(r'^project/update/(?P<pk>[0-9]+)/$', ProjectUpdateAPIView.as_view(), name='project-update'),
    url(r'^project/delete/(?P<pk>[0-9]+)/$', ProjectDeleteAPIView.as_view(), name='project-delete'),
    ## Process api urls
    url(r'^process/create/$', ProcessCreateAPIView.as_view(), name='process-create'),
    url(r'^process/$', ProcessListAPIView.as_view(), name='process-list'),
    url(r'^process/detail/(?P<pk>[0-9]+)/$', ProcessDetailAPIView.as_view(), name='process-detail'),
    url(r'^process/update/(?P<pk>[0-9]+)/$', ProcessUpdateAPIView.as_view(), name='process-update'),
    url(r'^process/delete/(?P<pk>[0-9]+)/$', ProcessDeleteAPIView.as_view(), name='process-delete'),
    ## Task api urls
    url(r'^task/create/$', TaskCreateAPIView.as_view(), name='task-create'),
    url(r'^task/$', TaskListAPIView.as_view(), name='task-list'),
    url(r'^task/detail/(?P<pk>[0-9]+)/$', TaskDetailAPIView.as_view(), name='task-detail'),
    url(r'^task/update/(?P<pk>[0-9]+)/$', TaskUpdateAPIView.as_view(), name='task-update'),
    url(r'^task/delete/(?P<pk>[0-9]+)/$', TaskDeleteAPIView.as_view(), name='task-delete'),
    ## Stage api urls
    url(r'^stage/create/$', StageCreateAPIView.as_view(), name='stage-create'),
    url(r'^stage/$', StageListAPIView.as_view(), name='stage-list'),
    url(r'^stage/detail/(?P<pk>[0-9]+)/$', StageDetailAPIView.as_view(), name='stage-detail'),
    url(r'^stage/update/(?P<pk>[0-9]+)/$', StageUpdateAPIView.as_view(), name='stage-update'),
    url(r'^stage/delete/(?P<pk>[0-9]+)/$', StageDeleteAPIView.as_view(), name='stage-delete'),
    ## update status of tasks
    url(r'^status/create/$', StatusCreateAPIView.as_view(), name='status-create'),
    url(r'^status/$', StatusListAPIView.as_view(), name='status-list'),
    url(r'^status/detail/(?P<pk>[0-9]+)/$', StatusDetailAPIView.as_view(), name='status-detail'),
    url(r'^status/update/(?P<pk>[0-9]+)/$', StatusUpdateAPIView.as_view(), name='status-update'),
    url(r'^status/delete/(?P<pk>[0-9]+)/$', StatusDeleteAPIView.as_view(), name='status-delete'),
    url(r'^task/status/update/(?P<order>[0-9]+)/$', UpdateInReviewStatusAPIView.as_view(), name='status-update'),
    # template view
    url(r'^projects/$', TemplateView.as_view(template_name="project.html"), name='temp-view'),
    #url(r'^projects/(?P<query>\w+)/$',ProjectListAPIView.as_view() , name='temp-view'),
    url(r'^processes/$', TemplateView.as_view(template_name="process.html"), name='processtemp-view'),
    url(r'^login/$', TemplateView.as_view(template_name="login.html"), name='login-view'),
    url(r'^logout/$', TemplateView.as_view(template_name="logout.html"), name='logout-view'),
    # user api urls
    url(r'^user/login/$', UserLoginAPIView.as_view(), name='user-login'),
    url(r'^user/logout/$', UserLogoutAPIView.as_view(), name='user-logout'),
    url(r'^user/list/$', UserListAPIView.as_view(), name='user-list'),
]
