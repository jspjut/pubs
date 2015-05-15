#!/usr/bin/python

# By Josef Spjut, 2014
# This script is intended to be used to read in some yaml files and output
# markdown, bibtex, html or similar file types with paper references.
# It requires PyYaml to function: http://pyyaml.org/wiki/PyYAML

# The input filenames
authorsyaml = 'authors.yml'
pubsyaml = 'pubs.yml'

# The output filenames
htmlfilename = '/Users/Josef/jspjut.github.io/testing.html'
mdfilename = '/Users/Josef/CV/src/publications.md'

# This header will probably still need to exist, but maybe I can put the 
# interests paragraph in a yaml file somewhere
htmlheaderstring = '''---
layout: page
title: Research
tagline: Publications and Interests
group: navigation
---
{% include JB/setup %}

<p>
My Research interests include Ray Tracing, Computer Graphics, Computer
Architecture, Parallel Computing, Real Time Systems, Application
Specific Processing, and Human Computer Interaction.
</p>

'''

# This is a temporary placeholder until I figure out how to autogenerate it
htmlfooterstring = '''<h2>HMC Clinic Projects</h2>

<p>At Harvey Mudd College I advised a few <a href="https://www.hmc.edu/clinic/">clinic
projects</a> with junior and
senior level students paid for by companies. 
The following is a list of those projects and the people involved. 
Those before my name are students, after are liaisons from the
company.</p>

<ul>
<li>Fabiha Hannan, Cyrus Huang, Sebastian Krupa, Guillaume Legrain, 
Minh Triet Nguyen, Maggie Rabasca, Zachary Vickland, Tiancheng Yang, 
<strong>Josef Spjut</strong>, Philip Cheung, John McNeil, Jef Vivian.
<em>Clinic for Dart Neuroscience</em>, 2014-2015.</li>

<li>Olivier Cheng, Stephen Ibanez, Amy Ngai, Joshua Sanz, Avi Thaker,
<strong>Josef Spjut</strong>, Alon Regev;
<em>Clinic for Ixia</em>, 2014-2015.</li>

<li>Antoine Billig, Chanel Chang, Austin Chen, Obosa Obazuaye, Jeffrey
Steele, Sean Velazquez, <strong>Josef Spjut</strong>, Pradeep Batra, Adrian
Torres, Julia Cline;
<strong>USB 3.0 to Multi-Protocol Interface Adapter</strong>,
<em>Clinic Report for Rambus Incorporate</em>, Harvey Mudd College, 183
pages, May 2014.</li>

<li>Dylan Stow, Carl Pearson, Jeffrey Steele,
Shreyasha Paudel, Adam Parower, Gurchetan Singh, Dong-hyeon Park,
<strong>Josef Spjut</strong>, Warren Furguson;
<strong>Multiplicative Based Division</strong>,
<em>Clinic Report for Intel Corp</em>, Harvey Mudd College, 117 pages, May
2013.</li>

<li>Allison Card, Kacyn Fujii, Hannah
Kastein, Paula Ning, Matthew Tambara, Stephanie Fawaz, <strong>Josef Spjut</strong>,
Sourabh Ravindran, Nitish Murthy,
<strong>Immersive Audio Game Development Kit</strong>
<em>Clinic Report for Texas Instruments</em>, Harvey Mudd College, 110 pages,
May 2013.</li>
</ul>

<h2>People</h2>

<p>I&#39;ve been fortunate to work with a large number of talented
people. The ones I&#39;ve worked with on research are listed below. Email
me if you think you should be on this list and you aren&#39;t.</p>

<h3>Current Research Students</h3>

<p>Eric Storm &#39;15, Ivan Wong &#39;15, 
Skyler Williams &#39;16, Ramy Elminyawi &#39;16, 
 Amy Ngai &#39;16, Richard Piersall &#39;16, Kirklann Lau &#39;16, 
 Andrew Fishberg &#39;16, Da Eun Shim &#39;16</p>

<h3>Past Research Students</h3>

<p>Fabiha Hannan &#39;16, Paul Jolly &#39;16,
Dong-hyeon Park &#39;14, Sami Mourad &#39;14, Akhil Bagaria &#39;16,
Andrew Carter &#39;13, Paula Ning &#39;13, Max Korbel &#39;13, Katherine Yang &#39;15</p>

<h3>Current and Recent (within 3 years) Collaborators</h3>

<p>Timo Aila, Tero Karras, Samuli Laine, David Luebke,
 Erik Brunvand, Konstantin Shkurko, Danny Kopta, Al Davis, 
Mike Parker, Seth Pugsley,
Thiago Ize, Andrew Kensler, </p>

<h3>Past Collaborators</h3>

<p>Rajeev Balasubramonian
David Nellans,
Niladrish Chatterjee, Pete Shirley, Steve Parker,
Solomon Boulos, Spencer Kellis, 
Frank Vahid, David Sheldon, Scott Sirowy, Roman Lysecky</p>
'''
# I should really find a way to annotate years on the above collaborations...

