from django.contrib.auth.models import AbstractUser
from django.db import models

STATUS_CHOICES = [
    ("b", "Block"),
    ("u", "Unblock"),
]

ROLES = [
    ("user", "user"),
    ("admin", "admin"),
]


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(
        "Имя",
        max_length=150,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        "role", max_length=25, choices=ROLES, default=ROLES[0][0]
    )
    blocked = models.CharField(
        "Блокировка",
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[1][0],
    )

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ROLES[-1][0] or self.is_staff or self.is_superuser

    @property
    def is_user(self):
        return self.role == ROLES[0][0]

    @property
    def is_blocked(self):
        return self.blocked == STATUS_CHOICES[0][0]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="follower",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="following",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = (
            models.UniqueConstraint(
                fields=("user", "author",), name="unique_following"
            ),
        )

    def __str__(self):
        return f"{self.user} follows {self.author}"
