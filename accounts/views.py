from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .models import CustomUser,UploadedFile
from .filters import CustomUserFilter
from .forms import FileUploadForm
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import CustomUser, UploadedFile
from .serializers import CustomUserSerializer, UploadedFileSerializer
from djoser.views import TokenCreateView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .utils import *
from .tokens import *
from PIL import Image
from PyPDF2 import PdfReader
import fitz
import io
from django.utils.http import urlsafe_base64_decode
import pyotp

User = get_user_model()
 
def home(request):
    return render(request,"accounts/home.html")

def signup(request):
    if request.method == 'POST':
        public_visibility = False
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repass']
        public_visibility = request.POST.get('cb1')
        #print(public_visibility)

        if User.objects.filter(username=username):
            messages.error(request,"Username already in use")
            return redirect("home")
    
        if User.objects.filter(email=email):
            messages.error(request,"email id already in use")
            return redirect("home")
    
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters")

        if password != repassword:
            messages.error(request,"Password not matching")
        else:
            if public_visibility == 'on': 
                public_visibility = True
            else:
                public_visibility = False
            
            CustomUser = get_user_model()
            myuser = CustomUser.objects.create_user(username,email,password)
            myuser.first_name = firstname
            myuser.last_name = lastname
            myuser.public_visibility = public_visibility
            myuser.is_active=False
            myuser.save()
            send_email_client(email) 
            # confirmation_email(request, myuser)         
            current_site = get_current_site(request)
            confirm_subject = "Confirm your email"
            confirm_msg = render_to_string('email_confirmation.html', {
            'name':myuser.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser),
            })
    
            email = EmailMessage(
                confirm_subject,
                confirm_msg,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = True
            email.send()

        # if not username.isalnum():
        #     messages.error(request,"username should be alphanumeric")    
        #     return redirect("home")
    
        # myuser = User.objects.create_user(username,email,password)
        
        return redirect('signin')
    
    return render(request,"accounts/signup.html")

def signin(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        otp = request.POST['otp']

        print(f"Received credentials: email={email}, password={password}")
    
        user = authenticate(username=email, password=password)

        print(f"Authenticated user: {user}")
        
        if user is not None:
            login(request, user)
            return redirect('index')

        else:
            messages.error(request,"Wrong credentials")
            return redirect('home')
            

    return render(request,"accounts/signin.html")


class AuthorsAndSellersView(FilterView):
    model = CustomUser
    template_name = 'authors_and_sellers.html'
    filterset_class = CustomUserFilter
    context_object_name = 'users'

# @otp_required
@login_required(login_url='signin')        
def users(request):
    users = User.objects.all()
    print(users)
    return render(request, 'users.html', {'users': users})

# @otp_required
@login_required(login_url='signin')  # Redirects to login page if not logged in
def index(request):
    users = User.objects.all()
    # print(users)
    return render(request, 'index.html', {'users': users})
    
# @otp_required
@login_required
def upload_book(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            messages.success(request, 'Book uploaded successfully.')
            return redirect('uploaded_files')
        else:
            messages.error(request, 'Error uploading the book. Please check the form.')
    else:
        form = FileUploadForm()

    return render(request, 'upload_book.html', {'form': form})

# @login_required
# def uploaded_files(request):
#     user_files = UploadedFile.objects.filter(user=request.user)
#     return render(request, 'uploaded_files.html', {'user_files': user_files})

def uploaded_files(request):
    user_files = UploadedFile.objects.filter(user=request.user)
    
    for file in user_files:
        if file.file.name.lower().endswith('.pdf'):
            pdf_path = file.file.path
            pdf_document = fitz.open(pdf_path)
            
            first_page = pdf_document[0]
            image = first_page.get_pixmap()
            
            image_pil = Image.frombytes("RGB", (image.width, image.height), image.samples)

            thumbnail_path = f"{pdf_path}_thumbnail.png"
            image_pil.save(thumbnail_path)
            
            file.thumbnail_path = thumbnail_path
            file.save()
    
    return render(request, 'uploaded_files.html', {'user_files': user_files})


def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)

    # Assuming the 'file' field in UploadedFile is a FileField
    file_path = uploaded_file.file.path

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
        return response


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

class GenerateToken(APIView):
    def post(self, request):
        if request.method == 'POST':
            email = request.data.get('email')
            password = request.data.get('password')

            print(f"Received credentials: email={email}, password={password}")

            user = authenticate(request, username=email, password=password)

            print(f"Authenticated user: {user}")

            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'access_token': access_token})
            else:
                return Response({'error': 'Invalid Credentials'}, status=401)
        return Response({'error': 'Invalid request method'}, status=400)


class FileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_files = UserFile.objects.filter(user=request.user)
        serializer = UserFileSerializer(user_files, many=True)
        return Response(serializer.data)


# class RegisterAPI(APIView):
#     def post(self, request):
#         try:
#             data =  request.data
#             serializer = UserSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return  Response({
#                     'status':200,
#                     'message': 'registration is successful, check email',
#                     'data' : serializer.data,
#                 })
                
#             return Response({
#                 'status': 400,
#                 'message': 'something went wrong',
#                 'data': serializer.data,
#             })
#         except Exception as e:
#             print(e)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser=None
        
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('index')
        
    else:
        return render(request, 'activation_failed.html')
           
# def otp(request):
#     if request.method == 'POST':
#         email = request.POST['email1']
#         otp = request.POST['otp']
#         user = CustomUser.objects.filter(email=email)
#         if not user.exists():
#             messages.error(request,"User does not exist")
#             return redirect("home")
#         if not user[0].otp == otp:
#             messages.error(request,"Invalid otp")
#             return redirect("home")
#         user[0].is_verified = False
#         user[0].save()
#         messages.success(request,"Account verified successfully")
#         return redirect("signin")
    

#     return render(request,"accounts/otp.html")

