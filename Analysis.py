import numpy as np 
import pandas as pd 
import matplotlib as plt   
import tensorflow as tf  
from tensorflow import keras
from keras.layers import TextVectorization  
from keras.layers import Hashing

hyp_data = pd.read_pickle('hyp_data.pkl') 
#drop all the columns in combined since theyre useless now 
hyp_data = hyp_data.drop(["Original Raw"], axis = 1) 

#split to train test and val dataframes
train, val, test = np.split(hyp_data.sample(frac=1), [int(0.8*len(hyp_data)), int(0.9*len(hyp_data))]) 

#for refrence, used columns are now: Regular Word (str), Word Length (int), 
# Total Number of Vowels(int), Vowel Constant Pattern (str) 
# with a target of Syllables (int)

#preprocessing step where i convert all the data in this dataset into smthing usable  

#gotta preprocess the regualr words
text_vectorization = TextVectorization(
    output_mode='int',
    split='character'  # Split by character
) 
text_vectorization.adapt(train['Regular Word'])   

#now preprocess for all 
train['Regular Word'] = text_vectorization(train['Regular Word'])
test['Regular Word'] = text_vectorization(test['Regular Word'])
val['Regular Word'] = text_vectorization(val['Regular Word'])

#now we have to preprocess the vc pattern 
#use a hashing function to do this 
#unique_patterns = hyp_data['Vowel Constonant Pattern'].unique()
#num_bins = len(unique_patterns)
#27,114 unique entries, lets set the number of bins to 30,000 just in case  
hashing_layer = Hashing(num_bins=30000) 
train['Vowel Constonant Pattern'] = hashing_layer(train['Vowel Constonant Pattern'])
test['Vowel Constonant Pattern'] = hashing_layer(test['Vowel Constonant Pattern'])
val['Vowel Constonant Pattern'] = hashing_layer(val['Vowel Constonant Pattern'])  

#converts df to dataset
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
  df = dataframe.copy()
  labels = df.pop('Syllables') 
  #turn columns into numpy arry 
  df = {key: value.values.reshape(-1, 1) for key, value in df.items()}
  ds = tf.data.Dataset.from_tensor_slices((df, labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  ds = ds.prefetch(batch_size)
  return ds 

#turn them into datasets
train_data = df_to_dataset(train)
valid_data = df_to_dataset(val)
test_data = df_to_dataset(test)




