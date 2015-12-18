###author: Spurthi Amba Hombaiah
###Data collector, cleaner module. Also generates seeds for further generation of data.

from config_reader import Config_reader
from data_queue import Queue
from text_file_reader import Text_file_reader
from file_writer import File_writer
import os
import requests
import json
import threading
import re
import random

class Data_collection:
	lock = threading.RLock()

	def clean_text(self, text):
		#Extract only paragraphs in html page 
		#Remove any existing numbers in the text and keep only characters
		processed_text = ''
		for line in text.split('\n'):
			if line.startswith('<p>') and line.endswith('</p>'):
				line = re.sub(r'</?[^>]+>', r'', line.strip())
				line = re.sub(r'[0-9]*\.?[0-9]+', r'', line)
				processed_text += line.strip()
		return processed_text

	def get_new_seeds(self, text):
		#Extract anything italicized in the html page as a new seed for further scraping
		new_seed = set()
		pattern = re.compile(r'<i>[^>]+</i>')
		for line in text.split('\n'):
			matches = pattern.findall(line)
			for m in matches:
				new_seed.add(m[3:-4])
		return new_seed

	def get_more_seeds(self, text):
		#Generate more seeds by considering each word (tokenizing) as a new seed for further scraping. 
		#This method was implemented because random seeding/extracting random seeds from text didn't lead to pages which returned results. So together with text within
		#italicized blocks, each word which hadn't been considered as a seed before is considered for further scraping of pages belonging to a language.
		new_seed = set()
		word_list = text.split()
		for w in word_list:
			if w != '':
				w = re.sub(r'[^a-zA-Z].*', r'', w)
				new_seed.add(w)
		return new_seed


	def parse_page(self, page_url, seed, page_seed):
		#API request to wikipedia page
		data = {'action': 'query', 'prop': 'extracts', 'format': 'json', 'titles': seed.encode('utf-8')}
		resp = requests.post(page_url, params = data)
		res = resp.json()
		text = ''
		try:
			text = res['query']['pages'].values()[0]['extract'].encode('ascii', 'ignore').encode('utf-8')
		except:
			print 'No data for seed - ', seed
			pass
		processed_text = self.clean_text(text)
		#Get seeds for further scraping of pages
		new_seed1 = self.get_new_seeds(text)
		new_seed2 = self.get_more_seeds(processed_text)
		text = ''
		new_seed = new_seed1.union(new_seed2)
		return list(new_seed), processed_text

	def get_data(self, lang, filenum):
		unique_seeds = set()
		seed_queue = Queue(lang)
		cr = Config_reader()
		http = cr.get_http()
		url_ = cr.get_url()
		url = http + lang + url_
		init_seed = cr.get_init_seed()
		text_size = 0
		unique_seeds.add(init_seed)
		seed_queue.add_element(init_seed)
		path = os.path.dirname(os.getcwd()) + '/data/' + lang + '/'
		page_seed = cr.get_page_seed()
		
		while seed_queue.size > 0 and text_size < filenum:
			seed = seed_queue.pop_element()
			#Call to parse webpage
			new_seed, text = self.parse_page(url, seed, page_seed)
			
			for s in new_seed:
				#Add seeds to seed queue
				if s not in unique_seeds:
					seed_queue.add_element(s)
					unique_seeds.add(s)
			
			if text != '':
				#If webpage returned consists of data, write it to a file
				text_size += 1
				wr = File_writer()
				wr.write_file(text, path, text_size, '.gz')
			new_seed = []
			text = ''
		

		





	






