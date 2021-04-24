#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 20:08:05 2020

@author: chasebrown
"""

import pandas as pd
from tika import parser
import os


def parsePDFOutput(rawList, filename):
    brokenFiles = ''
    data = {'Section': [],
            'A': [],
            'B': [],
            'C': [],
            'D': [],
            'F': [],
            'TotalAF': [],
            'GPA': [],
            'I': [],
            'S': [],
            'U': [],
            'Q': [],
            'X': [],
            'Total': [],
            'Instructor': []
            }
    
    counter = 15
    row = []
    for i in rawList:
        if not '-----' in i:
            if len(i)>4:
                if (i[4]=='-'):
                    try:
                        data['Section'].append(row[0])
                        data['A'].append(str(row[1]) + " | " + str(row[2]))
                        data['B'].append(str(row[3]) + " | " + str(row[4]))
                        data['C'].append(str(row[5]) + " | " + str(row[6]))
                        data['D'].append(str(row[7]) + " | " + str(row[8]))
                        data['F'].append(str(row[9]) + " | " + str(row[10]))
                        data['TotalAF'].append(row[11])
                        data['GPA'].append(row[12])
                        data['I'].append(row[13])
                        data['S'].append(row[14])
                        data['U'].append(row[15])
                        data['Q'].append(row[16])
                        data['X'].append(row[17])
                        data['Total'].append(row[18])
                        data['Instructor'].append(' '.join(row[19:]))
                    except Exception as e:
                        brokenFiles = (str(filename))
                    row = []
                    counter=0
            if counter<15:
                for s in i.split():
                    row.append(s)
                    counter+=1
    return [pd.DataFrame(data, columns = ['Section', 'A', 'B', 'C', 'D', 'F', 'TotalAF', 'GPA', 'I', 'S', 'U', 'Q', 'X', 'Total', 'Instructor']), str(brokenFiles)]
            
allTests = []
directory = os.fsencode("./PDFs/")
listOfPDFs = os.listdir(directory)

content = []
brokenFiles2 = []
counter = 0
for i in listOfPDFs:
    print(str(counter) + " Of " + str(len(listOfPDFs)))
    counter+=1
    rawText = parser.from_file('./PDFs/' + str(i).split("'")[1])
    try:
        df = parsePDFOutput(rawText['content'].splitlines(), str(i).split("'")[1])
    except:
        brokenFiles2.append(str(i).split("'")[1])
    content.append(df[0])
    brokenFiles2.append(str(df[1]))

dataframe = content[0]
first = True
for i in content:
    if not first:
        dataframe = dataframe.append(i, ignore_index=True, sort=False)
    else:
        first = False

dataframe.to_csv(r'PDFData.csv', index=None, sep=',', mode='a')

