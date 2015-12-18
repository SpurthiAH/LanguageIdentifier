# -*- coding: utf-8 -*-

###author: Spurthi Amba Homabaiah
###Reader for language file and gzip file

import os
import gzip

class Text_file_reader(object):
	lang_dict = dict()

	def lang_file_reader(self, csv_file):
		csv_path = os.path.dirname(os.getcwd()) + '/config/' + csv_file
		r = open(csv_path)
	
		for line in r:
			[name, code] = line.split(',')
			name = name.strip()
			code = code.strip()
			self.lang_dict[code] = dict()
			self.lang_dict[code]['name'] = name
		r.close()

	def data_file_reader(self, path):
		r = gzip.open(path, 'rb')
		data = r.read()
		r.close()
		return data.decode('utf-8')


		