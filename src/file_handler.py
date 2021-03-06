"""

The module for loading a dataset from a given file and parsing it into a dictionary.
The offered functions allow to receive a list of pairs of samples with their labels

"""

import random


def load_file(file_name, test_file):
	print(file_name);
	sample_folder	= "../samples";
	file_path	= sample_folder + "/" + file_name;
	text_file	= open(file_path, "r");
	lines_of_file	= text_file.read().split('\n');
	loaded_lines	= dict();

	if(test_file == False):
		for i in range(0, len(lines_of_file)):
			elements = lines_of_file[i].split(":::");
			if(elements[0] == ''):
				continue;
			if(len(elements) >= 3):
				elements_structured = (elements[1].encode('utf8'), elements[2].encode('utf8'), file_name[-6:-4].upper());
			else:
				elements_structured = elements[1].encode('utf8');
			loaded_lines[elements[0]] = elements_structured;
	else:
		for i in range(0, len(lines_of_file)):
			elements = lines_of_file[i].split(" ");
			if(elements[0] == '' or len(elements) < 3):
				continue;
			loaded_lines[elements[0]] = ' '.join(elements[2:-1]);
	return loaded_lines;

def load_files_formatted(truth_files, tweet_files):
	if truth_files != None:
		is_test = False;
		truths = []
		for t in truth_files:
			truths = truths + [load_file(t, is_test)];
	else:
		is_test = True;
		#truths = load_file("truth_es.txt", False);

	tweets = []
	for t in tweet_files:
		tweets = tweets + [load_file(t, is_test)];

	formatted_data = [];
	for i in range(len(tweets)):
		for p in tweets[i]:
			if is_test:
				label = (b'AGAINST', b'MALE', 'ES');
			else:
				label = truths[i][p];
			formatted_data.append((tweets[i][p], label, p)); #(tweet, labels, ID)

	return formatted_data


def load_files_formatted_split(truth_files, tweet_files, train_prop = 0.9, test_prop = 0.1):
	data = load_files_formatted(truth_files, tweet_files);

	#random shuffle
	random.seed(0xF12ABC12123); #random, but constant seed
	random.shuffle(data)

	#get proportion and return it
	upper_bound = int(round(len(data) * train_prop))
	
	return (data[:upper_bound],  data[upper_bound:])
