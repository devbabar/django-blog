from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from posts.models import Post


class BasicBlogPostTestCase(LiveServerTestCase):

	def setUp(self):

		User.objects.create_user(username="Alex", password="alex1234")
		self.selenium = webdriver.Firefox()
		self.selenium.maximize_window()
		super(BasicBlogPostTestCase, self).setUp()


	def tearDown(self):
		# self.selenium.quit()
		super(BasicBlogPostTestCase, self).tearDown()

	# '''------------------------------------------------------------------
	# Registration with wrong credentials to test form validation errors
	# ------------------------------------------------------------------'''
	
	# def test_registration_with_wrong_credentials(self):
	# 	selenium = self.selenium
	# 	selenium.get("http://127.0.0.1:8000/posts/")

	# 	selenium.find_element_by_id("signup-btn").click()

	# 	selenium.find_element_by_id("id_username").send_keys("mark")
	# 	selenium.find_element_by_id("id_first_name").send_keys("mark")
	# 	selenium.find_element_by_id("id_last_name").send_keys("smith")
	# 	selenium.find_element_by_id("id_email").send_keys("mark@gmail.com")
	# 	selenium.find_element_by_id("id_password1").send_keys("mark1234")

	# 	# wrong password2
	# 	selenium.find_element_by_id("id_password2").send_keys("mark") 

	# 	selenium.find_element_by_name("register").click()

	'''------------------------------------------------------------------
					Registration with correct credentials
	------------------------------------------------------------------'''

	def test_registration_with_correct_credentials(self):
		selenium = self.selenium
		selenium.get("http://127.0.0.1:8000/posts/")

		selenium.find_element_by_id("signup-btn").click()

		selenium.find_element_by_id("id_username").send_keys("mark")
		selenium.find_element_by_id("id_first_name").send_keys("mark")
		selenium.find_element_by_id("id_last_name").send_keys("smith")
		selenium.find_element_by_id("id_email").send_keys("mark@gmail.com")
		selenium.find_element_by_id("id_password1").send_keys("mark1234")
		selenium.find_element_by_id("id_password2").send_keys("mark1234") 

		selenium.find_element_by_name("register").click()
		self.selenium.close()

	'''------------------------------------------------------------------
					Login and Logout functions
	------------------------------------------------------------------'''

	def test_login_and_logout(self):
		selenium = self.selenium
		#Opening the link we want to test, live_server_url follow the setUp database
		# selenium.get('%s%s' % (self.live_server_url,reverse("posts:login")))

		#url follow the credentials from actual database
		selenium.get('http://127.0.0.1:8000/posts/accounts/login/')

		''' Login with credentials'''
		username_input = selenium.find_element_by_id("id_username")
		password_input = selenium.find_element_by_id("id_password")
		login_click = selenium.find_element_by_name("login")

		username_input.send_keys("kevin")
		password_input.send_keys("kevin1234")
		login_click.click()

		''' logout by clicking logout button '''
		logout_click = selenium.find_element_by_name("logout")
		logout_click.click()
		self.selenium.close()

	'''------------------------------------------------------------------
				Access to Dashboard and Create Post
	------------------------------------------------------------------'''
	def test_dashboard(self):
		selenium = self.selenium
		selenium.get('http://127.0.0.1:8000/posts/')
		wait = WebDriverWait(selenium, 1000)



		login_dashboard_click = selenium.find_element_by_id("login-btn").click()

		username_input = selenium.find_element_by_id("id_username")
		password_input = selenium.find_element_by_id("id_password")
		login_click = selenium.find_element_by_name("login")

		username_input.send_keys("kevin")
		password_input.send_keys("kevin1234")
		login_click.click()

		dashboard_btn = selenium.find_element_by_name("dashboard").click()

		self.selenium.execute_script("window.scrollTo(0,document.body.scrollHeight);")


		create_post_btn = selenium.find_element_by_id("create-post").click()
		self.selenium.execute_script("window.scrollTo(0,document.body.scrollHeight);")

		title_input = selenium.find_element_by_id("id_title")
		content_input = selenium.find_element_by_id("id_content")
		image_btn = selenium.find_element_by_xpath("//input[@type='file']")

		title_input.send_keys("selenium test1")
		content_input.send_keys("this is a test for selenium automated test")
		image_btn.send_keys("/Users/babarbaig/Documents/django/final/django_blog/basic_blog/env/src/static/sample_images/foggy_hills.jpg")
		publish_input = selenium.find_element_by_id("id_publish").click()
		selenium.find_element_by_link_text("6").click()
		selenium.find_element_by_id("submit-btn").click()
		
		self.selenium.execute_script("window.scrollTo(0,1400);")

		wait.until(EC.visibility_of_element_located((By.ID,"content-display")))


		dashboard_btn = selenium.find_element_by_name("dashboard").click()
		self.selenium.close()

	'''------------------------------------------------------------------
			Testing @login_required decorator to delete the post
	------------------------------------------------------------------'''

	def test_login_required_decorator(self):
		selenium = self.selenium
		selenium.get('http://127.0.0.1:8000/posts/dashboard/1/')

	def test_delete_post(self):
		selenium = self.selenium
		selenium.get("http://127.0.0.1:8000/posts/login")

		username_input = selenium.find_element_by_id("id_username").send_keys("kevin")
		password_input = selenium.find_element_by_id("id_password").send_keys("kevin1234")
		login_click = selenium.find_element_by_name("login").click()

		dashboard_btn = selenium.find_element_by_name("dashboard").click()
		delete_post_btn = selenium.find_element_by_class_name("delete-post").click()
		self.selenium.close()

	'''------------------------------------------------------------------
			Edit the existing post, update title, content and date 
	------------------------------------------------------------------'''

	def test_update_post(self):
		selenium = self.selenium
		selenium.get("http://127.0.0.1:8000/posts/login")

		username_input = selenium.find_element_by_id("id_username").send_keys("kevin")
		password_input = selenium.find_element_by_id("id_password").send_keys("kevin1234")
		login_click = selenium.find_element_by_name("login").click()

		dashboard_btn = selenium.find_element_by_name("dashboard").click()
		delete_post_btn = selenium.find_element_by_class_name("edit-post").click()

		title_input = selenium.find_element_by_id("id_title").clear()
		title_input = selenium.find_element_by_id("id_title").send_keys("Post update test1")
		content_input = selenium.find_element_by_id("id_content").send_keys("this is a test for selenium automated test to edit post")
		
		# image_btn = selenium.find_element_by_xpath("//input[@type='file']")
		# image_btn.send_keys("/Users/babarbaig/Documents/django/final/django_blog/basic_blog/env/src/static/sample_images/foggy_hills.jpg")
		
		publish_input = selenium.find_element_by_id("id_publish").click()
		selenium.find_element_by_link_text("15").click()
		selenium.find_element_by_class_name("submit-btn").click()

		self.selenium.execute_script("window.scrollTo(0,1400);")
		self.selenium.close()

	'''------------------------------------------------------------------
							Draft Post button
	------------------------------------------------------------------'''
	def test_draft_post_btn(self):
		selenium = self.selenium
		selenium.get("http://127.0.0.1:8000/posts/login")

		username_input = selenium.find_element_by_id("id_username").send_keys("kevin")
		password_input = selenium.find_element_by_id("id_password").send_keys("kevin1234")
		login_click = selenium.find_element_by_name("login").click()

		dashboard_btn = selenium.find_element_by_name("dashboard").click()

		draft_post_btn = selenium.find_element_by_id("draft-post").click()
		self.selenium.execute_script("window.scrollTo(0,document.body.scrollHeight);")
		self.selenium.close()

	'''------------------------------------------------------------------
							Future Post button
	------------------------------------------------------------------'''
	def test_future_post_btn(self):
		selenium = self.selenium
		selenium.get("http://127.0.0.1:8000/posts/login")

		username_input = selenium.find_element_by_id("id_username").send_keys("kevin")
		password_input = selenium.find_element_by_id("id_password").send_keys("kevin1234")
		login_click = selenium.find_element_by_name("login").click()

		dashboard_btn = selenium.find_element_by_name("dashboard").click()

		draft_post_btn = selenium.find_element_by_id("future-post").click()
		self.selenium.execute_script("window.scrollTo(0,document.body.scrollHeight);")
		self.selenium.close()

