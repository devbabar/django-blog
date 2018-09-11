from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from comments.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

'''import Q for search bar'''
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect,Http404, JsonResponse
from django.core import serializers
from django.shortcuts import render,get_object_or_404, redirect
from .models import Post
from comments.models import Comment
from .forms import PostForm, LoginForm, SignUpForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import datetime
today = timezone.now().date()

"""===============================================
-------------Handle user account------------------
==============================================="""

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/posts')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
	if request.method=='POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			u=form.cleaned_data['username']
			p=form.cleaned_data['password']
			user=authenticate(username=u, password=p)
			if user is not None:
				if user.is_active:
					login(request,user)
					messages.success(request,"You have been successfully logged in. Welcome back {}".format((user.username).capitalize()))
					return HttpResponseRedirect(reverse('posts:list'))
			else:
				messages.error(request,"The username or password were incorrect, Try Again")
				return HttpResponseRedirect(reverse('posts:login'))
	else:
		form=LoginForm()
		return render(request, 'accounts/login.html',{'form':form})

def logout_view(request):
	logout(request)
	messages.success(request,"You have been successfully logged out.")
	return HttpResponseRedirect(reverse('posts:list'))


"""=======================================
-------------Create Post------------------
======================================="""

@login_required
def post_create(request,id):
	form= PostForm(request.POST or None, request.FILES or None)
	
	if form.is_valid():
		instance=form.save(commit=False)
		instance.user = request.user
		instance.save()
		success_msg="Succes sfully Created"
		
		if instance.draft==True:
			draft_posts	= Post.objects.select_related("user").filter(user=request.user, draft = True).order_by('-timestamp')
			return render(request,"ajax_draft_posts.html",{"draft_posts":draft_posts})
		
		elif instance.publish > today:
			future_posts = Post.objects.select_related("user").filter(Q(publish__gte=today), user=request.user, draft = False).order_by('-timestamp')
			return render(request,'ajax_future_posts.html', {"future_posts":future_posts,})
		
		else:
			owner_posts	= Post.objects.select_related("user").filter(Q(publish__lte=today), user=request.user, draft = False).order_by('-timestamp')
			context={
						"instance":instance,
						"owner_posts":owner_posts
					}
			return render(request,"create_update.html",context)	

	form=PostForm()
	return HttpResponse(form.as_p(),content_type="application/json")

"""=======================================
-------------Detail Post------------------
======================================="""

@login_required
def post_detail(request,slug=None):

	"""Note: get_object_or_404 actually takes you to 404 error page, query does not exits"""
	instance=Post.objects.select_related("user").get(slug=slug)

	''' if we don't use ModelManager
	content_type=ContentType.objects.get_for_model(Post)
	obj_id = instance.id
	comments = Comment.objects.filter(content_type=content_type, object_id=obj_id).order_by('-timestamp')'''

	''' we set initial data to grab the post'''
	initial_data = {
		"content_type" : instance.get_content_type,
		"object_id" : instance.id,
	}

	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		new_comment= Comment.objects.create(user = request.user,
											content_type = content_type,
											object_id = obj_id,
											content = content_data
											)

		data = serializers.serialize("json",[new_comment,],use_natural_foreign_keys=True,use_natural_primary_keys=True,fields=("user","content","timestamp",))
		return HttpResponse(data)

	comments = Comment.objects.filter_by_instance(instance).select_related("user").order_by('-timestamp')

	context={
		'comments':comments,
		'today':today,
		'title':instance.title,
		'instance':instance,
		'form' : form
		}
	return render(request,'post_detail.html',context)

"""=======================================
-------------List Post------------------
======================================="""

