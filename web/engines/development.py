import sys, json
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder

filename = sys.argv[1]
dataset = pd.read_csv((filename))

#describe has max min mean etc. 

#qcut each feature. 

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



data_list = temp_dataset.to_numpy()     
te = TransactionEncoder()
te_ary = te.fit(data_list).transform(data_list)
df = pd.DataFrame(te_ary, columns=te.columns_)

from mlxtend.frequent_patterns import apriori

min_support = 0.9
frequent_itemsets = apriori(df, min_support= min_support, use_colnames=True)
while (len((frequent_itemsets)) < 20) & (min_support > 0.04):
	if min_support == 0.1:
		min_support -= 0.01
	else:
		min_support -= 0.1
	frequent_itemsets = apriori(df, min_support= min_support,  use_colnames=True)

from mlxtend.frequent_patterns import association_rules

min_threshold = 0.9
assoc_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_threshold)
while (len((assoc_rules)) < 10) & (min_threshold > 0.01):
	if min_threshold == 0.1:
		min_threshold -= 0.01
	else:
		min_threshold -= 0.1
	assoc_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_threshold)


frequent_itemsets.itemsets = frequent_itemsets.itemsets.apply(list)

fii = list(frequent_itemsets.itemsets)
fis = list(frequent_itemsets.support)
freq_dict = {}

for i in range(0,len(fii)-1):
	freq_dict["{0:.2f}".format(fis[i])] = fii[i]

if (len(frequent_itemsets) < 2):
	print("no frequent_itemsets")
else:
	print(freq_dict)

exit()
#print((dataset.describe()).to_json())