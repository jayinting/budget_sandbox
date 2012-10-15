from django.conf.urls import patterns, url

from budget import views as budView

urlpatterns = patterns('',
                       
#-------------------------------------------------------------------------------------------------- 
# General Views                  
#-------------------------------------------------------------------------------------------------- 

    url(r'^$', (budView.Index_View.as_view()), name="Index_View"),
    url(r'^csv/$', (budView.Import_Csv.as_view()), name="Import_Csv"),

)