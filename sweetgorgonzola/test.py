#!/usr/bin/python
# -*- coding: latin-1 -*-

import pandas as pd
import numpy as np
import sklearn

import matplotlib.pyplot as plt
plt.style.use = 'default'


from os import environ
from os.path import join

from sklearn.ensemble import RandomForestRegressor

import math

'''
EMPLACEMENTS REPOS
'''
# get standard project locations or customize them here
#CODE_FOLDER = environ['CODE_FOLDER']
CODE_FOLDER = ''
#DATA_FOLDER = environ['DATA_FOLDER']
DATA_FOLDER = '../Documents/perso/kaggle/challenge_28_data'
#DOCUMENTS_FOLDER = environ['DOCUMENTS_FOLDER']
#source_data_folder = join(DATA_FOLDER, 'input_data')
source_data_folder = DATA_FOLDER
output_data_folder = join(DATA_FOLDER, 'output_data')
processed_data_folder = join(DATA_FOLDER, 'processed_data')
gis_data_folder = join(DATA_FOLDER, 'GIS')

dtype = {'Finess':'str',
	 'Raison sociale' : 'str',
	 'Provenance des patients (d\xc3\xa9partement)': 'str',
	 'Domaines d activit\xc3\xa9s':'str',
	 '\xc3\xa2ge (deux classes >75 ans, <= 75 ans)':'str',
	 'Nombre de s\xc3\xa9jours/s\xc3\xa9ances MCO des patients en ALD':'int',
	 'Nombre total de s\xc3\xa9jours/s\xc3\xa9ances':'int',
	 'annee':'int',
	 'cible1':'float'}






'''
LOAD DATASET
'''

def load():
	df = pd.read_csv(join(source_data_folder, 'data2.csv'), sep=';', dtype=dtype)
	df.columns = ['finess', 'raison_sociale', 'departement', 'domaine_activite', 'age', 'jours_mco', 'jours_total', 'annee', 'cible1']
	('Data imported. Shape: %s') %str(df.shape)
	return df



'''
PREPROCESSING
'''

def preprocess(df):
	#Function to create the dictionaries modalities-labels
	def dic_strings_to_labels(df, col) :
	    S = set(df[col]) # collect unique label names
	    D = dict( zip(S, range(len(S))) ) # assign each string an integer, and put it in a dict
	    return D

	def strings_to_labels(df, col, D) :
	    Y = [D[y2_] for y2_ in df[col]]
	    return Y

	def new_variables(df):
		#New variables: be sure to comment lines you do not want to use
		print('Creating new variables...')
		df['raison_sociale_type'] = map(lambda x: x.split(' ')[0], df['raison_sociale'])
		#df_domaine_act = pd.get_dummies(df['domaine_activite'], prefix='domaine_activite', prefix_sep='_')
		#df_departements = pd.get_dummies(df['departement'], prefix='departement', prefix_sep='_')
		#df = pd.concat([df, df_domaine_act, df_departements], axis=1)
		return df

	def numeric_trash(df):
		#variables dont on ne saurait pas quoi faire : numeric
		global dic_labels
		dic_labels = {}
		for col in df.columns:
			try:
				(df[col]).astype(float)
			except ValueError:
			    dic_labels[col] = dic_strings_to_labels(df, col)
			    df[col] = strings_to_labels(df, col, dic_labels[col])
		print('Preprocessing done')
		return df

	df = new_variables(df)
	df = numeric_trash(df)
	global cols
	cols = df.columns
	return df



'''
TRAIN TEST SPLIT
'''

def full_train(df):
	print('Splitting train...')
	X_train = np.array(df[list(set(df.columns) - set(['cible1']))])
	y_train = np.array(df['cible1'])
	return X_train, y_train
	print('Train split done')

def train_test(df): #TODO
	print('Splitting train...')
	X_train = np.array(df[list(set(df.columns) - set(['cible1']))])
	y_train = np.array(df['cible1'])
	print('Train split done')



'''
MODEL
'''

def train(X, y):
	global model
	model = RandomForestRegressor
	print('Training %s...') %str(model)
	model = model(n_estimators = 10, n_jobs=-1).fit(X,y)
	print('Training done')

	global rmse
	global imp
	rmse = math.sqrt(sklearn.metrics.mean_squared_error(model.predict(X),y))
	imp = sorted(zip(model.feature_importances_, list(set(cols) - set(['cible1']))), key=lambda x: x[0], reverse=True)
	print('RMSE and feature importances computed: call them using print(rmse) or print(imp)')

def main_train():
	df = load()
	df = preprocess(df)
	X_train, y_train = full_train(df)

	del df #clear memory
	train(X_train, y_train)
	del X_train, y_train
	import pdb;pdb.set_trace()






'''
TEST
'''
def load_test():
	df_test = pd.read_csv(join(source_data_folder, 'test2.csv'), sep=';', dtype=dtype)
	df_test.columns = ['id', 'finess', 'raison_sociale', 'departement', 'domaine_activite', 'age', 'jours_mco', 'jours_total', 'annee']
	('Data imported. Shape: %s') %str(df_test.shape)
	return df_test


'''
PREPROCESSING TEST
'''

def preprocessing_test(df_test):
	#Function to create a new label for modalities not met in the train set
	def strings_to_labels_test (df, col, D) :
	    Y = df[col]
	    Y.loc[~Y.isin(D.keys())] = max(D.values()) + 1
	    D[max(D.values()) + 1] = max(D.values()) + 1
	    Y = [D[y] for y in Y]
	    return Y

	def new_variables_test(df_test):
		df_test['raison_sociale_type'] = map(lambda x: x.split(' ')[0], df_test.ix[:,2]) #attention l'id change là
		#df_domaine_act_test = pd.get_dummies(df_test['domaine_activite'], prefix='domaine_activite', prefix_sep='_')
		#df_departement_test = pd.get_dummies(df_test['departement'], prefix='departement', prefix_sep='_')
		#df_test = pd.concat([df_test, df_domaine_act_test, df_departement_test], axis=1)
		return df_test

	df_test = new_variables_test(df_test)
	for col in df_test.columns:#list(df.columns[:5]) + ['Raison sociale type'] :
		try:
			df_test[col].astype(float)
		except ValueError:
			df_test[col] = strings_to_labels_test(df_test, col, dic_labels[col])
	return df_test

def main_test():
	df_test = load_test()
	df_test = preprocessing_test(df_test)
	X_test = df_test[df_test.columns[1:]]

	#PREDICT AND OUTPUT
	y_test = model.predict(X_test)
	sub = pd.DataFrame(columns=['id', 'cible'])
	sub['id'] = df_test['id']
	sub['cible'] = y_test

	sub.to_csv(join(output_data_folder, 'submission.csv'), index=False, sep=';')


main_train()
main_test()
