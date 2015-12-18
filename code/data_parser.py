###author: Spurthi Amba Hombaiah
###Parser module for data. Also extracts n-gram features and builds profiles for languages.

import os
from text_file_reader import Text_file_reader
from collections import Counter
from config_reader import Config_reader
import re

class Data_parser:
	features = dict()

	def parse_data(self, lang):
		reader = Text_file_reader()
		counts = Counter()
		cr = Config_reader()
		n = cr.get_n()
		n_gram = cr.get_n_gram()
		path = os.path.dirname(os.getcwd()) + '/data/' + lang + '/'
		#Read every file. Generate n-grams from text and get counts for each and select the top n n-grams as features
		if os.path.isdir(path):
			files = os.listdir(path)
			for fil in files:
				fil_path = path + fil
				data = reader.data_file_reader(fil_path)
				data = re.sub(r'[0-9]*\.?[0-9]+', r'', data)
				for line in data.splitlines():
					line_list = line.split(".")
					for l in line_list:
						length = len(l)
						for i in xrange(1, n_gram + 1):
							for j in xrange(0, length - i + 1):
								string = l[j: j + i]
								if string.isspace():
									continue
					
								counts[string] += 1
								
		self.features[lang] = dict()
		prev = counts.most_common(1)[0][1]

		rank = 1
		#After choosing top n n-grams, assign a rank depending on their frequency of occurrence in the text of that particular language.
		for item in counts.most_common(n):
			if prev < item[1]:
				rank += 1
				prev = item[0]
			self.features[lang][item[0]] = rank




							



