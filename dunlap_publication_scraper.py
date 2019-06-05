#!/usr/bin/env python

# Code to automatically scrape Dunlap Directory and ADS, and identify recent Dunlap publications and highlight authors.
# Written by Bryan Gaensler for Dunlap Hack Day, 4 June 2019

# Get 5 most recent Dunlap papers from ADS

import ads
import datetime
import unidecode
from lxml import html
import requests
from itertools import groupby

# Number of papers to return
num = 5

# Max number of authors to list explicitly
maxauth = 5

# Gaensler ADS token
ads.config.token = ''

# Query ADS
# Uses https://ads.readthedocs.io/en/latest/
papers = list(ads.SearchQuery(q="aff:Dunlap Institute", sort="pubdate", rows=num))


authstr = ['' for x in range(num)]
pdate = ['' for x in range(num)]
title = ['' for x in range(num)]
bib = ['' for x in range(num)]
finalstr = ['' for x in range(num)]

for n,paper in enumerate(papers):
    for i in range(len(paper.author)):
        # Make Dunlap authors in bold
        if 'Dunlap Institute' in paper.aff[i]:
            paper.author[i] = "<strong>"+paper.author[i]+"</strong>"
        # Remove long author lists
        elif (i > maxauth):
            paper.author[i] = "..."
#   Eliminate multiple ellipses
    authstr[n] = ", ".join([x[0] for x in groupby(paper.author)])
    
    pdate[n] = datetime.datetime.strptime(paper.pubdate[0:7], "%Y-%m").strftime('%b %Y')
    title[n] = unidecode.unidecode(paper.title[0])
    bib[n] = paper.bibcode
    finalstr[n] = '<a href="https://ui.adsabs.harvard.edu/abs/'+bib[n]+'" target="_blank">'+authstr[n]+', '+title[n]+', '+pdate[n]+'</a> <p>'


# Now write output to WWW

f = open("/Users/bmg/Dropbox/dunlap_publications.html","w")

f.write('<h3>Recent Dunlap Publications</h3>'+'\n')
for n in range(num):
     f.write(str(n+1)+'. '+finalstr[n]+'\n')

f.write('<p><a href="https://ui.adsabs.harvard.edu/#search/q=aff%3A%22Dunlap%20Institute%22&sort=date%20desc" target="_blank">Complete list >></a></p>')
f.close()


