from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Application, Job
from .forms import Jobform


class JoblistView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'all_jobs'


class JobDetailView(DetailView):
    model = Job 
    template_name = 'jobs/job_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['already_applied'] = Application.objects.filter(
                job=self.object, applicant=self.request.user
            ).exists()
        else:
            context['already_applied'] = False
        return context


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = Jobform
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job_list')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = Jobform
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('my_job_list')

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)


class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('my_job_list')

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)


class MyJobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/my_job_list.html'
    context_object_name = 'my_jobs'

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)


@login_required
def apply_to_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    application, created = Application.objects.get_or_create(
        job=job,
        applicant=request.user,
    )
    if created:
        messages.success(request, 'Your application was submitted.')
    else:
        messages.info(request, 'You have already applied for this job.')
    return redirect('job_detail', pk=job.pk)


class MyApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'jobs/my_application_list.html'
    context_object_name = 'my_applications'

    def get_queryset(self):
        return Application.objects.filter(
            applicant=self.request.user
        ).select_related('job')