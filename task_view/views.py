from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

from .models import Task
from .forms import EmailForm


# Możlwiość zastosowania class view
# class PostListView(ListView):
#     queryset = Task.published.all()
#     context_object_name = 'tasks'
#     paginate_by = 3
#     template_name = 'task_view/task/list.html'


def tasks_list(request):
    #tasks = Task.objects.all() I wersja
    object_list = Task.objects.all() # II wersja
    paginator = Paginator(object_list, 1)
    page_number = request.GET.get('page')
    try:
        tasks = paginator.page(page_number)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    return render(request,
                  'task_view/task/list.html',
                  {'tasks': tasks,
                   'page': page_number})


def task_detail(request, year, month, day, task):
    task = get_object_or_404(Task,
                             slug=task,
                             status='in_progress',
                             created__year=year,
                             created__month=month,
                             created__day=day,
                             )
    return render(request,
                  'task_view/task/detail.html',
                  {'task': task})


def task_share(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #cleaned_data. This attribute is a dictionary of form fields and their values.

            task_url = request.build_absolute_uri(task.get_absolute_url())
            subject = f"{cd['name']} recommends you do "f"{task.title}"
            message = f"Read {task.title} at {task_url}\n\n"f"{cd['name']}\'s comments: {cd['comments']}"

            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailForm() # else = GET
    return render(request, 'task_view/task/share.html', {'task': task,
                                                         'form': form,
                                                         'sent': sent})


def hello(request):
    return HttpResponse(f'Hello !!!! Now is {timezone.now()}')


