# LanguageIdentifier

Introduction
Language identifier system predicts the language a given text belongs to by computing dissimilarity between the
provided text and sample corpus from different languages. Language identifier is available as a web-based service
and making an API call to the system returns the language the text is most likely associated with along with the
dissimilarity.
This language system is based on n-gram based text classification in which text is broken up into strings of lengths 1
to n by grouping consecutively occurring characters together. n-gram is a string which consists of consecutive
characters with its length ranging from 1 to n constructed from a text/corpus. This forms a n-gram profile for the
test text. n-gram profiles for languages supported are constructed by using corpus collected for these languages. For
making a prediction, n-gram profile of the test text is compared to the n-gram profiles of languages by computing
distance between the language profile and text profile in terms of difference in position of a n-gram occurring in
language and text profiles. If a n-gram occurring in text profile doesn’t occur in language profile, then a default
maximum rank is considered for that n-gram.

Languages Supported
Currently, 25 languages are supported by this system out of which 19 use Latin scripts and 6 use non-Latin scripts.

English,en
Francais,fr
Dansk,da
Deutsch,de
Portugues,pt
Latina,la
Bahasa Indonesian,id
Afrikaans,af
Galego,gl
Catala,ca
Polski,pl
Suomi,fi
Turkce,tr
Lietuviu,lt
Euskara,eu
Magyar,hu
Hrvatski,hr
Bahasa Melayu,ms
Eesti,et
Hindi,hi
Bengali,bn3.
Malayalam,ml
Tamil,ta
Telugu,te
Urdu,ur

System Architecture

HTTP Post
Initially, a Post request is made with the test text through an API call to the application.Multi-threaded Execution
Multiple threads are kicked off one for each language which is supported by the system. Each thread is responsible
for handling data collection, data cleaning, data storage, parsing and building profile for that particular language.

Data Collection
1. Web Scraping for languages using Latin script
Our system supports 19 languages which use Latin script.
Each thread makes an API call to a Wikipedia page for a particular language with initial seed as ‘Linux’. This
seed can be changed as required. The selection of initial seed affects the kind and amount of data collected.
It’s recommended to use a proper noun as an initial seed because the way the word is spelt wouldn’t change
across different languages. After getting a webpage, to generate new seeds, text appearing within italicized
blocks (those appearing between \<i> and \</i>) are extracted. Sometimes, these blocks of text as seeds don’t
return relevant results (they don’t have a corresponding webpage associated with them). So every unique
word appearing in the webpage is considered as a new seed for further scraping of data. Every time, only
unique seeds are considered for further data collection. On obtaining data for a webpage, only text
appearing within paragraphs are extracted (those appearing within \<p> and \</p>) and stored in the form
of .gz files in the corresponding language folder. Currently, we collect 1000 files for every language which
uses Latin script. This can be changed as needed.
This process takes a long time as seeds don’t generate relevant results often. After trying to generate
random seeds from webpage text, I decided on this approach as this would ensure obtaining the required
amount of data. Random seeding would terminate the process prematurely and the data collected would
be too less for the process.

2. Online resources for languages using non-Latin script
Our system supports 6 languages which use non-Latin script. These are mainly Indian languages which use
the following scripts:
Hindi – Devanagari
Malayalam, Tamil, Telugu, Bengali – Brahmi
Urdu – Abjad
I tried scraping data for these languages from their corresponding Wikipedia pages but the process didn’t
yield good results. Hence, this data was obtained from an online repository for Indian languages -
http://joshua-decoder.org/data/indian-parallel-corpora/ . We use only dev and devtest files which are
provided for each language as other files are not useful for our purpose.

3. Complete Data Corpus
We build a comprehensive data corpus by combining data for Latin-scripted and non-Latin scripted
languages. Files belonging to a particular language can be found under the directory belonging to that
particular language.Data Cleaning and Parsing
Data is cleaned to remove any numbers that may be contained in the text. Data from all files belonging to a language
is considered. This data is parsed to generate n-grams. This value of n can be changed as required. Each line in the
text is parsed and all substrings of length starting from 1 to n are generated.
Profile Building for Languages and Test Text
Counts are obtained for the generated n-grams and top n n-grams are chosen as the feature set for the language.
This n can be changed and in our system, it is set as 1000. This value affects the performance of the system. Each n-
gram is associated with a rank depending on its frequency of occurrence. n-gram with the highest frequency gets
the lowest rank. If there are multiple n-grams with the same frequency, then all of them are given the same rank.
Test text is also parsed and all n-grams are generated for this. For test text, ranks are given to n-grams as described
above.

