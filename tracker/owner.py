from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
class OwnerListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return super(OwnerListView, self).get_queryset().filter(User=self.request.user)
class OwnerDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return super(OwnerDetailView, self).get_queryset().filter(User=self.request.user)
class OwnerCreateView(LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        object = form.save(commit=False)
        object.User = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)
class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    def get_queryset(self):
        return super(OwnerUpdateView, self).get_queryset().filter(User=self.request.user)
class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        return super(OwnerDeleteView, self).get_queryset().filter(User=self.request.user)