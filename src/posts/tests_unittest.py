from django.test import TestCase, Client, RequestFactory
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from posts.models import Post
from .forms import *


class Setup_data(TestCase):
	
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(id=1,username="kevin11",password="kaka1234")

class User_Form_Test(TestCase):

	''' SignUpForm with complete fields '''
	def test_SignUpForm_valid(self):
		
		form = SignUpForm(data={'username':"kevin11", 'first_name':"kevin", 'last_name':"smith", 'email':"kevin@live.com", 
											'password1':"kaka1234",'password2':'kaka1234'})
		self.assertTrue(form.is_valid())


	''' SignUpForm with blank fields '''
	def test_SignUpForm_invalid(self):
		form = SignUpForm(data={'username':"ii", 'first_name':"kevin", 'last_name':"smith", 'email':"kevin@live.com", 
											'password':"kevin1234"})

		self.assertFalse(form.is_valid())

	''' LoginForm with complete fields'''
	def test_LoginForm_valid(self):
		form = LoginForm(data={'username':"kevin11",'password':"kaka1234"})
		self.assertTrue(form.is_valid())

	
	''' LoginForm with blank fields'''
	def test_LoginForm_invalid(self):
		form = LoginForm(data={'username':"",'password':"kaka1234"})
		self.assertFalse(form.is_valid())


class User_View_Test(Setup_data):

	''' login_view with valid credentials'''
	def test_login_view_valid(self):
		user_login = self.client.login(username="kevin11",password='kaka1234')
		self.assertTrue(user_login)
		response = self.client.post(reverse("posts:list"))
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,"post_list.html")

	
	''' login_view with invalid credentials'''
	def test_login_view_invalid(self):
		user_login = self.client.login(username="Andy",password='kaka1234')
		self.assertFalse(user_login)


	''' Access Dashboard with logged in user, @login_required decorator'''
	def test_dashboard_with_login(self):
		user_login = self.client.login(username="kevin11",password='kaka1234')
		response = self.client.get(reverse('posts:dashboard',kwargs={'id':self.user.id}))
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,"dashboard.html")

	
	''' Access Dashboard without logged in user, @login_required decorator'''
	def test_dashboard_without_login(self):
		response = self.client.get(reverse('posts:dashboard',kwargs={'id':self.user.id}))
		self.assertEqual(response.status_code,302)
		self.assertRedirects(response,'/posts/accounts/login/?next=/posts/dashboard/1/')

	
	''' Create Post with logged in user, @login_required decorator'''
	def test_create_post(self):
		user_login = self.client.login(username="kevin11",password='kaka1234')
		post = Post.objects.create(title='hello world', content='my test post', publish='2018-04-04')
		response = self.client.get(reverse('posts:dashboard',kwargs={'id':self.user.id}))
		self.assertEqual(post.title,"hello world")
		self.assertEqual(response.status_code,200)
		self.assertContains(response,"my test post")

	
	''' Create Post without logged in user, @login_required decorator'''
	def test_create_post(self):
		post = Post.objects.create(title='hello world', content='my test post', publish='2018-04-04')
		response = self.client.get(reverse('posts:dashboard',kwargs={'id':self.user.id}))
		self.assertEqual(response.status_code,302)
		self.assertRedirects(response,'/posts/accounts/login/?next=/posts/dashboard/1/')























