from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import HomePage
from wagtail.models import Page, Site

class Command(BaseCommand):
    help = 'Description of your custom command'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        try:
            root_page = Page.objects.get(pk=1)
            print("Root page found:", root_page)

            homepage = Page.objects.get(
                title="Welcome to your new Wagtail site!",
                slug="home",
                path="00010001",
                depth=2,
            )
            print("Homepage found:", homepage)

            site = Site.objects.get(
                pk=1,
                is_default_site=True,
            )
            print("Site found:", site)

            homepage.delete()

            # Create a new HomePage instance
            new_homepage = HomePage(
                title="Galleria",
                slug="home",
                body="",
            )

            # Add the new HomePage as a child of the root_page
            root = Page.get_first_root_node()
            print("Root node found:", root)
            root.add_child(instance=new_homepage)
            new_homepage.save()
            site.root_page = new_homepage
            # Update the Site to use the new HomePage
            site.save()

        except (Page.DoesNotExist, Site.DoesNotExist, HomePage.DoesNotExist) as e:
            print("Error: ", e)
