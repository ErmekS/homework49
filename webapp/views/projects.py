from django.shortcuts import redirect
# Create your views here.
from django.urls import reverse_lazy

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic import ListView

from webapp.forms import ProjectForm
from webapp.models import Project


class IndexView(ListView):
    model = Project
    template_name = "projects/index.html"
    context_object_name = "projects"
    ordering = "-start_date"
    paginate_by = 3


class ProjectView(DetailView):
    template_name = "projects/project_view.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.projects.order_by("-created_time")
        return context


class CreateProject(CreateView):
    form_class = ProjectForm
    template_name = "projects/create.html"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        return redirect("ProjectView", pk=project.pk)


class UpdateProject(UpdateView):
    model = Project
    template_name = 'projects/update.html'
    form_class = ProjectForm
    context_object_name = 'project'


class DeleteProject(DeleteView):
    model = Project
    template_name = "projects/delete.html"
    success_url = reverse_lazy('index')
