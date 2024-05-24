from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Service
from .forms import ServiceForm

def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})

def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('services:service_list'))
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form})

def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect(reverse('services:service_list'))
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form})

def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect(reverse('services:service_list'))
    return render(request, 'services/service_confirm_delete.html', {'service': service})
