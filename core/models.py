import math
import datetime

from django.db import models

class User(models.Model):
    """
    User Schema
    """
    name = models.CharField(max_length=255)
    