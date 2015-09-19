import re, os, sys
import urllib
import urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
from bs4 import BeautifulSoup
from addon.common.addon import Addon
import time
import base64, json
import pyaes


addon_id = 'plugin.video.ditto-rain'
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)
debug = Addon.getSetting('debug')

language = (Addon.getSetting('langType')).lower()
tvsort = (Addon.getSetting('tvsortType')).lower()
moviessort = (Addon.getSetting('moviessortType')).lower()

base_url = 'http://www.dittotv.com'
base2_url = '/tvshows/all/0/'+language+'/'

def addon_log(string):
    if debug == 'true':
        xbmc.log("[plugin.video.ditto-rain-%s]: %s" %(addon_version, string))

def make_request(url):
    try:
    	headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0', 'Accept' : 'text/html,application/xhtml+xml,application/xml'}
        if url == None:
        	url = base2_url
        request = urllib2.Request(url,None,headers)
        response = urllib2.urlopen(request)
        data = response.read()
        response.close()
        return data
    except urllib2.URLError, e:    # This is the correct syntax
        print e
        ##sys.exit(1)
        
def get_menu():
    
    addDir(2, '[COLOR orange][B]TV Shows[/B][/COLOR]', '', '')
    addDir(3, '[COLOR white][B]Movies[/B][/COLOR]', '', '')        
    addDir(4, '[COLOR green][B]Live TV[/B][/COLOR]', '', '')
    addDir(5, 'Search', '', '')

def get_search():
    if url:
	    search_url = base_url+url
    else:
        keyb = xbmc.Keyboard('', 'Search for Movies/TV Shows/Trailers/Videos in all languages')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search_term = urllib.quote_plus(keyb.getText())
			
        search_url = 'http://www.dittotv.com/search/all/0/'+search_term
	
    r=make_request(search_url)
    soup = BeautifulSoup(r, 'html5lib')
    tag_cataloglist = soup.findAll('div', {'class' : 'catalog-item'})
    for catalog in tag_cataloglist:
		if (catalog.find('span', {'class':'category_image'}).text != 'Live TV'):
			tag_link_title = catalog.find('span', {'class':'category_image'}).text + ' - '+catalog('h1')[0]['title']
			full_tag_link = catalog.find('a').attrs.get('href')
			tag_img = catalog.find('img').attrs.get('src')
			addDir(8, tag_link_title, full_tag_link, tag_img, False)
			
    if soup.find('a', attrs={"class" : "next-epg next-disabled"}):
        print "next-epg-disabled"
    else:        
        tag_next = soup.find('a', attrs={"class" : "next-epg"})
        if tag_next:
            next = tag_next.attrs.get('href','')
            if -1 == next.find('javascript:void(0)'):
                addDir(5, '>>> Next Page >>>', next, '')

def get_livetv():
    base4_url = 'http://www.dittotv.com/livetv/all/0/'+language
    r = make_request(base4_url)

    soup = BeautifulSoup(r, 'html5lib')
    #tag_cataloglist = soup.findAll('div', {'class' : 'row movies-all-outerWrap program-all-set'})
    tag_cataloglist = soup.findAll('div', {'class' : 'subpattern2 movies-all-indi channels-all alltvchannel'})
    for catalog in tag_cataloglist:
        tag_link = catalog('a')[0]['href']
        full_tag_link = tag_link
        tag_link_title = catalog('a')[0]['title']
        tag_img = catalog.find('img').attrs.get('src')
        addDir(8, tag_link_title, full_tag_link, tag_img, False)

        
def get_movies():
    base3_url = '/movies/all/0/'+language
    
    if url:
        r=make_request(base_url+url)
    else:
        r = make_request(base_url+base3_url)

    soup = BeautifulSoup(r, 'html5lib')
    tag_cataloglist = soup.findAll('div', {'class' : 'catalog-item mb1'})

    for catalog in tag_cataloglist:
        tag_link = catalog.find('a', {'class' : 'title-link'}).attrs.get('href')
        full_tag_link = tag_link
        tag_link_title = catalog.find('a', {'class' : 'title-link'}).attrs.get('title')
        tag_img = catalog.find('img').attrs.get('src')
        addDir(8, tag_link_title, full_tag_link, tag_img, False)  

    if soup.find('a', attrs={"class" : "next-epg next-disabled"}):
        print "next-epg-disabled"
    else:        
        tag_next = soup.find('a', attrs={"class" : "next-epg"})
        if tag_next:
            next = tag_next.attrs.get('href','')
            if -1 == next.find('javascript:void(0)'):
                addDir(3, '>>> Next Page >>>', next, '')
	if (moviessort == "name"):
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )				
        