def post_list(request):
	''' 3 ways to filter the queryset, all have almost the same performance '''
	queryset_list = Post.objects.select_related('user').filter(Q(publish__lte=today)).exclude(draft = True).order_by('-timestamp')
	# queryset_list = Post.objects.select_related('user').filter(Q(publish__lte=today),draft= False).order_by('-timestamp')
	# queryset_list = Post.objects.select_related('user').filter(publish__lte=today,draft= False).order_by('-timestamp')
	
	# if not queryset_list.publish > timezone.now().date() and queryset_list.draft:
	"""Note: for search bar"""
	query=request.GET.get('q')
	if query:
		queryset_list=queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()
	
	""" Note: For page pagination """
	paginator = Paginator(queryset_list, 3) # Show 3 post per page
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context={
		'object_list':queryset,
		'title':'List of Blog Post',
		'today':today
	}	
	return render(request,'post_list.html',context)

"""=======================================
-------------   Search  ------------------
======================================="""

def search(request):
	
	queryset_list = Post.objects.select_related('user').filter(Q(publish__lte=today)).exclude(draft = True).order_by('-timestamp')
	query=request.GET.get('q')
	if query:
		queryset_list=queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()

	if not queryset_list:
		messages.error(request,"Sorry No Result Found, Try Again..!")

	context={
		'object_list':queryset_list,
		'today':today
	}	
	return render(request,'search_result.html',context)

"""=======================================
-------------Update Post------------------
======================================="""


@login_required
def post_update(request,id,slug=None):
	instance=get_object_or_404(Post,slug=slug)
	if request.user == instance.user:
		form= PostForm(request.POST or None,request.FILES or None, instance=instance)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.save()
			messages.success(request,"Successfully Updated")
			return HttpResponseRedirect(instance.get_absolute_url())
	else:
		messages.error(request,"Sorry you are not authorized to edit this post")
		return redirect('posts:list')
	context={
		'title':instance.title,
		'instance':instance,
		'form':form,
	}
	return render(request,'update_form.html',context)



"""=======================================
-------------Delete Post------------------
======================================="""
	
@login_required
def post_delete(request,slug=None):
	
	instance = get_object_or_404(Post,slug=slug)
	if request.user == instance.user:
		instance.delete()
		messages.success(request,"Successfully deleted")
		return HttpResponseRedirect(request.META.get('HTTP_REFERER',"dashboard"))
	else:
		messages.error(request,"Sorry you are not authorized to delete this post")
		return redirect('posts:list')


"""=========================================================
------------- Dashboard Related Functions ------------------
========================================================="""

@login_required
def dashboard(request,id):
	owner_posts	= Post.objects.select_related("user").filter(Q(publish__lte=today),user=request.user,draft = False).order_by('-timestamp')
	
	if not owner_posts:
		messages.error(request,"Sorry no post to display, would you like to create a post ?")

	form= PostForm(request.POST or None, request.FILES or None)
	context = {
		"owner_posts"	:owner_posts,
		"form"			:form
		}
	return render(request,'dashboard.html',context)


''' Dashboard Options: Functions for $Ajax calls '''
@login_required
def dashboard_draft(request,id):
	
	draft_posts	= Post.objects.select_related("user").filter(user=request.user,draft = True).order_by('-timestamp')
	print draft_posts
	
	if not draft_posts:
		messages.error(request,"Sorry no post to display")

	context = {
		"draft_posts"	:draft_posts,
		}
	return render(request,'ajax_draft_posts.html',context)

@login_required
def dashboard_future(request,id):
	if not request.is_ajax():
		messages.error(request,"Sorry not valid Ajax call, try again..")
		return redirect('posts:list')
		''' if you want to return to the previous page than user HTTP_REFERER'''
		# return HttpResponseRedirect(request.META.get('HTTP_REFERER',"dashboard"))

	future_posts = Post.objects.select_related("user").filter(Q(publish__gte=today),user=request.user,draft = False).order_by('-timestamp')
	
	if not future_posts:
		messages.error(request,"Sorry no post to display")

	context = {
		"future_posts"	:future_posts,
		}
	return render(request,'ajax_future_posts.html',context)
