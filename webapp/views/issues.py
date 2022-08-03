from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
# Create your views here.
from django.utils.http import urlencode
from django.views import View
from django.views.generic import FormView, ListView, DetailView, CreateView

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
        return reverse("ProjectView", kwargs={"pk": self.object.project.pk})


class UpdateSketchpad(FormView):
    form_class = SketchpadForm
    template_name = "issues/update.html"

    def dispatch(self, request, *args, **kwargs):
        self.sketchpad = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("SketchpadView", kwargs={"pk": self.sketchpad.pk})

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['instance'] = self.sketchpad
        return form_kwargs

    def form_valid(self, form):
        self.sketchpad = form.save()
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(Sketchpad, pk=self.kwargs.get("pk"))


class DeleteSketchpad(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        sketchpad = get_object_or_404(Sketchpad, pk=pk)
        return render(request, 'issues/delete.html', {'sketchpad': sketchpad})

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        sketchpad = get_object_or_404(Sketchpad, pk=pk)
        sketchpad.delete()
        return redirect('index')
