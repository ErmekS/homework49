from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
# Create your views here.
from django.utils.http import urlencode

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import SketchpadForm, SearchForm
from webapp.models import Sketchpad, Project


class IndexSketchpadView(ListView):
    model = Sketchpad
    template_name = "issues/index.html"
    context_object_name = "sketchpads"
    ordering = "-updated_time"
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Sketchpad.objects.filter(
                Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Sketchpad.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class SketchpadView(DetailView):
    template_name = "issues/sketchpad_view.html"
    model = Sketchpad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project.project_name
        print(context)
        return context


class CreateSketchpad(CreateView):
    form_class = SketchpadForm
    template_name = "issues/create.html"

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:ProjectView", kwargs={"pk": self.object.project.pk})


class UpdateSketchpad(UpdateView):
    model = Sketchpad
    form_class = SketchpadForm
    context_object_name = 'sketchpad'
    template_name = 'issues/update.html'

    def get_success_url(self):
        return reverse('webapp:SketchpadView', kwargs={'pk': self.object.pk})


class DeleteSketchpad(DeleteView):
    model = Sketchpad
    template_name = 'issues/delete.html'
    context_object_name = 'sketchpad'
    success_url = reverse_lazy('webapp:IndexSketchpadView')
