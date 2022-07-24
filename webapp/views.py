from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import TemplateView
from webapp.forms import SketchpadForm
from webapp.models import Sketchpad


class IndexView(TemplateView):
    def get(self, request):
        sketchpads = Sketchpad.objects.all()
        return render(request, 'index.html', {"sketchpads": sketchpads})


class SketchpadView(TemplateView):
    template_name = 'sketchpad_view.html'

    def get_context_data(self, **kwargs):
        kwargs['sketchpad'] = get_object_or_404(Sketchpad, pk=kwargs['pk'])
        return super().get_context_data(**kwargs)


class CreateSketchpad(View):
    def get(self, request, *args, **kwargs):
        form = SketchpadForm()
        return render(request, 'create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SketchpadForm(data=request.POST)
        if form.is_valid():
            type = form.cleaned_data.pop("type")
            new_sketchpad = form.save()
            new_sketchpad.type.set(type)
            return redirect("CreateSketchpad", pk=new_sketchpad.pk)
        return render(request, "create.html", {"form": form})


class UpdateSketchpad(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        sketchpad = get_object_or_404(Sketchpad, pk=pk)
        form = SketchpadForm(initial={
            "summary": sketchpad.summary,
            "description": sketchpad.description,
            "status": sketchpad.status,
            "type": sketchpad.type.all()
        })
        return render(request, 'update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        sketchpad = get_object_or_404(Sketchpad, pk=pk)
        form = SketchpadForm(data=request.POST, instance=sketchpad)
        if form.is_valid():
            type = form.cleaned_data.pop('type')
            sketchpad = form.save()
            sketchpad.type.set(type)
            return redirect('index')
        return render(request, 'update.html', {"form": form})


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
