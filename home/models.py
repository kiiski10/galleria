
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image as PilImage
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images.models import Image
from wagtail.models import Page
import io
import requests


class HomePage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context["published_image_pages"] = (
            ImagePage.objects.live()
        )
        return context


class ImagePage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('image'),
        FieldPanel('body'),
    ]

    def get_youtube_video_id(self):
        video_url = self.body.split("url=\"")[1].split("\"")[0]
        video_id = video_url.split("/")[-1]
        if "&" in video_id:
            video_id = video_id.split("&")[0]
        if "?t=" in video_id:
            video_id = video_id.split("?t=")[0]
        if "?v=" in video_id:
            video_id = video_id.split("?v=")[1]
        return video_id

    def save(self, clean=True, user=None, log_action=False, **kwargs):
        youtube_urls = [
            "url=\"https://www.youtube",
            "url=\"https://youtube",
            "url=\"https://www.youtu.be",
            "url=\"https://youtu.be",
        ]
        has_embedded_content = "<embed embedtype=\"media\"" in self.body
        embedded_content_is_youtube_video = any(x in self.body for x in youtube_urls)

        if has_embedded_content and embedded_content_is_youtube_video:
            video_id = self.get_youtube_video_id()
            thumbnail_url = f"http://img.youtube.com/vi/%s/0.jpg" % video_id
            thumbnail_image = PilImage.open(requests.get(thumbnail_url, stream=True).raw)
            image_io = io.BytesIO()
            thumbnail_image.save(image_io, format='JPEG')
            image_io.seek(0)
            self.image = Image.objects.create(
                title=self.title,
                file=ContentFile(image_io.read(), name=f"{self.title}.jpg"),
            )
        super().save(clean, user, log_action, **kwargs)


