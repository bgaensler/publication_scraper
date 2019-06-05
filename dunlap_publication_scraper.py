# Code to automatically scrape Dunlap Directory and ADS, and identify recent Dunlap publications and highlight authors.
# Written by Bryan Gaensler for Dunlap Hack Day, 4 June 2019

# Get 5 most recent Dunlap papers from ADS
# Uses https://ads.readthedocs.io/en/latest/

import ads
import datetime
import unidecode
from lxml import html
import requests

# Number of papers to return
num = 5
adsname = range(num)
adsname2 = range(num)
bib = range(num)
title = range(num)
pdate = range(num)
authstr = range(num)
finalstr = range(num)

# Gaensler ADS token
ads.config.token = ''
papers = ads.SearchQuery(q="aff:Dunlap Institute", sort="date", rows=num)
for i,paper in enumerate(papers):
    # Now shorten each author to ADS format
    adsname[i] = range(len(paper.author))
    adsname2[i] = range(len(paper.author))
    bib[i] = paper.bibcode.encode('ascii')
    title[i] = unidecode.unidecode(paper.title[0])
    pdate[i] = datetime.datetime.strptime(paper.pubdate[0:7], "%Y-%m").strftime('%b %Y')
    for n in range(len(paper.author)):
        # Where is comma?
        m = paper.author[n].find(',')
        adsname[i][n] = unidecode.unidecode(paper.author[n][0:m+3]+'.')    
        adsname2[i][n] = adsname[i][n]

# Now scrape Dunlap personnel page for list of possible authors
# http://www.dunlap.utoronto.ca/people/directory/

directory = "http://www.dunlap.utoronto.ca/people/directory/"

page = requests.get(directory)
tree = html.fromstring(page.content)
name1 = tree.xpath('//span[@class="given-name"]/text()')
name2 = tree.xpath('//span[@class="family-name"]/text()')

# Now form author strings formatted for ads
dunlapname = ["" for x in range(len(name1))]
for n in range(0,len(name1)):
    dunlapname[n] = unidecode.unidecode(name2[n])+', '+unidecode.unidecode(name1[n][0])+'.'


# Now find the Dunlap authors in each ADS paper and make them bold

for n in range(num):
    for name in dunlapname:
        if (name in adsname[n]):
            i = adsname[n].index(name)
            adsname2[n][i] = "<strong>"+name+"</strong>"


# Now write output to WWW

f = open("/Users/bmg/Dropbox/dunlap_publications.html","w")

f.write('<h3>Recent Dunlap Publications</h3>'+'\n')
for n in range(num):
    authstr[n] = adsname2[n][0]
    for m in range(1,len(adsname2[n])):
        authstr[n] = authstr[n]+'; '+adsname2[n][m]
        finalstr[n] = '<a href="https://ui.adsabs.harvard.edu/abs/'+bib[n]+'" target="_blank">'+authstr[n]+', '+title[n]+', '+pdate[n]+'</a> <p>'
#    finalstr[n] = authstr[n]+', '+pdate[n]
    f.write(str(n+1)+'. '+finalstr[n]+'\n')

f.write('<p><a href="https://ui.adsabs.harvard.edu/#search/q=aff%3A%22Dunlap%20Institute%22&sort=date%20desc" target="_blank">Complete list >></a></p>')
f.close()

