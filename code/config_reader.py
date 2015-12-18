###author: Spurthi Amba Hombaiah
###Reader for configuration file

import ConfigParser
import os

class Config_reader(object):
	url = ''
	http = ''
	seed = 0
	pages = 0
	delay = 0
	page_seed = 0
	n_gram = 0
	max_trys = 0
	min_len = 0
	default_seed = []
	init_seed = ''
	n = 0
	non_latin_scripts = set()
	
	config_file = 'config.properties'
	config_parser = ConfigParser.RawConfigParser()
	config_file_path = os.path.dirname(os.getcwd()) + '/config/' + config_file
	config_parser.read(config_file_path)

	#Seed url
	def get_url(self):
		self.url = self.config_parser.get('config_file', 'url')
		return self.url

	#HTTP protocol
	def get_http(self):
		self.http = self.config_parser.get('config_file', 'http')
		return self.http

	def get_seed(self):
		self.seed = int(self.config_parser.get('config_file', 'seed'))
		return self.seed

	#Number of pages to be retrieved
	def get_pages(self):
		self.pages = int(self.config_parser.get('config_file', 'pages'))
		return self.pages

	#Delay in kicking off threads
	def get_delay(self):
		self.delay = int(self.config_parser.get('config_file', 'delay'))
		return self.delay

	def get_page_seed(self):
		self.page_seed = int(self.config_parser.get('config_file', 'page_seed'))
		return self.page_seed

	#Maximum length of n-grams
	def get_n_gram(self):
		self.n_gram = int(self.config_parser.get('config_file', 'n_gram'))
		return self.n_gram

	def get_max_trys(self):
		self.max_trys = int(self.config_parser.get('config_file', 'max_trys'))
		return self.max_trys

	def get_min_len(self):
		self.min_len = int(self.config_parser.get('config_file', 'min_len'))
		return self.min_len

	def get_default_seed(self):
		default_seed_string = self.config_parser.get('config_file', 'default_seed')
		self.default_seed = [val.strip() for val in default_seed_string.split(',')]
		return self.default_seed

	#Initial seed for web parsing
	def get_init_seed(self):
		self.init_seed = self.config_parser.get('config_file', 'init_seed')
		return self.init_seed

	#Number of features to be considered for building the profile
	def get_n(self):
		self.n = int(self.config_parser.get('config_file', 'n'))
		return self.n

	#Non-Latin scripts which are supported
	def get_non_latin_scripts(self):
		non_latin = self.config_parser.get('config_file', 'non_latin_scripts')
		non_latin_list = [val.strip() for val in non_latin.split(',')]
		self.non_latin_scripts = set(non_latin_list)
		return self.non_latin_scripts
		
		
		
		
		
		
		
		
		
		




			

