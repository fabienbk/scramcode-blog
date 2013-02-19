from django import forms
from django.shortcuts import render
from django_markdown.widgets import MarkdownWidget
from models import Post, get_last_posts, get_post 
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

class NewPostForm(forms.Form):
    post_id = forms.IntegerField(required=False)
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=MarkdownWidget())


def create_or_update_post(post_id, title, text, want_publish):     
    post = Post()
    if post_id != None and post_id > 0:
        post = get_post(post_id)
    post.title = title
    post.text = text
    if want_publish and post.online is False:
        post.online = True
    post.save()
    return post


@login_required
def edit_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():                                                
            want_publish = False
            if request.POST.has_key('save-publish'):
                want_publish = True
            
            post_id = form.cleaned_data['post_id']
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            post = create_or_update_post(post_id, title, text, want_publish)            
            return HttpResponseRedirect('/post/'+str(post.id)+"/"+str(post.slug)+"/")            
    else:        
        if request.GET.has_key('edit'):
            post_id = request.GET['edit']
            post = get_post(post_id)
            form = NewPostForm({'title':post.title, 'text':post.text, 'post_id':post_id})
        else:
            form = NewPostForm({'title':'', 'text':'', 'post_id':''})
            
    return render(request, 'admin/edit_post.html', {'form': form, 'last_post_list': get_last_posts(True, 20)})


@login_required
def list_post(request):
    if request.method == 'POST':
        if request.POST.has_key('edit'):
            return HttpResponseRedirect('/edit/?edit='+request.POST['edit'])
        elif request.POST.has_key('toggle'):
            post = Post.objects.get(id=request.POST['toggle'])
            post.online = not post.online
            post.save()
        elif request.POST.has_key('delete'):
            post = Post.objects.get(id=request.POST['delete'])
            post.delete()            
        
    post_list = Post.objects.all()
    return render(request, 'admin/list_post.html', {'post_list': post_list})

