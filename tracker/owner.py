from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import ProcessFormView, CreateView, DeleteView, UpdateView
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
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["submit"] = "Create"
        return context
class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    def get_queryset(self):
        return super(OwnerUpdateView, self).get_queryset().filter(User=self.request.user)
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["submit"] = "Update"
        return context
class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        return super(OwnerDeleteView, self).get_queryset().filter(User=self.request.user)
class OwnerDuplicateView(OwnerCreateView):
    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        return ProcessFormView.get(self,request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["submit"] = "Create"
        return context