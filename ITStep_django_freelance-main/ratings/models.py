from django.db import models
from freelance.models import OrderRequest


class RatingOrder(models.Model):
    order = models.ForeignKey(
        to="freelance.Order",
        verbose_name="Заказ",
        on_delete=models.CASCADE,
        related_name="order_rating",
    )
    testimonial = models.TextField(verbose_name="Отзыв", blank=True, null=True)

    user = models.ForeignKey(
        to="freelance.UserProfile",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="user_rating",
        null=True,
        blank=True,
    )

    order_rating = models.FloatField(verbose_name="Рейтинг", blank=True, null=True)

    def __str__(self):
        return (
            self.order.customer.profile.user.username
            or self.order.executor.profile.user.username
        )

    class Meta:
        unique_together = ("order", "user")
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
