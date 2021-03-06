"""

Here the functions for the pipeline are defined.

"""
from nltk.tokenize.toktok import ToktokTokenizer
from nltk import FreqDist;


#define tokenizer
def tokenizer1():
	toktok = ToktokTokenizer();

	def exToken(data):
		res = [];
		for d in data:
			res = res + [(toktok.tokenize(d[0]), d[1][0])]; #change here the second number for gender/stance

		return res;

	return exToken;

def cleaner1():
	return lambda x : x;

def featureEx1():
	def featex(data):
		res = [];
		for d in data:
			feat_dict = {};

			for w in d[0]:
				feat_dict[w] = 1;

			res = res + [(feat_dict, d[1])];

		return res;

	return featex;



####################GENDER#######################

def tokenizer_gender():
	toktok = ToktokTokenizer();

	def exToken(data):
		res = [];
		for d in data:
			res = res + [(toktok.tokenize(d[0]), d[1][1])];

		return res;

	return exToken;
def cleaner_gender():
	return lambda x : x;

def featureEx_gender():
	def featex(data):
		res = [];
		for d in data:
			feat_dict = {};

			for w in d[0]:
				feat_dict[w] = 1;
			
			res = res + [(feat_dict, d[1])];

		return res;

	return featex;

def tokenizer_gender2():
	toktok = ToktokTokenizer();

	def exToken(data):
		res = [];
		for d in data:
			res = res + [(toktok.tokenize(d[0]), d[1], d[2])]; 

		return res;

	return exToken;

def cleaner_gender2():
	return lambda x : x;

def featureEx_gender2():
	name = "espanol"
	file = open("../corpora/"+name+"_stopwords.txt");
	stop_words = set();
	for l in file:
		stop_words.add(l.lower());
	
	name = "catalan"
	file = open("../corpora/"+name+"_stopwords.txt");
	for l in file:
		stop_words.add(l.lower());
	def featex(data):
		res = [];
		for d in data:
			feat_dict = {};

			letter_count = 0;
			word_count = 0;
			feat_dict["os"] = 0;
			feat_dict["as"] = 0;
			for w in d[0]:
				if(w.lower() in stop_words):
					continue;
				letter_count += len(w);
				
				if (not w + "_count" in feat_dict):
					feat_dict[w + "_count"] = 0;
				feat_dict[w + "_count"] += 1;
				feat_dict[w] = 1;
				if(w[-1] == "a"):
					feat_dict["as"] += 1;
				elif(w[-1] == "o"):
					feat_dict["os"] += 1;

			feat_dict["word count"] = len(d[0]);
			feat_dict["average letter length"] = letter_count // len(d[0]);

			res = res + [(feat_dict, d[1], d[2])];

		return res;

	return featex;

def labelSelection_gender2():
	def labelsec(data):
		return [(d[0], d[1][1]) for d in data];

	return labelsec;

#####################STANCE########################
def tokenizer_stance():
	toktok = ToktokTokenizer();

	def exToken(data):
		res = [];
		for d in data:
			res = res + [(toktok.tokenize(d[0]), d[1][0])]; 

		return res;

	return exToken;
def cleaner_stance():
	return lambda x : x;

def featureEx_stance():
	def featex(data):
		res = [];
		for d in data:
			feat_dict = {};

			for w in d[0]:
				feat_dict[w] = 1;
			
			res = res + [(feat_dict, d[1])];

		return res;

	return featex;

"""
Vol. 2
"""

def tokenizer_stance2():
	toktok = ToktokTokenizer();

	def exToken(data):
		res = [];
		for d in data:
			res = res + [(toktok.tokenize(d[0]), d[1], d[2])]; 

		return res;

	return exToken;

def cleaner_stance2():
	return lambda x : x;

def featureEx_stance2(is_espanol):
	if(is_espanol):
		name = "espanol"
	else:
		name = "catalan"

	file = open("../corpora/"+name+"_stopwords.txt");
	stop_words = set();
	for l in file:
		stop_words.add(l.lower());

	def featex(data):
		res = [];
		for d in data:
			feat_dict = {};

			letter_count = 0;
			word_count = 0;
			feat_dict["os"] = 0;
			feat_dict["as"] = 0;
			for w in d[0]:
				if(w.lower() in stop_words):
					continue;
				letter_count += len(w);
				
				if (not w + "_count" in feat_dict):
					feat_dict[w + "_count"] = 0;
				feat_dict[w + "_count"] += 1;
				feat_dict[w] = 1;
				if(w[-1] == "a"):
					feat_dict["as"] += 1;
				elif(w[-1] == "o"):
					feat_dict["os"] += 1;

			feat_dict["word count"] = len(d[0]);
			feat_dict["average letter length"] = letter_count // len(d[0]);

			res = res + [(feat_dict, d[1], d[2])];

		return res;

	return featex;

def featureEx_stance3(is_espanol):
	def featex(data):
		res = [];
		for d in data:
			feat_dict = {};

			letter_count = 0;
			word_count = 0;
			feat_dict["os"] = 0;
			feat_dict["as"] = 0;
			feat_dict["hashtags"] = 0;
			feat_dict["addresses"] = 0;
			feat_dict["num!"] = 0;
			for w in d[0]:
				word = w.lower();
				letter_count += len(w);
				
				if(word[-1] == "a"):
					feat_dict["as"] += 1;
				elif(word[-1] == "o"):
					feat_dict["os"] += 1;

				if(word[0] == "#"):
					feat_dict["hashtags"] += 1;
					
				if(word[0] == "@"):
					feat_dict["addresses"] += 1; 

				for l in w:
					if l == "!":
						feat_dict["num!"] += 1;

				feat_dict[word[0] + "*" * (len(word)-1)] = 1;
				

			feat_dict["word count"] = len(d[0]);
			feat_dict["average letter length"] = letter_count // len(d[0]);

			res = res + [(feat_dict, d[1], d[2])];

		return res;

	return featex;

def featureEx_stance2_vol2():
	def featex(data):
		res = [];
		
		for d in data:
			fdist = FreqDist(w.lower() for w in d[0]);
			words = fdist.most_common(100)[5:];

			feat_dict = {w : fdist[w] for w in words};
			
			res = res + [(feat_dict, d[1], d[2])];

		return res;

	return featex;

def labelSelection_stance2():
	def labelsec(data):
		return [(d[0], d[1][0]) for d in data];

	return labelsec;
	

