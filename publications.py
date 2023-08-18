#!/usr/bin/env python3

# By Josef Spjut, 2014-2022
# This script is intended to be used to read in some yaml files and output
# markdown, bibtex, html or similar file types with paper references.
# It requires PyYaml to function: http://pyyaml.org/wiki/PyYAML

# The input filenames
authorsyaml = 'authors.yml'
pubsyaml = 'pubs.yml'
mediayaml = 'media.yml'

# The output filenames
# basepath = '/Users/Josef/'
basepath = '../'
htmlfilename = basepath + 'jspjut.github.io/content/research/research.html' # use is deprecated on the website
mdfilename = basepath + 'CV/src/publications.md' # used by CV tool
mediafilename = basepath + 'jspjut.github.io/content/media/_index.md' # media page
researchfilename = basepath + 'jspjut.github.io/content/research/_index.md' # research page

htmlheaderstring = '''+++
title = "Research"
date = 2018-09-20
+++

<style>
a.author{
	color: grey;
}
a.primary{
	font-weight: bold;
}
</style>


'''
researchheaderstring = '''+++
title = "Research"
date = "2018-01-01T00:00:00Z"
math = false
highlight = false

# This is the list of publication types to display (in order)
pubtype_list = ["7", "8", "9", "10", "4", "11"]

# Optional featured image (relative to `static/img/` folder).
[header]
image = ""
caption = ""

+++

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
<strong>Design and Implementation of a Memory Testing Apparatus</strong>, 
<em>Clinic Report for Dart Neuroscience</em>, Harvey Mudd College, 116 pages, May 2015.</li>

<li>Olivier Cheng, Stephen Ibanez, Amy Ngai, Joshua Sanz, Avi Thaker,
<strong>Josef Spjut</strong>, Alon Regev;
<strong>Computer Network Testing</strong>,
<em>Clinic Report for Ixia</em>, Harvey Mudd College, 48 pages, May 2015.</li>

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


<h3>Past Research Students</h3>

<p>Eric Storm &#39;15, Ivan Wong &#39;15, 
Skyler Williams &#39;16, Ramy Elminyawi &#39;16, 
 Amy Ngai &#39;16, Richard Piersall &#39;16, Kirklann Lau &#39;16, 
 Andrew Fishberg &#39;16, Da Eun Shim &#39;16,
Fabiha Hannan &#39;16, Paul Jolly &#39;16,
Dong-hyeon Park &#39;14, Sami Mourad &#39;14, Akhil Bagaria &#39;16,
Andrew Carter &#39;13, Paula Ning &#39;13, Max Korbel &#39;13, Katherine Yang &#39;15</p>

'''

# hiding the collaborator list since I automated it
'''
<h3>Current and Recent (within 3 years) Collaborators</h3>

<p>Trey Greer, Turner Whitted, David Luebke,
Timo Aila, Tero Karras, Samuli Laine, 
 Erik Brunvand, Konstantin Shkurko, Daniel Kopta, Al Davis, 
Seth Pugsley,
</p>

<h3>Past Collaborators</h3>

<p>Mike Parker, 
Thiago Ize, Andrew Kensler, 
Rajeev Balasubramonian
David Nellans,
Niladrish Chatterjee, Pete Shirley, Steve Parker,
Solomon Boulos, Spencer Kellis, 
Frank Vahid, David Sheldon, Scott Sirowy, Roman Lysecky</p>
'''

mediaheaderstr = '''+++
title = "Media Coverage"
+++

'''

# Start main script
import yaml
import sys
import string
import datetime

# media library
import media
import pubs2hugo

# function for uniquifying the ids in bibtex. Be sure to only run once per reference...
strdict = {}
def uniquify(str):
	if str not in strdict.keys():
		strdict[str] = 0
		return str
	else:
		for a in string.ascii_lowercase:
			if str+a not in strdict.keys():
				strdict[str+a] = 0
				return str+a
		print( 'ERROR, could not uniquify' )

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
			mdstr += '**%s**, '%pub['title']
		except KeyError:
			pass
		try:
			mdstr += '*%s*, '%pub['conference']
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
			if pub['date'] > datetime.datetime.now().date():
				mdstr += ' (to appear)'
				pass
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
		try:
			mdstr += '\n[webpage](%s)'%pub['webpage']
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
					mdstr += '%s<a href="%s" class="author primary">%s</a>'%(first, authors[a]['url'], authors[a]['name'])
				else:
					mdstr += '%s<a href="%s" class="author">%s</a>'%(first, authors[a]['url'], authors[a]['name'])
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
			if pub['date'] > datetime.datetime.now().date():
				mdstr += ' (to appear)'
				pass
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
			mdstr += '\n<a href="%s">alternate</a>'%pub['alternate']
		except:
			pass
		try:
			mdstr += '\n<a href="%s">alternate 2</a>'%pub['alternate2']
		except:
			pass
		try:
			mdstr += '\n<a href="%s">slides</a>'%pub['slides']
		except:
			pass
		try:
			mdstr += '\n<a href="%s">webpage</a>'%pub['webpage']
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

