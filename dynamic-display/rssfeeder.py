import sys
import feedparser

# Function to fetch the rss feed and return the parsed RSS
def parseRSS( rss_url ):
    return feedparser.parse( rss_url ) 

# Function grabs the rss feed headlines (titles) and returns them as a list
def getHeadlines( rss_url ):
    headlines = []

    feed = parseRSS( rss_url )
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])
    return headlines


def getRSSnews( allheadlines, news_type ):

    # Method 1 :
    #RSS news from following sources, per blocks
    #newsurls = {
    #    'googlenews':       'https://news.google.com/news/rss/?hl=fr&amp;ned=fr&amp;gl=FR',
    #    'bfmtv':       'https://www.bfmtv.com/rss/planete/',
    #    'equipe' :      'https://www.lequipe.fr/rss/actu_rss.xml',
    #}
 
    ## Iterate over the feed urls
    #for key,url in newsurls.items():
    #    allheadlines.extend( getHeadlines( url ) )


    # OR Method 2
    #Filtered RSS news by categories
    newsurlsEcology = 'https://www.bfmtv.com/rss/planete/'
    newsurlsSport = 'https://www.lequipe.fr/rss/actu_rss.xml'
    newsurlsLocal = 'https://news.google.com/news/rss/?hl=fr&amp;ned=fr&amp;gl=FR' # Would be great if takes directly the city as local
    headlinesEcology = []
    headlinesSport = []
    headlinesLocal = []
    headlinesEmpty = [" "," "]

    ## Iterate over the feed urls
    if "ecologie" in news_type:
        headlinesEcology.extend(getHeadlines(newsurlsEcology))
    if "sport" in news_type:
        headlinesSport.extend(getHeadlines(newsurlsSport))
    if "locale" in news_type:
        headlinesLocal.extend(getHeadlines(newsurlsLocal))

    lenlist = [len(headlinesEcology), len(headlinesSport), len(headlinesLocal)]

    #Iterate over the RSS, several categories at once
    if max(lenlist) > 0:
        for i in range(max(lenlist) - 1):
            if len(headlinesEcology) > 0 and i < len(headlinesEcology):
                allheadlines.append(headlinesEcology[i])
            if len(headlinesSport) > 0 and i < len(headlinesSport):
                allheadlines.append(headlinesSport[i])
            if len(headlinesLocal) > 0 and i < len(headlinesLocal):
                allheadlines.append(headlinesLocal[i])
    else:
        allheadlines.append(headlinesEmpty[0]) # TODO ERROR IndexError when update
        allheadlines.append(headlinesEmpty[1])

    ## Iterate over the allheadlines list and print each headline
    #for nws in allheadlines:
    #    print(nws)

    return allheadlines