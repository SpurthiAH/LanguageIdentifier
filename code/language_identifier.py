###author: Spurthi Amba Hombaiah
###Drive module which kicks-off threads for processing different languages

from text_file_reader import Text_file_reader
from config_reader import Config_reader
from data_collection import Data_collection
from threading import Thread
from lang_id_builder import Lang_id_builder
from data_parser import Data_parser
from predictor import Language_predictor
import time

class Language_identifier:
	def __init__(self):
		self.lang_file = 'languages.txt'
		self.config_file = 'config.properties'

	def setup(self):
		tr = Text_file_reader()
		tr.lang_file_reader(self.lang_file)

	def driver(self, test_text):
		self.setup()
		lb = Lang_id_builder()
		cr = Config_reader()
		lang_dict = Text_file_reader.lang_dict
		langs = lang_dict.keys()
		delay = cr.get_delay()
		threads = []
		#For every language kick-off a thread which will handle data collection, cleaning, parsing, feature building for that language
		for lang in langs:
			t = Thread(target=lb.builder, args=[lang], kwargs=None)
			print "Starting ", lang, "\n\n"
			threads.append(t)
			t.start()
			time.sleep(delay)

		for t in threads:
			t.join()

		#Call to the predictor module
		predict = Language_predictor()
		language, distance = predict.predict_language(test_text)

		return language, distance