Profile Comparison
Profile of the test text is compared with the profiles of different languages by computing the distance between ranks
for each n-gram in the test text with the corresponding n-gram in the profile for the language. If the n-gram isn’t
present in the language profile, then it is assigned a maximum rank of n + 1. For computing distance, absolute
differences are computed and summed up over all n-grams.
Finally, the language whose profile is least dissimilar is returned as the most probable language to which the text
might belong. The profile for this language basically has the least distance from the profile computed for the test
text. The final minimum distance is normalized over distances for all languages and returned along with the language.

API Specification
Call to the system should be as follows:
API call:
curl http://localhost:5000/lang_id -d "text=Machine Learning and Natural Language Processing are some of the
hottest fields in Computer Science currently." -X POST –v
Result:
{
"English":0.00016288295592749175
}
This makes a POST request to the Language Identifier web-service which computes the degree of association of the
text with the languages supported and returns the language the text is most likely associated with along with the
distance computed between the profiles constructed for text and supported languages.

Source code
There are 3 folders – code, data and config .
1. Code folder consists of all the source code for the project.
  a. lang_ip_api.py – web application for posting request from the user
  b. language_identifier.py – starts threads for processing data for different languages
  c. lang_id_builder.py – driver module from where calls are made to data collector, data parser and
     predictor modules
  d. config_reader.py – module for reading configuration file
  e. text_file_reader.py – module for reading text files and gz files
  f. file_writer.py – module for writing gz files
  g. data_collection.py – module for data collection by making calls to Wikipedia pages and data cleaning
  h. data_parser.py – module for parsing data collected and building features/profiles for languages
  i. data_queue.py – customized queue implementation
  j. predictor.py – predicts the language a given text belongs to by computing the distance between the
           profiles for text and languages supported

2. Data folder consists of data collected for different languages. Each data folder is named after the two letter
  ISO code for the language. Data for languages which use Latin script is collected by making calls to Wikipedia
 pages. This consists of 1000 .gz files. Data for languages which use non-Latin script has been obtained from
online resources. These folders consist of only 2 .gz files.
Non-latin script languages supported by the system are Indian languages and this data was obtained from
an online repository for Indian languages. Link: http://joshua-decoder.org/data/indian-parallel-corpora/ .
This dataset consists of original text and translated text in English. Only two original texts named dev and
devtest are used for training our system. Even this data has been provided.

3. Config folder consists of configuration files used in the system. These files consists of configuration
  parameters for the system.
 a. languages.txt – Lists all the languages supported by the system. If any new language needs to be
  supported, this should be added here.
 b. config.properties – defines configurable parameters like base url, number of pages to be downloaded
  for each language, n_gram size, init_seed for web scraping, feature size, non-Latin scripts that are
 supported. These properties can be changed without making any modifications to the source code.
All the source code, data and configuration files have been zipped and attached as a part of the email. Also, the
entire project has been uploaded on GitHub.
The whole process can be run end-to-end after deleting folders from Data folder expect for those belonging to Non-
Latin scripts - bn, hi, ml, ta, te and ur. Please do not delete these folders as we don’t collect data for these languages.

Testing
For testing the system, please run the application (on command line) as follows:
Go to code folder under LanguageIdentifier. This is required as we use the directory path for finding configuration
files and reading data files.cd ./LanguageIdentifier/code/
Run the following command
python lang_id_api.py
To make an API call, execute the curl command (command line). This will make a POST request to the web application
and return results.
The whole process can be run end-to-end after deleting folders from Data expect for those belonging to non-Latin
scripts bn, hi, ml, ta, te and ur. Please do not delete these folders as we don’t collect data for these languages.
Data collection takes a long time. If you want to avoid waiting, please don’t delete data folders for languages.