def get_shows():
    
    if url:
        r=make_request(base_url+url)
    else:
        r = make_request(base_url+base2_url)

    soup = BeautifulSoup(r, 'html5lib')
    tag_cataloglist = soup.findAll('div', {'class' : 'catalog-item'})

    for catalog in tag_cataloglist:
        tag_link = catalog.find('a', {'class' : 'title-link'}).attrs.get('href')
        full_tag_link = tag_link
        tag_link_title = catalog.find('a', {'class' : 'title-link'}).attrs.get('title')
        tag_img = catalog.find('img').attrs.get('src')
        addDir(1, tag_link_title, full_tag_link, tag_img, False)
    
    if soup.find('a', attrs={"class" : "next-epg next-disabled"}):
        print "next-epg-disabled"
    else:        
        tag_next = soup.find('a', attrs={"class" : "next-epg"})
        if tag_next:
            next = tag_next.attrs.get('href','')
            if -1 == next.find('javascript:void(0)'):
                addDir(2, '>>> Next Page >>>', next, '')
	if (tvsort == "name"):
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )


def get_episodes():
    r = make_request(base_url+url+'/episodes')

    soup = BeautifulSoup(r, 'html5lib')
    tag_cataloglist = soup.findAll('div', {'class' : 'catalog-item'})
    
    for catalog in tag_cataloglist:
        tag_link = catalog.find('a').attrs.get('href')
        full_episode_link = tag_link
        tag_link_title = catalog.find('a', {'class' : 'title-link'}).attrs.get('title')
        tag_img = catalog.find('img').attrs.get('src')
        addDir(8, tag_link_title, full_episode_link, tag_img, False)
    
def get_livetv_url():
    addon_log('get_video_url: begin...')
    videos = []
    html = make_request(base_url+url)
    # matchlist = re.compile('([^"]*(?=m3u8).*?["])').findall(str(html))
    encurl = re.findall(r'\"file\":\"(.+?)\"', html)[0]
    if 'livetv' in url:
        key = re.findall(r'value=\"(.*?)\" class=\"livetv-url-val\"', html)[0]
    else:
        key = re.findall(r'value=\"(.*?)\" class=\"e-url-val\"', html)[0]
    decrypted = GetLSProData(key=key, iv='00000000000000000000000000000000', data=encurl)

    params = re.compile("(http://[^']*\/)").findall(decrypted)
    if params:
        params = params[0]
    else:
        params = ''
	
    html2 = make_request(decrypted)
    if html2:
		matchlist2 = re.compile("BANDWIDTH=([0-9]+)[^\n]*\n([^\n]*)\n").findall(str(html2))
		if matchlist2:
			for (size, video) in matchlist2:
				if size:
					size = int(size)
				else:
					size = 0
				video=params+video
				videos.append( [size, video] )
    else:
        videos.append( [-2, match] )

    videos.sort(key=lambda L : L and L[0], reverse=True)

    for video in videos:
        if -1 == video[0]:
            size = '[Auto] '
        elif -2 == video[0]:
            size = '[Windows] '
        else:
            size = '[' + str(video[0]) + '] '
        addDir(0, size + name, video[1], image, True)

    addon_log('get_video_url: end...')    

	#Thanks Shani(LSP)
def GetLSProData(key,iv,data):
    import binascii
    key=base64.b64decode(key)
    iv=binascii.unhexlify(iv)
    data=base64.b64decode(data)
    decryptor = pyaes.new(key, pyaes.MODE_CBC, IV=iv)
    val1= decryptor.decrypt(data)
    val2= repr(val1).partition('\\')
    retval= val2[0].replace('\'', '')
    return retval
	
def addDir(mode,name,url,image,isplayable=False):
    name = name.encode('utf-8', 'ignore')
    url = url.encode('utf-8', 'ignore')
    image = image.encode('utf-8', 'ignore')

    if 0==mode:
        link = url
    else:
        link = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&image="+urllib.quote_plus(image)

    ok=True
    item=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
    item.setInfo( type="Video", infoLabels={ "Title": name } )
    isfolder=True
    if isplayable:
        item.setProperty('IsPlayable', 'true')
        isfolder=False
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=link,listitem=item,isFolder=isfolder)
    return ok

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

params=get_params()
mode=None
name=None
url=None
image=None

try:
    mode=int(params["mode"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    image=urllib.unquote_plus(params["image"])
except:
    pass

addon_log("Mode: "+str(mode))
addon_log("Name: "+str(name))
addon_log("URL: "+str(url))
addon_log("Image: "+str(image))

if mode==None:
	get_menu()
    
if mode==2:
    get_shows()

if mode==3:
    get_movies()
    
if mode==4:
    get_livetv()

if mode==5:
	get_search()
	
if mode==1:
    get_episodes()

if mode==8:
    get_livetv_url()
    
if mode==11:
    get_video_url()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
