from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import OuterRef, Exists
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

from freelance.models import Order, OrderRequest, UserProfile
from ratings.models import RatingOrder
from ratings.forms import RatingForm


class RatingListView(LoginRequiredMixin, ListView):
    model = RatingOrder
    template_name = "ratings/rating_list.html"
    form_class = RatingForm
    success_url = reverse_lazy("ratings:rating_list")
    context_object_name = "ratings"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # Получаем поисковый запрос из GET параметра
        search_query = request.GET.get("search", "").strip()

        if search_query:
            # Фильтруем записи по содержанию поискового запроса в username
            self.object_list = RatingOrder.objects.filter(
                user__user__username__icontains=search_query
            ).order_by("user__user__username")
        else:
            # Если поисковый запрос пуст, загружаем все записи или ничего не загружаем
            self.object_list = RatingOrder.objects.all().order_by(
                "user__user__username"
            )

        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = request.POST
        if form["filter"] == "executor":
            queryset = RatingOrder.objects.filter(user__user__groups__name="Executors")
        elif form["filter"] == "customer":
            queryset = RatingOrder.objects.filter(user__user__groups__name="Customers")
        else:
            queryset = RatingOrder.objects.all()

        self.object_list = queryset

        context = self.get_context_data()
        return self.render_to_response(context)


class RatingUpdateView(LoginRequiredMixin, UpdateView):
    model = RatingOrder
    template_name = "ratings/rating_update.html"
    form_class = RatingForm
    success_url = reverse_lazy("ratings:rating_list")

    def get_object(self, queryset=None):
        pk = self.kwargs.get("order")

        user_type = {"Customers": "customer", "Executors": "executor"}.get(
            self.request.user.groups.first().name, "customer"
        )

        order = get_object_or_404(Order, pk=pk)

        order_request = (
            OrderRequest.objects.filter(order=order, status__in=["accepted"])
            .distinct()
            .first()
        )

        if user_type == "customer":
            user = order_request.executor.profile
        else:
            user = order.customer.profile

        if queryset is None:
            queryset = RatingOrder.objects.filter(order_id=pk, user=user)
            self.pk = queryset.first().pk

        rating_order = queryset.first()

        if not rating_order or not RatingOrder.objects.filter(order=order, user=user):
            rating_order = RatingOrder.objects.create(order=order, user=user)
            self.pk = rating_order.pk

        return rating_order

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # stars = request.POST
        stars = "5"
        if form.is_valid():
            return self.form_valid(form)
        else:
            if form.error_class:
                form.error_class = None
                self.object = self.get_object()
                form = self.get_form()
                if form.save(commit=False):
                    form.save()
                    user = UserProfile.objects.get(user=form.instance.user.user)
                    user.rating = (user.rating + float(stars)) / 2
                    user.save()
                    return redirect(self.get_success_url())
                else:
                    return self.form_invalid(form)
            return self.form_invalid(form)


class RatingDetailView(LoginRequiredMixin, DetailView):
    model = RatingOrder
    template_name = "ratings/rating_detail.html"
    form_class = RatingForm
    success_url = reverse_lazy("ratings:rating_list")


class RatingCreateView(LoginRequiredMixin, CreateView):
    model = RatingOrder
    template_name = "ratings/rating_update.html"
    form_class = RatingForm
    success_url = reverse_lazy("ratings:rating_list")


class AboutCustomerRatingView(LoginRequiredMixin, DetailView):
    model = RatingOrder
    template_name = "ratings/rating_update.html"
    form_class = RatingForm
    success_url = reverse_lazy("ratings:rating_list")

    def get_object(self, queryset=None):
        pk = self.kwargs.get("order")
        if queryset is None:
            queryset = RatingOrder.objects.filter(order_id=pk)
            self.pk = queryset.first().pk
        return queryset
