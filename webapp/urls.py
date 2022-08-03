from django.urls import path
# from django.views.generic import RedirectView

from webapp.views import IndexView, SketchpadView, CreateSketchpad, UpdateSketchpad, DeleteSketchpad, CreateProject, ProjectView, IndexSketchpadView, UpdateProject, DeleteProject

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('project/<int:pk>', ProjectView.as_view(), name='ProjectView'),
    path('sketchpad/', IndexSketchpadView.as_view(), name='IndexSketchpadView'),
    path('sketchpad/<int:pk>', SketchpadView.as_view(), name='SketchpadView'),
    path('project/sketchpad/create/<int:pk>/', CreateSketchpad.as_view(), name='CreateSketchpad'),
    path('project/sketchpad/update/<int:pk>/', UpdateSketchpad.as_view(), name='UpdateSketchpad'),
    path('sketchpad/delete/<pk>/', DeleteSketchpad.as_view(), name='DeleteSketchpad'),
    path('project/create/', CreateProject.as_view(), name='CreateProject'),
    path('project/update/<int:pk>/', UpdateProject.as_view(), name='UpdateProject'),
    path('project/delete/<pk>/', DeleteProject.as_view(), name='DeleteProject'),
]



