from django.urls import path
from .views import signUpUser, loginUser, getUser, getSelfInfo, fetchOldMessages

urlpatterns = [
    path('signup', signUpUser.as_view(), name='signup_user'),
    path('login', loginUser.as_view(),name='login_user'),
    path('users', getUser.as_view(), name="get_user"),
    path('self', getSelfInfo.as_view(), name="self_info"),
    path('fetchmessages', fetchOldMessages.as_view(), name='fetch_messages')
]
