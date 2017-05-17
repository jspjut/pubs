"""Script for handling media yaml formatting"""

def htmlformat(medialist):
    '''returns a string of formatted html for a list of media entried'''
    htmlstr = '<ul>\n'
    for article in medialist:
        htmlstr += '\t<li>\n'
        try:
            htmlstr += '<em>%s</em> - \n'%article['journal']
        except KeyError:
            pass
        try:
            htmlstr += '%s,\n'%article['date']
        except KeyError:
            pass
        try:
            htmlstr += '<a href="%s"><strong>%s</strong></a>\n'%(article['url'], article['title'])
        except KeyError:
            pass
        htmlstr += '\t</li>\n'
    htmlstr += '</ul>\n\n'
    return htmlstr

def mdformat(medialist):
    '''returns a string of formatted html for a list of media entried'''
    mdstr = ''
    for article in medialist:
        mdstr += '* '
        try:
            mdstr += '%s - '%article['journal']
        except KeyError:
            pass
        try:
            mdstr += '%s,\n'%article['date'].strftime("%B %d %Y")
        except KeyError:
            pass
        try:
            mdstr += '[%s](%s)'%(article['title'], article['url'])
        except KeyError:
            pass
        mdstr += '\n'
    mdstr += '\n'
    return mdstr
