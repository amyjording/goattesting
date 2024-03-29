from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()
	
	#helper function
	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		#Amy wants to create another to-do for her list and goes to
		# the following homepage to add her next item.
		self.browser.get(self.live_server_url)

		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# She is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
			)

		# She types 'Choreograph a dance' because she has plans later in the summer.
		# WHen she hits enter, the page updates, and now the page lists
		# "1: Choreograph a dance" as an item in a to-do list.
		inputbox.send_keys('Choreograph a dance')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Choreograph a dance')


		# There is still a text box inviting her to add another item. She
		# enters "Practice the dance each Sunday"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Practice the dance each Sunday')
		inputbox.send_keys(Keys.ENTER)

		# The page updatesybuttest again, and shows both items on her list

		self.wait_for_row_in_list_table('1: Choreograph a dance')
		self.wait_for_row_in_list_table('2: Practice the dance each Sunday')

		self.fail("Finish the test!")

		# Amy wonders about the site remembering her list, and notices that
		# the site generated a unique url for her and text that tells her about it.

		# She visits that URL - her to-do list is still there.

		# Satisfied, she goes back to sleep
