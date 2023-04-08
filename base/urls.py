from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.loginPage,name='loginPage'),
    path('logout/',views.logoutPage,name="logoutPage"),
    path('task-image/<str:pk>/',views.task_image,name="taskImage"),
    path('task-approve/<str:pk>/',views.task_approve,name="taskApprove"),
    path('task-form/',views.task_form,name="taskForm")
    # path('task',views.getTasks),
    # path('task/<int:pk>/',views.getTask),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)