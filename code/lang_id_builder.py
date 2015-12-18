###author: Spurthi Amba Hombaiah
###Driver module which calls data collector, data parser.

from config_reader import Config_reader
from data_queue import Queue
from text_file_reader import Text_file_reader
from file_writer import File_writer
from data_collection import Data_collection
from data_parser import Data_parser
import os
import requests
import json
import threading
import re
import random

class Lang_id_builder:
	def builder(self, lang):
		#Get configuration parameters
		cr = Config_reader()
		non_latin_scripts = cr.get_non_latin_scripts()

		#Check directory for latin scripts
		if lang not in non_latin_scripts:
			filenum = cr.get_pages()
			dir_name = os.path.dirname(os.getcwd()) + '/data/' + lang
			if os.path.isdir(dir_name):
				files = os.listdir(dir_name)
				#Check size of directory. If it is same as file size, move onto parser method
				if len(files) == filenum:
					pass
				else:
					#If size of directory is less than defined file size, delete files and populate data again (collect new pages)
					for fil in files:
						path = dir_name + '/' + fil
						os.remove(path)
					#Call data collector module
					dc = Data_collection()	
					dc.get_data(lang, filenum)
			else:
				#Create directory if it doesn't exist
				os.makedirs(dir_name) 
				#Call data collector module
				dc = Data_collection()	
				dc.get_data(lang, filenum)

		#Call parser function
		parser = Data_parser()
		parser.parse_data(lang)