
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image as PilImage
from urllib import parse
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
        published_image_pages = ImagePage.objects.live().order_by("path")
        context["images_and_thumbnails"] = []

        for i in published_image_pages:
            if i.image:
                context["images_and_thumbnails"].append({"page": i, "thumbnail": i.image})
            elif i.thumbnail_image:
                context["images_and_thumbnails"].append({"page": i, "thumbnail": i.thumbnail_image})
        return context


class ImagePage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    thumbnail_image = models.ForeignKey(
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

    def get_context(self, request):
        context = super(ImagePage, self).get_context(request)

        all_image_pages = list(ImagePage.objects.live().order_by("path"))
        current_index = all_image_pages.index(self)
        next_page = all_image_pages[current_index + 1].url if current_index + 1 < len(all_image_pages) else None
        previous_page = all_image_pages[current_index - 1].url if current_index - 1 >= 0 else None

        context["next_page"] = next_page
        context["previous_page"] = previous_page
        return context

    def get_youtube_video_id(self):
        video_url = self.body.split("url=\"")[1].split("\"")[0]
        query_params = parse.parse_qs(
            parse.urlparse(video_url).query
        )
        video_id = query_params["v"][0]
        return video_id

    def save(self, clean=True, user=None, log_action=False, **kwargs):
        if clean:
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
                thumbnail_title = f"youtube_thumbnail_%s" % video_id
                thumbnail_exists = Image.objects.filter(title=thumbnail_title).exists()

                if thumbnail_exists:
                    self.thumbnail_image = Image.objects.get(title=thumbnail_title)
                else:
                    thumbnail_url = f"http://img.youtube.com/vi/%s/0.jpg" % video_id
                    thumbnail_image = PilImage.open(requests.get(thumbnail_url, stream=True).raw)
                    image_io = io.BytesIO()
                    thumbnail_image.save(image_io, format='JPEG')
                    image_io.seek(0)
                    if self.thumbnail_image:
                        old_image = self.thumbnail_image
                        self.thumbnail_image = None
                        old_image.delete()
                    self.thumbnail_image = Image.objects.create(
                        title=thumbnail_title,
                        file=ContentFile(image_io.read(), name=f"{self.title}.jpg"),
                    )
        super().save(clean, user, log_action, **kwargs)
