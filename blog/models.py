from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from markdown import markdown

class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    text = models.TextField()
    text_html = models.TextField(editable=False, blank=True, null=True)    
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    online = models.BooleanField()
    url = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title
        
    # generate and save the html
    def save(self):
        self.text_html = markdown(self.text, ['codehilite'])
        self.slug = slugify(self.title)
        super(Post, self).save()
        
    @permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, { 'slug': self.slug })
        
        
def get_post(post_id):
    return Post.objects.get(id=int(post_id))        
        
        
def get_latest_post_id():
    last_post_list = get_last_posts(False, 1)
    if len(last_post_list) == 0:
        return None
    else:
        return last_post_list[0].id


def get_last_posts(include_offline, max_number):
    if include_offline:
        return Post.objects.all().order_by('-creation_date')[:max_number]
    else:
        return Post.objects.all().filter(online__exact=True).order_by('-creation_date')[:max_number]
    
    
def get_next_post(post_id):
    current_post = get_post(post_id)
    next_list = Post.objects.all().filter(creation_date__gt=current_post.creation_date)[:1]
    if (len(next_list) == 0):
        return None
    else:
        return next_list[0]


def get_previous_post(post_id):
    current_post = get_post(post_id)
    previous_list = Post.objects.all().order_by('-creation_date').filter(creation_date__lt=current_post.creation_date)[:1]    
    if (len(previous_list) == 0):
        return None
    else:
        return previous_list[0]


