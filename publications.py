#!/usr/bin/python

import yaml
import sys

def test(pub, ptype = ''):
	for i, p in pub.items():
		print '\t', i, '->', p
		# if publication
		if type(p) is dict:
			print '\t', p['title']
			if p['authors'] is not None:
				for a in p['authors']:
					print '\t\t',authors[a]['name']

def bibtex(pub, ptype = 'article'):
	sys.stdout.write('@%s{%s,\n'%(ptype,pub['authors'][0]+pub['date'][:-2]))
	for i, p in pub.items():
		#print '\t', i, '->', p
		if p['authors'] is not None:
			first = ''
			for a in p['authors']:
				sys.stdout.write('%s %s '%(first, authors[a]['name']))
				first = 'and'
		print ',\n', p['title']

if __name__ == '__main__':
	print 'run!'

	# get author lookup
	afile = open('authors.yml', 'r')
	authors = yaml.load(afile)['authors']

	# load pub list
	stream = open('pubs.yml', 'r')
	for publist in yaml.load_all(stream):
		print publist['name']

		for pub in publist['pubs']:
			bibtex(pub)

		print '\n'
		exit(0)





