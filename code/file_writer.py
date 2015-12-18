###author: Spurthi Amba Hombaiah
###Write to gzip files

import gzip

class File_writer:
	def write_file(self, text, path, index, compression):
		filename = path + str(index) + compression
		if compression == '.gz':
			fil = gzip.open(filename, 'wb')
		fil.write(text)
		fil.close()