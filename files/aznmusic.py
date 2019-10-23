#!/usr/bin/python
#coding=utf-8

import os, re, urllib, urllib2, base64
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

Addon_ID = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(Addon_ID)
mycode = base64.b64decode
home = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))
icon = os.path.join(home, 'icon.png')
fanart = os.path.join(home, 'fanart.jpg')
logosLoc = os.path.join(home, 'resources', 'logos')
linkicon = os.path.join(logosLoc, 'linkicon.png')
playicon = os.path.join(logosLoc, 'playicon.png')
settingsicon = os.path.join(logosLoc, 'settings.png')
myk = mycode('YXpub\1\n\WVkaWE=\2\=\?')
mybase = 'ye7i3diemJDD4-LP2sfUxtWo3d_Mk8rbz-fT0c7FmNPG6t3gztjY09qoz-fTktbGxePPnNfF4JDO2-HhytaY'

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
		return link
	except:
		pass

def get_categories():
	add_dir('[COLOR lightblue]Add-on Settings[/COLOR]', 'settings', 3, settingsicon, fanart)
	add_dir('[COLOR lightgreen][I]Thử link mới[/I][/COLOR]', 'playablelink', 1, linkicon, fanart)
	content = make_request(key(myk, mybase+'0c3b59nO193UkNvo29LZ3MrEqc_n09He1Mrd29LT2ZfOlO8='))
	match = re.compile('#(.+?),(.+)\s*(.+)\s*').findall(content)
	for group_logo, title, link in match:
		if 'tvg-logo' in group_logo:
			thumb = re.compile('tvg-logo=[\'"](.*?)[\'"]').findall(str(group_logo))
			if len(thumb) > 0:
				thumb = thumb[0].strip()
				if thumb.startswith('http'):
					thumb = thumb.replace(' ', '%20')
			else:
				thumb = icon
		else:
			thumb = icon
		if 'tvg-fanart' in group_logo:
			fanartlogo = re.compile('tvg-fanart=[\'"](.*?)[\'"]').findall(str(group_logo))
			if len(fanartlogo) > 0:
				fanartlogo = fanartlogo[0].strip()
				if fanartlogo.startswith('http'):
					fanartlogo = fanartlogo.replace(' ', '%20')
			else:
				fanartlogo = fanart
		else:
			fanartlogo = fanart
		add_dir(title, link, 2, thumb, fanartlogo)

def test_link():
	try:
		keyb = xbmc.Keyboard('', 'Nhập link muốn thử')
		keyb.doModal()
		if (keyb.isConfirmed()):
			url = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
			if len(url) > 0:
				add_link('[COLOR lightgreen][I]Nhấn vào đây để play[/I][/COLOR]', url, playicon, fanart)
			else:
				get_categories()
		else:
			get_categories()
	except:
		pass

def collections(url):
	fanartlogo = (key(myk, mybase+'zdDh3eCUidzN0OHdnMvF18LT7pzX1cs=')%((url.split("/")[-1]).split(".")[0]))
	content = make_request(url)
	match = re.compile('#(.+?),(.+)\s*(.+)\s*').findall(content)
	for logo, title, link in match:
		if 'tvg-logo' in logo:
			thumb = re.compile('tvg-logo=[\'"](.*?)[\'"]').findall(str(logo))
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
		link = link.strip()
		if ('https://www.youtube.com/user/' in link) or ('https://www.youtube.com/channel/' in link) or ('plugin.video.xshare/?mode=90&page=0&url' in link) or ('plugin://plugin.video.azn.thuynga' in link):
			add_dir(title, link, 100, thumb, fanartlogo)
		else:
			add_link(title, link, thumb, fanartlogo)

def addon_settings():
	addon.openSettings()
	sys.exit(0)

def key(k, e):
	dec = []
	e = base64.urlsafe_b64decode(e)
	for i in range(len(e)):
		k_c = k[i % len(k)]
		dec_c = chr((256 + ord(e[i]) - ord(k_c)) % 256)
		dec.append(dec_c)
	return "".join(dec)

def resolve_url(url):
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def add_dir(name, url, mode, iconimage, fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
	ok=True
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
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=4"
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
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

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass

if mode == None:
	get_categories()

elif mode == 1:
	test_link()

elif mode == 2:
	collections(url)

elif mode == 3:
	addon_settings()

elif mode == 4:
	resolve_url(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))