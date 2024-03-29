#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#
testingrooms = ['A','B','C']
for room in testingrooms:
    source= '/Users/uv/Documents/GitHub/ps2-UVab/testingroom'+room+'/experiment_data.csv'
    destination= '/Users/uv/Documents/GitHub/ps2-UVab/rawdata/IATdata_Room'+room+'.csv'
    shutil.copy(source,destination)


#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0,5))
for room in testingrooms:
    temp = sp.loadtxt('/Users/uv/Documents/GitHub/ps2-UVab/rawdata/IATdata_Room'+room+'.csv',delimiter=',')
    data = np.vstack([data,temp])
#%%
# calculate overall average accuracy and average median RT
#
acc_avg = np.mean(data[:,3])   # 91.48%
mrt_avg = np.mean(data[:,4])   # 477.3ms

#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#
acc_word_avg = 0.0
mrt_word_avg = 0.0 
acc_face_avg = 0.0
mrt_face_avg = 0.0 

for row in range(len(data)) : 
    if data[row,1] == 1:
        acc_word_avg+= data[row,3]
        mrt_word_avg+= data[row,4]
    elif data[row,1]==2: 
        acc_face_avg+= data[row,3]
        mrt_face_avg+= data[row,4]
    else:
        print('!!!row number '+str(row)+' missing!!!')    #make sure if there are NAs or others they will be flagged! 
acc_word_avg/= sum(data[:,1] == 1)   #divide each sum by the number of rows that satisfy the condition! 
mrt_word_avg/= sum(data[:,1] == 1) 
acc_face_avg/= sum(data[:,1] == 2)
mrt_face_avg/= sum(data[:,1] == 2)

print("words: "+"acc:"+str(acc_word_avg)) #print each conditional mean 
print("words: "+"mrt:"+str(mrt_word_avg))
print("faces: "+"acc:"+str(acc_face_avg))
print("faces: "+"mrt:"+str(mrt_face_avg))

# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms


#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
#
acc_wp = np.mean(data[(data[:,2] == 1), 3])  #94
acc_bp = np.mean(data[(data[:,2] == 2), 3])  # 88.9%
mrt_wp = np.mean(data[(data[:,2] == 1), 4])  # 469.6ms
mrt_bp = np.mean(data[(data[:,2] == 2), 4])  # 485.1ms
print(acc_wp)
print(acc_bp)
print(mrt_wp)
print(mrt_bp)
#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#
mrt_words_wp = np.mean(data[(data[:,1] == 1) & (data[:,2] == 1), 4])
mrt_words_bp = np.mean(data[(data[:,1] == 1) & (data[:,2] == 2), 4])
mrt_faces_wp = np.mean(data[(data[:,1] == 2) & (data[:,2] == 1), 4])
mrt_faces_bp = np.mean(data[(data[:,1] == 2) & (data[:,2] == 2), 4])
print(mrt_words_wp)
print(mrt_words_bp)
print(mrt_faces_wp)
print(mrt_faces_bp)
# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats

mrt_words_wp = data[(data[:,1] == 1) & (data[:,2] == 1), 4]
mrt_words_bp = data[(data[:,1] == 1) & (data[:,2] == 2), 4]
words_ttest = scipy.stats.ttest_rel(mrt_words_wp, mrt_words_bp)
mrt_faces_wp = data[(data[:,1] == 2) & (data[:,2] == 1), 4]
mrt_faces_bp = data[(data[:,1] == 2) & (data[:,2] == 2), 4]
faces_ttest = scipy.stats.ttest_rel(mrt_faces_wp, mrt_faces_bp)

# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))
# sorry I ran out of time, but i have the averages printed already
print('\nWORDS T-TEST: t = {:.2f}, p = {:.3f}'.format(words_t[0], words_t[1]))
print('\nFACES T-TEST: t = {:.2f}, p = {:.3f}'.format(faces_t[0], faces_t[1]))
