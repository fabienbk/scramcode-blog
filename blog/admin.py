from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import MarkdownWidget
from blog.models import Post
from django.db import models
from markupfield.fields import MarkupField

admin.site.register(Post)



