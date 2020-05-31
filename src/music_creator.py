import os
import sys
import numpy
import math
import pandas as pd
import wave
import sys
import datetime

path_intru='../data/reference/'
path_data_in='../data/input/'
path_data_out='../data/output/Music/'

class MusicCreator():
	def __init__(self,state='France',measure='Ozone',start_date='2020-01-01',end_date='2020-05-01',nb_agg=7,**kwargs):
		#Create data list
		df=pd.read_csv(path_data_in+measure+'/'+state+'_'+measure+'.csv')
		df=df[df[df.columns[1]]>0]
		list_df=df[(df.time>=start_date)&(df.time<=end_date)]
		list_min_max=df[(df.time>=str(int(end_date[:4])-1)+start_date[4:])&(df.time<=end_date)][df.columns[1]]
		list_agg=[]
		for i in range(int(list_df.shape[0]/nb_agg)):
			list_agg.append([sum(list_df[i*nb_agg:(i+1)*nb_agg][df.columns[1]])/nb_agg,max(list_df[i*nb_agg:(i+1)*nb_agg][df.columns[0]])])
		
		list_min_max_agg=[]
		for i in range(int(len(list_min_max)/nb_agg)):
			list_min_max_agg.append(sum(list_min_max[i*nb_agg:(i+1)*nb_agg])/nb_agg)
		min_val=min(list_min_max_agg)
		max_val=max(list_min_max_agg)
		#Choose type of music
		instru='piano'
		notes=[]
		for i in os.listdir(path_intru+instru+'/'):
			notes.append(path_intru+instru+'/'+i)
		#Calculate notes
		infiles=[]
		for i in range(len(list_agg)):
			pitch = ((list_agg[i][0]-min_val)/(max_val-min_val))*len(notes)
			if int(pitch)==len(notes):
				infiles.append([notes[len(notes)-1],pitch,list_agg[i][0]])
			else:
				infiles.append([notes[int(pitch)],pitch,list_agg[i][0]])
		#Assemblate notes
		data= []
		self.list_chunk=[]
		for infile in infiles:
			w = wave.open(infile[0], 'rb')
			data.append([w.getparams(), w.readframes(w.getnframes()-40000-int(infile[1])*2000)])
			self.list_chunk.append([infile[1]/12,w.getnframes()-40000-int(infile[1])*2000,infile[2]])
			w.close()
		#Write Music
		outfile = path_data_out+"out.wav"
		output = wave.open(outfile, 'wb')
		output.setparams(data[0][0])
		for i in range(len(data)):
			output.writeframes(data[i][1])
		output.close()


if __name__ == '__main__':
	MusicCreator()
