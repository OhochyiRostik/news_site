from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from site_app.views import *

urlpatterns = [
    # path('', cache_page(60)(NewsHome.as_view()), name='home'),
    path('', NewsHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),

    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', NewsCategory.as_view(), name='category'),
    # re_path(r'archive/(?P<year>[0-9]{4})/', archive)
]
