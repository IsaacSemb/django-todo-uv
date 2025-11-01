from django.db import models
from django.contrib.auth.models import User


NOTES = """

django has an inbuilt user, so most cases no need for user model


"""


class Todo(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        # How items are ordered when you query them
        ordering = ["-created_at"]  # descending

        # Human-readable names in admin panel
        verbose_name = "Todo Item"  # Singular
        verbose_name_plural = "Todo Items"  # Plural

        # Database table name (optional, Django auto-generates one)
        db_table = "todos"

        # Unique constraints across multiple fields
        constraints = [
            models.UniqueConstraint(
                fields=["title", "user"], name="unique_title_per_user"
            ),
            models.UniqueConstraint(
                fields=["description", "user"], name="unique_desc_per_user"
            ),
        ]

        # Indexing for faster searches
        indexes = [
            models.Index(fields=["status"]),  # Makes filtering by status faster
        ]

    def __str__(self):
        return f"{self.title} -- {self.description}"