# Start main script
import yaml
import sys
import string

# function for uniquifying the ids in bibtex. Be sure to only run once per reference...
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
			bibstr += ',\n title = { {%s} }'%pub['title']
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
		try:
			mdstr += '\n[slides](%s)'%pub['slides']
		except:
			pass
	mdstr += '\n'
	return mdstr

# Return a formatted html string; ptype chooses bolded author
def htmlformat(pubentry, authors, ptype = 'jspjut'):
	mdstr = ''
	for pid, pub in pubentry.items():
		mdstr += '<li>'
		# author list
		if pub['authors'] is not None:
			mdstr += ''
			first = ''
			for a in pub['authors']:
				if a == ptype:
					mdstr += '%s<strong><a href="%s">%s</a></strong>'%(first, authors[a]['url'], authors[a]['name'])
				else:
					mdstr += '%s<a href="%s">%s</a>'%(first, authors[a]['url'], authors[a]['name'])
				first = ', '
			mdstr += ';\n'
		
		# add the fields that exist
		try: 
			mdstr += '<strong>%s</strong>,\n'%pub['title']
		except KeyError:
			pass
		try:
			mdstr += '<em>%s</em>,\n'%pub['conference']
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
			mdstr += '<strong>%s</strong>'%pub['misc']
		except KeyError:
			pass

		# add paper links
		try:
			mdstr += '\n<a href="%s">paper</a>'%pub['paper']
		except:
			pass
		try:
			mdstr += '\n<a href="%s">slides</a>'%pub['slides']
		except:
			pass

		# add bib drop-down
		try:
			bib = bibtex(pubentry, authors)
			mdstr += ''' <a class="ec" href="javascript:" onclick="e=document.getElementById('bib%s').style;e.display=(e.display=='block'?'none':'block')">Bibtex</a>'''%pid 
			mdstr += '''<span id="bib%s" class="b" style="display: none;"><pre>%s</pre></span>'''%(pid, bib)
		except:
			pass
	mdstr += '</li>\n'
	return mdstr

def authormarkdown(authors):
	mdstr = ''
	for key, val in authors.items():
		mdstr += '   [%s]: %s\n'%(key, val['url'])
	return mdstr

if __name__ == '__main__':
	mdstr = ''
	htmlstr = htmlheaderstring
	# get author lookup
	afile = open(authorsyaml, 'r')
	authors = yaml.load(afile)['authors']

	# load pub list
	stream = open(pubsyaml, 'r')
	# delimited by --- in the yaml
	for publist in yaml.load_all(stream): 
		mdstr += '## %s\n'%publist['name']
		htmlstr += '<h2>%s</h2>\n<ol>'%publist['name']

		# loop over list of publications
		for pub in publist['pubs']:
			mdstr += markdown(pub, authors)
			htmlstr += htmlformat(pub, authors)

		mdstr += '\n\n'
		htmlstr += '</ol>\n\n'
	# add links at the end of markdown
	mdstr += authormarkdown(authors)

	# add html footer
	htmlstr += htmlfooterstring

	# write out html and markdown results
	htmlfile = open(htmlfilename, 'w')
	htmlfile.write( htmlstr )
	htmlfile.close()

	mdfile = open(mdfilename, 'w')
	mdfile.write( mdstr )
	mdfile.close()





