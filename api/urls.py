from django.urls import path
from api import views
from api.views import NoteListView, NoteDetailView
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'


urlpatterns = [
    path('notes/', NoteListView.as_view(), name='note_list'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

