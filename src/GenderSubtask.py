"""

Module for realizing the stance subtask. With optional command line arguments, see below.

"""

#import own modules
import file_handler;
import pipelineFunctions;
import classifier;
import evaluator;

from classifier import ClassificationPipeline;

#other modules
import sys;

import nltk
from nltk.classify import MaxentClassifier


def load_data(tweet_files, truth_files):
	print("> Loading data..." +  str(tweet_files) + " and " + str(truth_files));
	
	if not no_training:
		data = file_handler.load_files_formatted_split(truth_files, tweet_files, 0.9, 0.1);
	else:
		data = file_handler.load_files_formatted_split(truth_files, tweet_files, 1- test_prop, test_prop); #all data test
	
	print("< Loaded data successfully");

	return data;


def setup_pipeline(data):
	print("> Instantiating pipeline...");
	pipeline = ClassificationPipeline();

	pipeline.setTokenizer(pipelineFunctions.tokenizer_gender2());
	pipeline.setCleaner(pipelineFunctions.cleaner_gender2());
	pipeline.setFeatureEx(pipelineFunctions.featureEx_stance2(not no_espanol));

	if not no_training:
		pipeline.setClassifier(MaxentClassifier);
		pipeline.setLabelSelection(pipelineFunctions.labelSelection_gender2());
	else:
		pipeline.loadClassifierFromFile(classifierFile);	

	pipeline.setData(data);

	print("< Instantiated pipeline successfully")
	return pipeline;

def apply(data, classifier):
	#we assume that the labels are still given in the data, so (feat, (labels)) structure
	print("> Classifying data using classifier");	
	result = [];
	indexkeymap = dict();	

	i = 0;
	for (inst, labels, key) in data:
		result = result + [classifier.classify(inst)];
		indexkeymap[i] = key;
		i = i + 1;
	
	print("> Successfully classified instances.");
	return (result, indexkeymap);


def print_result(data, result, indexkeymap, labelindex):
	print("> Printing result to file");
	
	print_str = "";
	for i in range(len(result)):
		result_str =  result[i].decode('utf8');
		print_str += indexkeymap[i] + "\t0\t0\t"
		print_str += str(result_str) + "\n"
		#print_str += data[i][0] + "\n";

	open_name = "../resultados/test/result_gender_" + classifierFile;
	if not no_catalan:
		open_name += "CA";

	if not no_espanol:
		open_name += "ES";

	wfile = open(open_name, "w");
	wfile.write(str(print_str));
	wfile.close();

	#wfile = open(open_name + "_GOLD", "w");
	#for s in gold_str:
	#	wfile.write(str(s.encode('utf8')));

	#wfile.close();


def main():
	print("###### GENDER SUBTASK ######");
	global no_espanol;
	global no_catalan;
	global no_training;
	global classifierFile;
	global test_prop;

	if len(sys.argv) > 1:
		print("Starting the task with the following configuration:");
		
		if sys.argv[1] == "-CA":
			no_espanol = True;
			print("ONLY CATALAN");
		elif sys.argv[1] == "-ES":
			no_catalan = True;
			print("ONLY ESPANOL");
		elif sys.argv[1] == "-ALL":
			print("BOTH LANGUAGES");
		else:
			print("INVALID LANUGAGE CONFIG - default with ES and CA");

	if len(sys.argv) > 2:
		classifierFile = sys.argv[2];
		no_training = True;
		print("LOADING CLASSIFIER " + classifierFile + " - RUN AS TEST EVAL");

	if len(sys.argv) > 3:
		test_prop = float(sys.argv[3]);
		print("WITH TEST SPLIT " +  str(test_prop));

	tweet_files = [];
	truth_files = [];		

	if not no_catalan:
		if False:#no_training:
			tweet_files = ["test_samples/GenderCa"]
			truth_files = None
		else:
			tweet_files = tweet_files + ["tweets_ca.txt"];
			truth_files = truth_files + ["truth_ca.txt"];

	if not no_espanol:
		if False:#no_training:
			tweet_files = ["test_samples/GenderEs"]
			truth_files = None
		else:
			tweet_files = tweet_files + ["tweets_es.txt"];
			truth_files = truth_files + ["truth_es.txt"];
		
	data = load_data(tweet_files, truth_files);

	if not no_training:
		pipeline = setup_pipeline(data[0]);
	else:
		pipeline = setup_pipeline(data[1]);

	pipeline.preprocess();

	if not no_training:
		pipeline.train();
		pipeline.storeClassifierInFile(classifierFile);
		print("### TRAINED AND STORED CLASSIFIER (in " +  classifierFile + ")");
	else:
		res = apply(pipeline.getProcessedData(), pipeline.getClassifier());
		print_result(data[1], res[0], res[1], 1);
		
		evaluator.evaluateMultilabel(res[0], pipeline.getProcessedData(), 1);

#call main
no_catalan = False;
no_espanol = False;

test_prop = 0.1;

no_training = False;
classifierFile = "basic1_gender_all";
	
main();
