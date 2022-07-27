from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
# Create your views here.
from django.views import View
from django.views.generic import TemplateView, FormView, ListView
from webapp.forms import SketchpadForm, SearchForm
from webapp.models import Sketchpad
from django.urls import reverse
from django.utils.http import urlencode
from webapp.base_view import FormView as CustomFormView


class IndexView(ListView):
    model = Sketchpad
    template_name = "index.html"
    context_object_name = "sketchpads"
    ordering = "-updated_time"
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Sketchpad.objects.filter(
                Q(description__icontains=self.search_value) | Q(summary__icontains=self.search_value))
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


class SketchpadView(TemplateView):
    template_name = 'sketchpad_view.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        sketchpad = get_object_or_404(Sketchpad, pk=pk)
        kwargs["sketchpad"] = sketchpad
        return super().get_context_data(**kwargs)


class CreateSketchpad(CustomFormView):
    form_class = SketchpadForm
    template_name = "create.html"

    def form_valid(self, form):
        self.sketchpad = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect("SketchpadView", pk=self.sketchpad.pk)


class UpdateSketchpad(FormView):
    form_class = SketchpadForm
    template_name = "update.html"

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
        return render(request, 'delete.html', {'sketchpad': sketchpad})

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        sketchpad = get_object_or_404(Sketchpad, pk=pk)
        sketchpad.delete()
        return redirect('index')
