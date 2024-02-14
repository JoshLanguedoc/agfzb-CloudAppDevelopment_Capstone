from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path(route='about', view=views.about, name='about'), #path for about page
    path(route='contact', view=views.contact, name='contact'), #path for contact page

    # path for registration

    path(route='login', views.login_request, name='login'), #path for login requests
    path(route='logout', views.logout_request, name='logout'), #path for logout requests
    path(route='', view=views.get_dealerships, name='index'), #path for index page

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)