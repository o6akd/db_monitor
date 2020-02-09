Recognize: 
	Input: Pandas DataFrame 
	Output: A Jason object with data type corresponding to each column of the input
			- Scales are Useless, Nominal, Binary, Ordinal, Count,Time,Interval. 
				-> Adapted from this resource: https://towardsdatascience.com/7-data-types-a-better-way-to-think-about-data-types-for-machine-learning-939fae99a689
			- Type corresponds to output of tpye(x) function.
			- Topic is hopefully found in meta data. 

		-- Ex: {column_name:{primitive_type: 'int', scale:'ordinal', topic:'health'} }
		This jason object is passed to other modules. It's used as part of determining the strategy. 
		It's part of the global object. 
		-- Ex: {data: {name: "health.csv", 
					   properties: {column_names:['age','gender','column_name'] , 
					   				'age':{primitive_type: 'int', scale:'ordinal', topic:'health'}}
					   strategy:['classification'] }}
					   
	Process: Trained ML model checks predicts the data types.
		-- How does the ML work? --
		We pull data from the Kaggle website and every data instance is labeled with its type and column name and optional topic.
		This data set is used for training the classification model. Needs to be trained only once. 

Decision Tree:
	Is it a missing value? 
	Is it numerical only?
		Is it continious? (23.342, 23.54, 45.232)
			Is it a ratio?
			Else:continious
		Is it discrete?
			Is it binary? (1, 0) #can also correspond to text data such as male female
			Is it a count? (1,4,56,78)
			Is it ordinal? (ranking)
	Is it text only?
		Is it a missing value? ("Null",NaN, [NaN], nan,null etc. )
		Is it nominal? ("female" , "male", "blue", "red", "yellow" ) 
		Is it ordinal? ("happy", "unhappy", "very sad") (can be represented with numbers)
	Is it an interval?
		#has to have a combination of numeric and text data
		# 1-2 , 3-5, 6-10 etc. 

    How to find these?
		- Check for primitive type
		- For numbers check mean, median, mode, variance, value counts 
		- For categorical data: check mode, check unique value counts
	Problems:
		- Overlapping categories:
			- Numeric data might represent categories, it would be impossible to know which one. 
			  Potential solutions: unique count might give insight. Still impossible know nominal or ordinal without a dictionary
			- Zip codes are numerical yet nominal...
			- 45C is a numerical continious temperature 
	
* Preparing the training data
    - Features: 
	    - ascii onehot encoding + (zero for categorical: mean + variance ) + (-1 for continious and counts) unique value count + column name
		 + topic name + primitive type + intended type + (optional) ml_strategy
		- y value (prediction) can be intended type, topic name or ml_strategy
	- Predict:
		- Topic, intended type, strategy or ml_strategy

	- Final Output
		- Given the inferred data types we can show:
			- relationship between variables: hypothesis testing is a method
			- Predictive models as assets, no inference
			- Important features: given a prediction which predictor is the most important one
			- Clustering: show cluster intervals
		- Alternative output 
		    - given data infer the strategy : using web scraping this requires adding additional features to training
			- given the dataset show a website with relevant code. 
			- given the dataset show relevant strategies. 
							