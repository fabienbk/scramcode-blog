from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # public urls
    url(r'^$', 'blog.views.home', name='home'),
    
    url(r'^post/(?P<post_id>\d+)/previous/$', 'blog.views.show_previous', name='show_previous'),
    url(r'^post/(?P<post_id>\d+)/next/$', 'blog.views.show_next', name='show_next'),    
    url(r'^post/(?P<post_id>\d+)/(.*)/$', 'blog.views.show_post', name='show_post'),
    
    # blog admin
    url(r'^accounts/login/$', 'django.contrib.auth.views.login' , name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'} , name='logout'),
    
    url(r'^edit/$', 'blog.admin_views.edit_post', name='edit_post'),
    url(r'^list/$', 'blog.admin_views.list_post', name='list_post'),
    
    
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    

)


# ... the rest of your URLconf goes here ...
urlpatterns += staticfiles_urlpatterns()
