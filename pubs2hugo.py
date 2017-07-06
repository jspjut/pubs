#!/usr/bin/python
'''Script to generate publications files for a hugo academic site.'''
# Josef Spjut 2017

import yaml

import publications

if __name__ == '__main__':
	# get author lookup
    afile = open(publications.authorsyaml, 'r')
    authors = yaml.load(afile)['authors']

    # load pub list
    stream = open(publications.pubsyaml, 'r')
    # delimited by --- in the yaml
    for publist in yaml.load_all(stream): 
        pubtype = publist['name']
        puburltext = publist['urlid']
        pubhugoid = publist['hugoid']

        print pubtype

		# loop over list of publications
        for pubentry in publist['pubs']:
            # loop over content
            for pid, pub in pubentry.items():
                outstr = '+++\n\n'
                # author list
                if pub['authors'] is not None:
                    # outstr += '# Authors. Comma separated list, `["Bob Smith", "David Jones"]`\n'
                    outstr += 'authors = ['
                    first = ''
                    for a in pub['authors']:
                        if a == 'jspjut': # special case for important author
                            outstr += '%s"**[%s](%s)**"'%(first, authors[a]['name'], authors[a]['url'])
                        else:
                            outstr += '%s"[%s](%s)"'%(first, authors[a]['name'], authors[a]['url'])
                        first = ', '
                    outstr += ']\n\n'
                    outstr += 'authors_flat = ['
                    first = ''
                    for a in pub['authors']:
                        outstr += '%s"%s"'%(first, authors[a]['name'])
                        first = ', '
                    outstr += ']\n\n'
                
                # title
                outstr += 'title = "%s"\n'%pub['title']
                
                # add publication category
                outstr += '\n# Publication type.\n'
                outstr += 'publication_types = ["%s"]\n\n'%(pubhugoid)

                # date
                try:
                    outstr += 'date = "%s"\n'%pub['date']
                except KeyError:
                    pass

                # journal/conference name
                try:
                    outstr += '\n# Publication name and optional abbreviated version.\n'
                    outstr += 'publication = "%s"\n'%pub['conference']
                    outstr += 'publication_short = "%s"\n'%pub['conf-short']
                except KeyError:
                    pass

                outstr += '# Abstract and optional shortened version.\n'
                try:
                    outstr += 'abstract = "%s"\n'%pub['abstract']
                    outstr += 'abstract_short = ""\n'
                except KeyError:
                    pass

                # # Featured image thumbnail (optional)\n'
                try:
                    outstr += 'image_preview = "thumbnail/%s"\n'%(pub['thumbnail'])
                except KeyError:
                    outstr += 'image_preview = "placeholder.png"\n'

                #constants...
                outstr += '\n# Is this a selected publication? (true/false)\n'
                outstr += 'selected = false\n'
                outstr += '\n# Does this page contain LaTeX math? (true/false)\n'
                outstr += 'math = false\n'
                outstr += '\n# Does this page require source code highlighting? (true/false)\n'
                outstr += 'highlight = true\n'

                outstr += '\n# Links (optional)\n'
                try:
                    outstr += 'url_pdf = "%s"\n'%pub['paper']
                except KeyError:
                    outstr += 'url_pdf = ""\n'
                outstr += 'url_code = ""\n'
                outstr += 'url_dataset = ""\n'
                try:
                    outstr += 'url_project = "%s"\n'%pub['webpage']
                except:
                    outstr += 'url_project = ""\n'
                try:
                    outstr += 'url_slides = "%s"\n'%pub['slides']
                except:
                    outstr += 'url_slides = ""\n'
                outstr += 'url_video = ""\n'

                # used for making the publication unique on pages
                outstr += 'unique_id = "%s"\n'%publications.uniqueid(pub, authors)

                outstr += '\n# Optional custom urls.\n'
                try:
                    outstr += '[[url_custom]]\n\tname="alternate"\n\turl = "%s"\n'%pub['alternate']
                except KeyError:
                    pass
                try:
                    outstr += '[[url_custom]]\n\tname="alternate2"\n\turl = "%s"\n'%pub['alternate2']
                except KeyError:
                    pass
                
                outstr += '\n# Optional featured image (relative to `static/img/` folder).\n'
                outstr += '[header]\n'
                try:
                    outstr += 'image = "headers/%s"\n'%(pub['banner'])
                except KeyError:
                    # outstr += 'image = "placeholder-banner.jpeg"\n'
                    outstr += 'image = ""\n'
                outstr += 'caption = ""\n'

                outstr += '\n+++\n'
                #save the file
                # generate filename  ~/github/jspjut-projects/jubilant-meme/content/publication/
                output_filename = '%scontent/publication/%s/%s.md'%('/Users/Josef/github/jspjut-projects/jubilant-meme/', puburltext, pid)
                # print output_filename, outstr
                # exit(0)
                outfile = open(output_filename, 'w')
                outfile.write(outstr)
                outfile.close()

