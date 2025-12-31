from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


# Create your models here.


def validate_age(birth_date):
    if not birth_date:
        return

    today = date.today()

    age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    if age < 15:
        raise ValidationError(_("L’utilisateur doit avoir au moins 15 ans."))


class User(AbstractUser):

    REQUIRED_FIELDS = ["birth_date"]

    birth_date = models.DateField(
        null=False,
        blank=False,
        validators=[validate_age],
        help_text=_("Date de naissance (minimum 15 ans)"),
        verbose_name=_("date de naissance"),
    )

    contact_permission = models.BooleanField(
        default=False,
        help_text=_("Indique si l’utilisateur accepte d’être contacté (RGPD)"),
        verbose_name=_("permission de contact"),
    )

    def __str__(self):
        return self.username
