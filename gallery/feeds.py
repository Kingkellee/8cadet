from django.contrib.syndication.views import Feed
from gallery.models import Album


class AlbumFeed(Feed):
    title = "Latest albums"
    link = "/"
    description = " "

    def items(self):
        return Album.objects.order_by("-creation_date")

    def item_title(self, item):
        return item.name

