from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

def index(request):
    return HttpResponse("Homepage")

def form(request):
    template = loader.get_template('emptyseat/form.html')
    # return HttpResponse(template.render({}, request))
    return render(request, 'emptyseat/form.html', {})

def setup_schedule(request):
    print(request.POST)
    for i in request.POST:
        print(request.POST[i])
    return HttpResponseRedirect(reverse('emptyseat:index'))