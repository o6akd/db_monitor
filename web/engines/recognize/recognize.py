import sys, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
'''
						
TODO:
 - Prepare a training dataset
 - Train the ML and test.
 - Deploy
'''

class Recognize: #Recognize the data types
	def __init__(self,df):
		self.df = df

	#TODO: Split each text to feature columns 
	# is a number > splitting criterion has ./- > create ascii feaures > add variance feautures > mod feature 
	# if has ./- is this a date? Use ascii 
	#label
	#train
	#test
	def make_table(self): #transform source file 
		ascii_list = []
		for char in range(33,127):
			ascii_list.append(chr(char))
		def encoder( column): #transform column rows to lists of 1's and 0's depending on if a character is in ascii list. 
			source_data = self.df
			def split_map(word, mean, column):
				charList = list(word)
				mapped_list = list(map(lambda x: x in charList, ascii_list))
				to_return = np.concatenate([(np.array(mapped_list)).astype(int), np.array([mean,column])])
				return to_return
			mean = "none"
			encoded_list = []
			if type(source_data.loc[1,column]) == str:
				encoded_list = list(map(lambda word: split_map(str(word), mean, (column)) , source_data.loc[:,column] ) )
				rows.append(encoded_list)
			else:
				try:
					mean = source_data.loc[:,column].std()
					encoded_list = list(map(lambda word: split_map(str(word), int(mean), (column)) , source_data.loc[:,column]))
					rows.append(encoded_list)
				except:
					return None
			return rows[0]
		source_data = self.df
		rows = []
		for column in source_data.columns:
			rows.append(encoder(column))
		ascii_list = ascii_list + ['mean_val','label']
		one_hot_df = pd.DataFrame(np.array(rows[0]), columns = ascii_list)
		return one_hot_df

df = pd.read_csv("../training_data/dates.csv")
x = Recognize(df).make_table()
print(x.head())
exit()
	#x = re.findall(r"([0-3][0-9]|[0-9])[/:.-]{1}([0-9]{2})[/:.-]{1}([0-9]{4})","32/14-2000")