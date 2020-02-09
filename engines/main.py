import sys, json
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules

class Engine:
	def __init__(self, file_name):
		self.file_name = file_name
		self.json_out = {}
		self.dataset = pd.read_csv((file_name))

	def strategy(self):
		dataset = self.dataset
		sample_size = len(dataset)
		if sample_size < 50:
			print("More Data")
		else:
			if predicting_category & labeled_data:
				print("Classification: \n")
				if sample_size < 100000:
					print("Linear SVC \n")
					print("Doesn't work?")
					if text_data:
						print("Naive Bayes \n")
					else: 
						print("KNN \n")
						print("Doesn't work? SVC or Ensemble")
				else:
					print("SGD Classifier \n")
					print("Doesn't work? kernel approximation \n")
			elif predicting_category:
				print("Clustering: \n")
				if categories_known & sample_size < 10000:
					print("Kmeans \n")
					print("Doesn't work? Spectral Clustering or GMM")
				elif categories_known:
					print("MiniBatch Kmeans")
				elif sample_size < 10000:
					print("Mean Shift or VBGMM")
				else:
					print("though luck")
			elif predicting_quantity:
				print("REgression: \n")
				if sample_size < 100000:
					print("SGD Regressor")	
				elif few_features_are_important:
					print("Lasso or Elastic Net")
				else:
					print("Ridge Regression or SVR (kernel = linear)\n")
					print("Doesn't work? SVR (kernel = rbf)")					
			elif just_looking:
				print("Dimentionality Reduction")
				if sample_size < 10000:
					print("Iso map or Spectral Embedding \n")
					print("Doesn't work? LLE")
				else:
					print("Kernel Approximation")
			else:
				print("Good luck!")





class Appriori:
	'''
		file_name: client file to be processed
		json_out : ouput json object to be send to client
	'''
	def __init__(self, file_name):
		self.file_name = file_name
		self.json_out = {}
		self.dataset = pd.read_csv((file_name))

	def bin_this_df(self, df):#qcut each feature. 
        temp_dataset = dataset.copy()
        for column in temp_dataset.columns:
            def helper(x):
                return column + ":"+ x
            try:	
                temp_dataset.loc[:,column] = pd.qcut(temp_dataset.loc[:,column], q = 4)
            except Exception as e:
                pass
            finally:
                temp_dataset.loc[:,column] = temp_dataset.loc[:,column].apply(str)
                temp_dataset.loc[:,column] = temp_dataset.loc[:,column].apply(helper)
        return temp_dataset

	def apriori(self):
		temp_df = self.bin_this_df(self.dataset)
		data_list = temp_df.to_numpy()     
		te = TransactionEncoder()
		te_ary = te.fit(data_list).transform(data_list)
		te_ary_df = pd.DataFrame(te_ary, columns=te.columns_)
		min_support = 0.1
		frequent_itemsets = apriori(te_ary_df, min_support= min_support, use_colnames=True)
		while (len((frequent_itemsets)) < 20) & (min_support > 0.04):
			if min_support == 0.1:
				min_support -= 0.01
			else:
				min_support -= 0.1
			frequent_itemsets = apriori(te_ary_df, min_support= min_support,  use_colnames=True)
		return frequent_itemsets

	def assoc_rules(self, frequent_itemsets):
        min_threshold = 0.9
        assoc_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_threshold)
        while (len((assoc_rules)) < 10) & (min_threshold > 0.04):
            if min_threshold == 0.1:
                min_threshold -= 0.01
            else:
                min_threshold -= 0.1
            assoc_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_threshold)
		assoc_rules.itemsets = assoc_rules.itemsets.apply(list)
		return assoc_rules
#print((dataset.describe()).to_json())

def main():
	assert len(sys.argv) > 1
	filename = sys.argv[1]
	engine = Engine(filename)
	exit()

if __name__ == "__main__":
	main()	