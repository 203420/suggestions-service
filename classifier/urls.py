from django.urls import path, re_path
from django.conf.urls import include

from classifier.views import classifierView

urlpatterns = [
    re_path(r'', classifierView.as_view()),
]