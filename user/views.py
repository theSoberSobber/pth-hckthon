from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login
from django.conf import settings
from .models import *
from .utils import getMediaImageList
import json

class UserLogin(TemplateView):
    template_name = 'user/login.html'
    extra_context = {}
    temp_data = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        self.extra_context["passpoint"] = False
        self.extra_context["username"] = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        step = self.request.POST.get("step",None)
        
        if step=="auth":
            username = request.POST.get("inputUsername","")
            password = request.POST.get("inputPassword","")
            user_obj = User.objects.filter(username=username)
            if user_obj:
                user_obj = user_obj.first()
                is_password = user_obj.check_password(password)
                user_attempt_obj = UserAttempt.objects.filter(user=user_obj)
                if user_attempt_obj:
                    user_attempt_obj = user_attempt_obj.first()
                else:
                    user_attempt_obj = UserAttempt.objects.create(user=user_obj)
                
                if user_attempt_obj.unauthorized_attempt_count>=settings.MAX_ATTEMPT_COUNT:
                    messages.error(request,"Due to maximum attempts, you account has blocked, for unblocking it kindly contact us.")
                    return redirect("login")
                elif not is_password:
                    messages.error(request,"Invalid Credentials, Please enter the correct password")
                    return redirect("login")
                else:
                    imgset1, imgset2, imgset3 = getMediaImageList(username)
                    self.temp_data[username] = True
                    self.extra_context["passpoint"] = True
                    self.extra_context["username"] = username
                    self.extra_context["imgset1"] = imgset1
                    self.extra_context["imgset2"] = imgset2
                    self.extra_context["imgset3"] = imgset3
                    context = self.get_context_data(**kwargs)
                    return self.render_to_response(context)
            else:
                messages.error(request,"Invalid Credentials, Please enter the correct username")
                return redirect("login")
        elif step=="passpoint":
            yields = json.loads(request.POST["yields"])
            username = request.POST.get("username","")
            user_obj = User.objects.get(username=username)
            user_attempt_obj = UserAttempt.objects.get(user=user_obj)
            auth_passpoint_obj = UserAuthPassPoint.objects.get(user=user_obj)
            password_verify = self.temp_data.get(username,False)
            auth_img_verify = auth_passpoint_obj.auth_images == ",".join(yields["imgSrcList"])
            auth_point_verify = False

            points = yields["imgPointList"]
            db_points = json.loads(auth_passpoint_obj.auth_points)
            if (int(points["x1"]) in range(int(db_points["x1"])-20, int(db_points["x1"])+20)) and \
                (int(points["y1"]) in range(int(db_points["y1"]) - 20, int(db_points["y1"]) + 20)) and \
                    (int(points["x2"]) in range(int(db_points["x2"])-20, int(db_points["x2"])+20)) and \
                        (int(points["y2"]) in range(int(db_points["y2"]) - 20, int(db_points["y2"]) + 20)) and \
                            (int(points["x3"]) in range(int(db_points["x3"])-20, int(db_points["x3"])+20)) and \
                                (int(points["y3"]) in range(int(db_points["y3"]) - 20, int(db_points["y3"]) + 20)):
                                auth_point_verify = True
            if password_verify and auth_img_verify and auth_point_verify:
                login(request,user_obj)
                del self.temp_data[username]
                user_attempt_obj.unauthorized_attempt_count = 0
                user_attempt_obj.save()
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                user_attempt_obj.unauthorized_attempt_count += 1
                user_attempt_obj.save()
                if user_attempt_obj.unauthorized_attempt_count>=settings.MAX_ATTEMPT_COUNT:
                    messages.error(request,"Due to maximum attempts, you account has blocked, for unblocking it kindly contact us.")
                else:
                    messages.error(request,f"Incorrect auth image points, you have {settings.MAX_ATTEMPT_COUNT-user_attempt_obj.unauthorized_attempt_count} attempt left")
                return redirect("login")
        else:
            return redirect("login")

class UserRegistration(TemplateView):
    template_name = 'user/register.html'
    extra_context = {}
    temp_data = {}

    def get(self, request, *args, **kwargs):
        self.extra_context["passpoint"] = False
        self.extra_context["username"] = None
        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        step = self.request.POST["step"]
        if step=="new":
            username = request.POST.get("inputUser","")
            fname = request.POST.get("inputFName","")
            lname = request.POST.get("inputLName","")
            password = request.POST.get("inputPassword","")
            con_password = request.POST.get("inputConPassword","")
            user_obj = User.objects.filter(username=username)
            if user_obj:
                messages.error(request,"Username already exist, kindly choose different one")
                return redirect("register")
            elif password != con_password:
                messages.error(request,"Password and Confirm password does not match")
                return redirect("register")
            else:
                user_data = {
                    "username" : username,
                    "first_name" : fname,
                    "last_name" : lname,
                    "password" : password,
                }
                imgset1, imgset2, imgset3 = getMediaImageList()
                self.temp_data[username] = user_data
                self.extra_context["passpoint"] = True
                self.extra_context["username"] = username
                self.extra_context["imgset1"] = imgset1
                self.extra_context["imgset2"] = imgset2
                self.extra_context["imgset3"] = imgset3
                context = self.get_context_data(**kwargs)
                return self.render_to_response(context)
        elif step=="passpoint":
            yields = json.loads(request.POST["yields"])
            username = request.POST["username"]
            user_data = self.temp_data[username]

            user_obj = User()
            user_obj.username = user_data["username"]
            user_obj.first_name = user_data["first_name"]
            user_obj.last_name = user_data["last_name"]
            user_obj.set_password(user_data["password"])
            user_obj.save()

            auth_passpoint_obj = UserAuthPassPoint()
            auth_passpoint_obj.user = user_obj
            auth_passpoint_obj.auth_images = ",".join(yields["imgSrcList"])
            auth_passpoint_obj.auth_points = json.dumps(yields["imgPointList"])
            auth_passpoint_obj.save()
            del self.temp_data[username]
            return redirect("login")
        else:
            return redirect("/register/?step=auth")

class UserLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")

class UserDashboard(LoginRequiredMixin,TemplateView):
    template_name = 'user/dashboard.html'
    login_url = reverse_lazy('login')