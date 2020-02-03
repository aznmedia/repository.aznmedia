﻿#!/usr/bin/python
#coding=utf-8

import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib, sys, re, os, base64

KodiVersion = int(xbmc.getInfoLabel("System.BuildVersion")[:2])
if KodiVersion > 18:
	from urllib.request import Request, urlopen
	from urllib.parse import quote_plus
else:
	import urllib2

Addon_ID = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(Addon_ID)
mycode = base64.b64decode
home = xbmc.translatePath(addon.getAddonInfo('path'))
logosLoc = os.path.join(home, 'resources', 'logos')
linkicon = os.path.join(logosLoc, 'linkicon.png')
playicon = os.path.join(logosLoc, 'playicon.png')
settingsicon = os.path.join(logosLoc, 'settings.png')
icon = os.path.join(home, 'icon.png')
fanart = os.path.join(home, 'fanart.jpg')
myk = mycode('YXpub\1\n\WVkaWE=\2\=\?')
mybase = 'ye7i3diemJDD4-LP2sfUxtWo3d_Mk8rbz-fT0c7FmNPG6t3gztjY09qoz-fTktbGxePPnNfF4JDO2-HhytaY'

def make_request(url):
	if KodiVersion > 18:
		try:
			req = Request(url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
			response = urlopen(req)
			link = response.read().decode('utf-8')
			response.close()
			return link
		except:
			pass
	else:
		try:
			req = urllib2.Request(url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
			response = urllib2.urlopen(req)
			link = response.read()
			response.close()
			return link
		except:
			pass

def get_categories(url):
	#xbmc.log("Printing url: %s"%url,xbmc.LOGNOTICE)
	if url == None:
		add_dir('Add-on Settings', 'settings', 1, settingsicon, fanart)
		add_dir('[COLOR lightgreen][I]Thử link mới[/I][/COLOR]', 'playablelink', 2, linkicon, fanart)
		content = make_request(key(myk, mybase+'0c3b59nO193UkNvo29LZ3MrEqeLV2t3XyMKo26Da'))
	else:
		content = make_request(url)
	match = re.compile('#(.+?),(.+)\s*(.+)\s*').findall(content)
	for group_logo, title, url in match:
		if 'tvg-logo' in group_logo:
			thumb = re.compile('tvg-logo=[\'"](.*?)[\'"]').findall(str(group_logo))
			if len(thumb) > 0:
				thumb = thumb[0].strip()
				if thumb.startswith('http'):
					thumb = thumb.replace(' ', '%20')
				elif thumb == 'server.png':
					thumb = os.path.join(logosLoc, 'server.png')
				else:
					thumb = icon
			else:
				thumb = icon
		else:
			thumb = icon
		title = title.strip()
		url = url.strip()
		if ('https://www.youtube.com/user/' in url) or ('https://www.youtube.com/channel/' in url) or ('/section/' in url) or ('folder' in url):
			add_dir(title, url, 100, thumb, fanart)
		elif ('https://bitbucket.org' in url):
			add_dir(title, url, None, thumb, fanart)
		else:
			add_link(title, url, thumb, fanart)

def test_link():
	try:
		keyb = xbmc.Keyboard('', 'Nhập link muốn thử')
		keyb.doModal()
		if (keyb.isConfirmed()):
			if KodiVersion > 18:
				url = urllib.parse.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
			else:
				url = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
			if len(url) > 0:
				add_link('[COLOR lightgreen][I]Nhấn vào đây để play[/I][/COLOR]', url, playicon, fanart)
			else:
				get_categories(url)
		else:
			get_categories(url)
	except:
		pass

def addon_settings():
	addon.openSettings()
	sys.exit(0)

def key(k, e):
	dec = []
	e = base64.urlsafe_b64decode(e)
	for i in range(len(e)):
		k_c = k[i % len(k)]
		if KodiVersion > 18:
			dec_c = chr((256 + (e[i]) - (k_c)) % 256)
		else:
			dec_c = chr((256 + ord(e[i]) - ord(k_c)) % 256)
		dec.append(dec_c)
	return "".join(dec)

def resolve_url(url):
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def add_dir(name, url, mode, iconimage, fanart):
	if KodiVersion > 18:
		u = (sys.argv[0] + "?url=" + urllib.parse.quote_plus(url) + "&mode=" + str(mode))
		ok = True
		liz = xbmcgui.ListItem(name)
		liz.setArt({ 'poster': iconimage })
	else:
		u = (sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode))
		ok = True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty("Fanart_Image", fanart)
	if ('https://www.youtube.com/user/' in url) or ('https://www.youtube.com/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
	elif ('plugin.video.xshare/?mode=90&page=0&url' in url) or ('plugin://plugin.video.azn.thuynga' in url):
		u = url
	ok=xbmcplugin.addDirectoryItem(int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def add_link(name, url, iconimage, fanart):
	if KodiVersion > 18:
		u = (sys.argv[0] + "?url=" + urllib.parse.quote_plus(url) + "&mode=3")
		ok = True
		liz = xbmcgui.ListItem(name)
		liz.setArt({ 'poster': iconimage })
	else:
		u = (sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=3")
		ok = True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty("Fanart_Image", fanart)
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(int(sys.argv[1]),url=u,listitem=liz)
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

params = get_params()

url = None
name = None
mode = None
iconimage = None

if KodiVersion > 18:
	try: url = urllib.parse.unquote_plus(params["url"])
	except: pass
	try: name = urllib.parse.unquote_plus(params["name"])
	except: pass
	try: mode = int(params["mode"])
	except: pass
	try: iconimage = urllib.parse.unquote_plus(params["iconimage"])
	except: pass
else:
	try: url = urllib.unquote_plus(params["url"])
	except: pass
	try: name = urllib.unquote_plus(params["name"])
	except: pass
	try: mode = int(params["mode"])
	except: pass
	try: iconimage = urllib.unquote_plus(params["iconimage"])
	except: pass

xbmc.log("==================== AznThuyNga ====================",xbmc.LOGNOTICE)
xbmc.log("NAME: %s"%name,xbmc.LOGNOTICE)
xbmc.log("URL: %s"%url,xbmc.LOGNOTICE)
xbmc.log("MODE: %s"%mode,xbmc.LOGNOTICE)
xbmc.log("ICONIMAGE: %s"%iconimage,xbmc.LOGNOTICE)
xbmc.log("==================================================",xbmc.LOGNOTICE)

if mode == None:
	get_categories(url)

elif mode == 1:
	addon_settings()

elif mode == 2:
	test_link()

elif mode == 3:
	resolve_url(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
