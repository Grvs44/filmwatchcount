from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import ProcessFormView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ContextMixin:
    context = {}

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs).update(self.context)


class UserMixin:
    def get_queryset(self):
        return super().get_queryset().filter(User=self.request.user)


class OwnerListView(UserMixin, LoginRequiredMixin, ListView):
    pass


class OwnerDetailView(UserMixin, LoginRequiredMixin, DetailView):
    pass


class OwnerCreateView(ContextMixin, UserMixin, LoginRequiredMixin, CreateView):
    template_name = 'filmwatchcount/form_template.html'
    context = {'submit_label': 'Create'}

    def form_valid(self, form):
        object = form.save(commit=False)
        object.User = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerUpdateView(ContextMixin, UserMixin, LoginRequiredMixin, UpdateView):
    template_name = 'filmwatchcount/form_template.html'
    context = {'submit_label': 'Update'}


class OwnerDeleteView(ContextMixin, UserMixin, LoginRequiredMixin, DeleteView):
    template_name = 'filmwatchcount/form_template.html'
    context = {'submit_label': 'Delete'}


class OwnerDuplicateView(OwnerCreateView):
    template_name = 'filmwatchcount/form_template.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return ProcessFormView.get(self, request, *args, **kwargs)
