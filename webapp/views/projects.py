from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
# Create your views here.
from django.urls import reverse_lazy

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic import ListView

from webapp.forms import ProjectForm, AddUsersForm
from webapp.models import Project


class IndexView(ListView):
    model = Project
    template_name = "projects/index.html"
    context_object_name = "projects"
    ordering = "-start_date"
    paginate_by = 3


# class ProjectView(DetailView):
#     template_name = "projects/project_view.html"
#     model = Project
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['projects'] = self.object.projects.order_by("-created_time")
#         return context


class ProjectView(DetailView):
    template_name = "projects/project_view.html"
    model = Project

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        users = User.objects.filter(projects__pk=pk)
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.projects.order_by("-created_time")
        context["users"] = users
        return context


class AddUsers(UpdateView):
    model = Project
    form_class = AddUsersForm
    template_name = 'projects/add_users_view.html'

    def has_permission(self):
        return self.request.user.has_perm("webapp.add_user") or \
               self.request.user == self.get_object().users


class CreateProject(PermissionRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "projects/create.html"

    def has_permission(self):
        return self.request.user.has_perm("webapp.create_project") or \
               self.request.user == self.get_object().users

    # def form_valid(self, form):
    #     project = form.save(commit=False)
    #     project.save()
    #     return redirect("webapp:ProjectView", pk=project.pk)


class UpdateProject(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/update.html'
    form_class = ProjectForm
    context_object_name = 'project'

    def has_permission(self):
        return self.request.user.has_perm("webapp.update_project") or \
               self.request.user == self.get_object().users


class DeleteProject(DeleteView):
    model = Project
    template_name = "projects/delete.html"
    success_url = reverse_lazy('webapp:index')

    def has_permission(self):
        return self.request.user.has_perm("webapp.remove_project") or \
               self.request.user == self.get_object().users
