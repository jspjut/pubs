#!/usr/bin/python

import yaml
import sys
import string

def test(pub, authors, ptype = ''):
	teststr = ''
	for i, p in pub.items():
		teststr += '%s -> %s'%(i,p)
		# if publication
		if type(p) is dict:
			teststr += '\t%s'%p['title']
			if p['authors'] is not None:
				for a in p['authors']:
					teststr += '\t\t%s'%authors[a]['name']
	return teststr

strdict = {}
def uniquify(str):
	if str not in strdict.keys():
		strdict[str] = 0
		return str
	else:
		for a in string.lowercase:
			if str+a not in strdict.keys():
				strdict[str+a] = 0
				return str+a
		print 'ERROR, could not uniquify'

def uniqueid(pub, authors):
	firstauthor = authornametag(authors[pub['authors'][0]]['name'])
	secondauthor = ''
	if (len(pub['authors'])>1):
		secondauthor = authornametag(authors[pub['authors'][1]]['name'])
	bibid = firstauthor + secondauthor + '%02d'%(pub['year']%100)
	return uniquify(bibid)

# Use lower case last name as the author tag
def authornametag(authorname):
	return authorname.split(' ')[-1].lower()

# Return a formatted bibtex string
def bibtex(pubentry, authors, ptype = 'inproceedings'):
	bibstr = ''
	for pid, pub in pubentry.items():
		if pub['authors'] is None:
			return bibstr
		bibid = uniqueid(pub, authors)

		# start with @inproceedings{id
		bibstr += '@%s{%s'%(ptype,bibid)
		# author list
		if pub['authors'] is not None:
			bibstr += ',\n author = {'
			first = ''
			for a in pub['authors']:
				bibstr += '%s %s '%(first, authors[a]['name'])
				first = 'and'
			bibstr += '}'

		# add the fields that exist
		try: 
			bibstr += ',\n title = {{%s}}'%pub['title']
		except KeyError:
			pass
		try:
			bibstr += ',\n year = {%d}'%pub['year']
		except KeyError:
			pass
		try:
			bibstr += ',\n booktitle = {%s}'%pub['conference']
		except KeyError:
			pass
	bibstr += '\n}\n'
	return bibstr

# Return a formatted markdown string; ptype chooses bolded author
def markdown(pubentry, authors, ptype = 'jspjut'):
	mdstr = ''
	for pid, pub in pubentry.items():
		mdstr += '1. '
		# author list
		if pub['authors'] is not None:
			mdstr += ''
			first = ''
			for a in pub['authors']:
				if a == ptype:
					mdstr += '%s **[%s][%s]**'%(first, authors[a]['name'], a)
				else:
					mdstr += '%s [%s][%s]'%(first, authors[a]['name'], a)
				first = ','
			mdstr += ';\n'
		
		# add the fields that exist
		try: 
			mdstr += '**%s**,\n'%pub['title']
		except KeyError:
			pass
		try:
			mdstr += '*%s*,\n'%pub['conference']
		except KeyError:
			pass
		try:
			mdstr += '%s, '%pub['location']
		except KeyError:
			pass
		try:
			mdstr += '%s, '%pub['month']
		except KeyError:
			pass
		try:
			mdstr += '%d.'%pub['year']
		except KeyError:
			pass
		try:
			mdstr += ' **%s**'%pub['misc']
		except KeyError:
			pass

		# add paper links
		try:
			mdstr += '\n[paper](%s)'%pub['paper']
		except:
			pass
	mdstr += ''
	return mdstr

def authormarkdown(authors):
	mdstr = ''
	for key, val in authors.items():
		mdstr += '   [%s]: %s\n'%(key, val['url'])
	return mdstr

if __name__ == '__main__':
	# get author lookup
	afile = open('authors.yml', 'r')
	authors = yaml.load(afile)['authors']

	# load pub list
	stream = open('pubs.yml', 'r')
	for publist in yaml.load_all(stream):
		print '##', publist['name']
		# loop over list of publications
		for pub in publist['pubs']:
			bib = bibtex(pub, authors)
			other = test(pub, authors)
			md = markdown(pub, authors)
			print md

		print ''
	print authormarkdown(authors)





