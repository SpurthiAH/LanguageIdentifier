# -*- coding: utf-8 -*-

###author: Spurthi Amba Hombaiah
###Predicts which language the test text belongs after computing profile for the test text and comparing this profiles for all languages and selecting the one for which distance is minimum.


from data_parser import Data_parser
from config_reader import Config_reader
from text_file_reader import Text_file_reader
from collections import Counter
import math
import sys
import re

class Language_predictor:
	def predict_language(self, text):
		cr = Config_reader()
		n_gram = cr.get_n_gram()
		n = cr.get_n()
		counts = Counter()
		
		#Replacing numbers in test text
		text = re.sub(r'[0-9]*\.?[0-9]+', r'', text)

		#Counts for n-grams computed for the test text
		for line in text.splitlines():
			for l in line.split('.'):
				length = len(l)
				
				for i in xrange(1, n_gram + 1):
					for j in xrange(0, length - i + 1):
						string = l[j: j + i]
						if string.isspace():
							continue
						counts[string] += 1
	
		distance = dict()
		sel_lang = ''
		min_dist = sys.maxint
		tot_dist = 0

		#Compute distance between text profile and language profiles
		for lang in Data_parser.features.keys():
			dist = 0
			pos = 1
			prev = counts.most_common(1)[0][1]
			for index, item in enumerate(counts.most_common()):
				string = item[0]
				if string in Data_parser.features[lang]:
					if prev < item[1]:
						pos += 1
					dist += int(math.fabs(Data_parser.features[lang][string] - pos))
				else:
					dist += int(n + 1 - pos)
				tot_dist += dist
			if dist < min_dist:
				min_dist = dist
				sel_lang = lang

		#print Text_file_reader.lang_dict[sel_lang]['name'], float(min_dist)/tot_dist
		return Text_file_reader.lang_dict[sel_lang]['name'], float(min_dist)/tot_dist





		

