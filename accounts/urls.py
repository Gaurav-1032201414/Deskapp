from django.db import router
from django.urls import path,include
from . import views
from .views import AuthorsAndSellersView 
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, UploadedFileViewSet,GenerateToken #,FileView
from django.contrib.auth import views as auth_views
# from two_factor.urls import urlpatterns as tf_urls
# from django_otp import urls as otp_urls
# from two_factor.views import SetupView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'uploaded_files', UploadedFileViewSet,basename='uploaded_files')

urlpatterns = [
    path('', views.home, name='home'),
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('index',views.index, name='index'),
    path('users',views.users, name='users'),
    path('authors_and_sellers/', AuthorsAndSellersView.as_view(), name='authors_and_sellers'),
    path('upload_book',views.upload_book,name='upload_book'),
    path('upload_files',views.uploaded_files,name='uploaded_files'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('api/', include(router.urls)),
    path('api1/generate-token/', GenerateToken.as_view(), name='generate_token'),
    # path('api2/file_view/', FileView.as_view(), name='file_view'),
    path('logout/', views.custom_logout, name='logout'),
    # path('two_factor/', include(otp_urls)),
    # path('setup/', SetupView.as_view(), name='setup'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),
    # path('auth_signin/', views.auth_signin, name='auth_signin'),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    # path("otp", views.otp, name="otp"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
