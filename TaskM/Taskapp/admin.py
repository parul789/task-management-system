from django.contrib import admin
from .models import Project,Process,Task,Stage,Status

class ProjectModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','start_date','end_date','stage']
    class Meta:
        model = Project

class ProcessModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','priority','status']
    class Meta:
        model = Process

class TaskModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','order','process','status','created']
    class Meta:
        model = Task

class StageModelAdmin(admin.ModelAdmin):
    list_display = ['id','entry']


class StatusModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'status','task']


admin.site.register(Project,ProjectModelAdmin)
admin.site.register(Process,ProcessModelAdmin)
admin.site.register(Task,TaskModelAdmin)
admin.site.register(Stage,StageModelAdmin)
admin.site.register(Status,StatusModelAdmin)


