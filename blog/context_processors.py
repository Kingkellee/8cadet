from .models import Post
from newsletter.forms import SubscriptionForm

def posts(request):
	form = SubscriptionForm()
    return {
        'all_posts': Post.objects.order_by('created_on'),
        'popular_posts': Post.objects.filter(status=1).order_by('-hit_count_generic__hits')[:10],
        'form': form,
    }