def getCollaborators(collaborators, pubentry, authors, exclude = 'jspjut'):
	year = 1982
	for pid, pub in pubentry.items():
		if pub['year'] is not None:
			year = pub['year']
		try:
			collaborators[year]
		except KeyError:
			collaborators[year] = set()
		if pub['authors'] is not None:
			for a in pub['authors']:
				if a == exclude:
					continue # skip myself
				collaborators[year].add(authors[a]['name'])
	return collaborators

def collaboratorString(collaborators):
	firstyear = 2006
	# need to update these years every year
	recentyear = 2020
	currentyear = 2024
	recentset = set()
	pastset = set()
	for year in range(firstyear, currentyear):
		try:
			if year < recentyear:
				[pastset.add(c) for c in collaborators[year]]
			else:
				[recentset.add(c) for c in collaborators[year]]
			# htmlstr += '<p>' + ', '.join(collaborators[year]) + '</p>'
		except:
			pass
	htmlstr = ''
	htmlstr += '<h3>Current and Recent Collaborators</h3>\n\n'
	htmlstr += '<p>' + ', '.join(sorted(recentset)) + '</p>\n\n'
	htmlstr += '<h3>Past Collaborators</h3>\n\n'
	htmlstr += '<p>' + ', '.join(sorted(pastset.difference(recentset))) + '</p>\n\n'
	return htmlstr

if __name__ == '__main__':
	mdstr = ''
	htmlstr = htmlheaderstring
	# get author lookup
	afile = open(authorsyaml, 'r')
	authors = yaml.load(afile, Loader=yaml.FullLoader)['authors']

	# collaborators dict
	collaborators = {}

	# load pub list
	stream = open(pubsyaml, 'r')
	# delimited by --- in the yaml
	for publist in yaml.load_all(stream, Loader=yaml.FullLoader): 
		# skip unpublished list
		if publist['urlid'] == 'unpub':
			for pub in publist['pubs']:
				collaborators = getCollaborators(collaborators, pub, authors)
			continue

		# skip patents (for now)
		# if publist['urlid'] == 'pat':
		# 	continue

		mdstr += '## %s\n'%publist['name']
		htmlstr += '<h2>%s</h2>\n<ol>'%publist['name']

		# loop over list of publications
		for pub in publist['pubs']:
			mdstr += markdown(pub, authors)
			htmlstr += htmlformat(pub, authors)
			collaborators = getCollaborators(collaborators, pub, authors)

		mdstr += '\n\n'
		htmlstr += '</ol>\n\n'
	# add links at the end of markdown
	mdstr += authormarkdown(authors)

	# add collaborators to html footer
	htmlfooterstring += collaboratorString(collaborators)

	# add html footer
	htmlstr += htmlfooterstring

	# write out html and markdown results
	print('Writing research (old) file at ' + htmlfilename)
	htmlfile = open(htmlfilename, 'w')
	htmlfile.write( htmlstr )
	htmlfile.close()

	print('Writing CV file at ' + mdfilename)
	mdfile = open(mdfilename, 'w')
	mdfile.write( mdstr )
	mdfile.close()

	# media stuff
	mediamdstr = mediaheaderstr

	mfile = open(mediayaml, 'r')
	for entry in yaml.load_all(mfile, Loader=yaml.FullLoader):
		mediamdstr += '## %s\n'%entry['name']
		mediamdstr += entry['text'] + '\n\n'
		mediamdstr += media.mdformat(entry['media'])

	# medias = yaml.load(mfile, Loader=yaml.FullLoader)['media']
	# mediahtmlstr = media.htmlformat(medias)
	# mediamdstr += media.mdformat(medias)

	print('Writing media file at ' + mediafilename)
	mediafile = open(mediafilename, 'w')
	mediafile.write(mediamdstr)
	mediafile.close()

	researchmdstr = researchheaderstring + htmlfooterstring
	print('Writing research file at ' + researchfilename)
	researchfile = open(researchfilename, 'w')
	researchfile.write(researchmdstr)
	researchfile.close()

	# build hugo files per publication
	pubs2hugo.main()




