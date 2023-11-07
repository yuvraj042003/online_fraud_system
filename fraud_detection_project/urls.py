"""fraud_detection_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fraud_detection_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="showHomePageToUser"),
    path('login/', views.loginPage, name="loginUserPage"),
    path('register/', views.register, name="registerPageForUser"),
    path('logout/', views.logoutPage, name="logOutUser"),
    path('saveuser',views.saveUser, name="saveUserDetailOnRegistration"),
    path('home/',views.homePage,name="showHomePageBasedonSession"),
    path('show-acc/',views.showAccountDetails,name="showAccountDetailOfUser"),
    path('send-money/',views.sendMoney,name="sendMoneytoUSer"),
    path('feedback/', views.feedback, name='feedback'),
    path('save-feedback/', views.saveFeedback, name='savefeedbackofuser'),
    # path('test/', views.gg, name='detectionalgo'),
    path('auto-fill/', views.autoFill, name='autofilluserdetails'),
    path('from-account-getuserdetails/', views.fromAccountGetDetails, name='fromAccountGetDetails'),
    path('add-recipent/', views.addRecipent, name='addrecepient'),
    path('open-account/', views.openAccount, name='opennew Account'),
    path('send-otp/',views.sendOTP,name='sendotpmethod'),
    path('transfer/',views.transferAmount,name='sendmoney'),
    path('withdraw/',views.withdrawl,name='money'),
path('desposit/',views.deposite,name='desposite'),
 path('renderDeposit/',views.renderDeposit,name='renderDeposit'),
path('renderWithr/',views.renderWithr,name='renderWithr')
]
