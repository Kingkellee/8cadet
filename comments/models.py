from django.db import models
from django.contrib.auth.models import User
from blog.models import Post


class Comment (models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	content = models.TextField()
	created_on = models.DateTimeField(auto_now_add = True)
	active = models.BooleanField(default=False)

	class Meta:
	    ordering = ['-created_on']


	def __str__(self):
	    return 'Comment {} by {}'.format(self.content, self.author)

	@property
	def get_all_reply(self):
		return self.replies.all().order_by('reply_time')

	@property
	def get_replies_count(self):
		return self.replies.all().count()


class Reply(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_author')
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
	reply_time = models.DateTimeField(auto_now_add=True)
	reply_content = models.TextField()

	class Meta:
	    verbose_name_plural = 'replies'

	def __str__(self):
	    return 'Reply {} by {}'.format(self.reply_content, self.author)