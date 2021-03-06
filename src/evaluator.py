"""

"""

import nltk
import collections
from collections import Counter

def evaluate(result, data):
	data = [x[1] for x in data];
	res = nltk.ConfusionMatrix(result, data);
	print(res.pretty_format(sort_by_count=True, show_percents=True, truncate=9));

def evaluateMultilabel(result, data, label_index):	
	data = [l[label_index] for (f, l, i) in data]
	
	cm = nltk.ConfusionMatrix(result, data);	

	print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))

	print_accuracy_per_label(cm, data);
	print_macro_f1_per_label(cm, data);

def print_accuracy_per_label(cm, data):
	labels = set(data);

	true_positives = Counter();
	false_negatives = Counter();
	false_positives = Counter();

	for i in labels:
		for j in labels:
			if i == j:
		    		true_positives[i] += cm[i,j];
			else:
		    		false_negatives[i] += cm[i,j];
		    		false_positives[j] += cm[i,j];

	print("TP:", sum(true_positives.values()), true_positives);
	print("FN:", sum(false_negatives.values()), false_negatives);
	print("FP:", sum(false_positives.values()), false_positives);	

def print_macro_f1_per_label(cm, data):
	labels = set(data);
	
	true_positives = Counter();
	false_negatives = Counter();
	false_positives = Counter();

	for i in labels:
		for j in labels:
			if i == j:
		    		true_positives[i] += cm[i,j];
			else:
		    		false_negatives[i] += cm[i,j];
		    		false_positives[j] += cm[i,j];

	
	precision = dict();
	recall = dict();
	f1_score = dict();	

	for l in labels:
		precision[l] = float(true_positives[l]) / float(true_positives[l] + false_positives[l] + 0.00001);
		recall[l] = float(true_positives[l]) / float(true_positives[l] + false_negatives[l] + 0.00001);
		f1_score[l] = float(2 * precision[l] * recall[l]) / float(precision[l] + recall[l] + 0.00001);
		print("For " + str(l) +":");
		print("Precision: " + str(precision[l]));
		print("Recall: " +  str(recall[l]));
		print("F1: " + str(f1_score[l]));
	
	
	
	
