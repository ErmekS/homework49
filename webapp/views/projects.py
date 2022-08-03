from django.shortcuts import redirect, get_object_or_404, render
# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, FormView
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


class UpdateProject(FormView):
    form_class = ProjectForm
    template_name = "projects/update.html"

    def dispatch(self, request, *args, **kwargs):
        self.project = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("ProjectView", kwargs={"pk": self.project.pk})

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['instance'] = self.project
        return form_kwargs

    def form_valid(self, form):
        self.project = form.save()
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(Project, pk=self.kwargs.get("pk"))


class DeleteProject(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        project = get_object_or_404(Project, pk=pk)
        return render(request, 'projects/delete.html', {'project': project})

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return redirect('index')
