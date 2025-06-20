from rest_framework.filters import BaseFilterBackend
class OwnerFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(User=request.user)
