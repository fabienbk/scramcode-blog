from blog.models import get_last_posts, get_latest_post_id, get_post, get_next_post, get_previous_post
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_page

def home(request):    
    return show_post(request, get_latest_post_id())


@cache_page(60 * 15)
def show_post(request, post_id):
    if post_id != None:
        post_list = get_last_posts(False, 10)
        post = get_post(post_id)
        return render(request, 'index.html', {'post' : post, 'recent_post_list' : post_list[1:10]})
    else:
        return render(request, 'index.html', {'post' : None, 'recent_post_list' : []})

    
def show_next(request, post_id):
    next_post = get_next_post(post_id)
    if next_post != None:
        return HttpResponseRedirect('/post/'+str(next_post.id)+'/'+str(next_post.slug)+'/')
    else:
        post = get_post(post_id)
        return HttpResponseRedirect('/post/'+str(post.id)+'/'+str(post.slug)+'/')


def show_previous(request, post_id):
    previous_post = get_previous_post(post_id)
    if previous_post != None:
        return HttpResponseRedirect('/post/'+str(previous_post.id)+'/'+str(previous_post.slug)+'/')
    else:
        post = get_post(post_id)
        return HttpResponseRedirect('/post/'+str(post.id)+'/'+str(post.slug)+'/')
