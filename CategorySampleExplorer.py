#!/usr/bin/env python3

# Program explores the category tagged wav files.
# Segregates correct and error files and gives summary of correct samples

from os import walk
import csv
import pandas as pd

mydir = "/net/projects/scratch/winter/valid_until_31_July_2021/0-animal-communication/data_grid/Chimp_IvoryCoast/manually_verified_2s/chimp_only_23112020"


_, _, fileNames = next(walk(mydir)) # get the files in the directory

errors = []
row_list = []

for fname in fileNames:
    df = fname.replace("_","-")
    try:
        dict1 = {}
        dict1['filename'] = fname
        dict1['name'] = df.split('-')[2]
        calltyp = df.split('-')[3]
        int(calltyp) # this raising exception means calltype string is found at the expected location
        errors.append([fname])
    except ValueError:
        dict1['calltyp'] = calltyp
        row_list.append(dict1)  # build the list of dict to make the pandas dataframe for easy analysis
    except:
        errors.append([fname]) # files with non standard tags, flag as errors

data_f = pd.DataFrame(row_list, columns=['name','calltyp','filename']) # convert list of dict to pandas dataframe
data_f.to_csv('ChimpcallList.csv', index=False, header=True) # write the list of correctly classified samples

summary = data_f.groupby(['name','calltyp'])['filename'].count()
summary.unstack().to_csv('Summary.csv',index=True, header=True)

with open('Errorlist.csv','w',newline='') as errfile: # wite the list of wrongly tagged samples
    errwriter = csv.writer(errfile)
    errwriter.writerows(errors)



