from django.db import models
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    source = models.CharField(max_length=255, verbose_name=_("NewsSource"), null=True, blank=True)
    author = models.CharField(max_length=150, verbose_name=_("NewsAuthor"), null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name=_("NewsTitle"))
    description = models.TextField(verbose_name=_("NewsDescription"), null=True, blank=True)
    content = models.CharField(max_length=255, verbose_name=_("NewsContent"), null=True, blank=True)

    url = models.URLField(verbose_name=_("NewsUrl"), null=True, blank=True)
    image = models.URLField(verbose_name=_("NewsImageUrl"), null=True, blank=True)

    published_at = models.DateTimeField(verbose_name=_("NewsPublishedAt"), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ("-created",)

    def __str__(self):
        return f"News [{self.pk} {self.title[:10]}]"
