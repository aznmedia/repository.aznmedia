#!/usr/bin/python
#coding=utf-8

from sqlite3 import dbapi2 as db_lib
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib, urllib2, sys, re, os, shutil, base64, time, zipfile

KodiVersion = int(xbmc.getInfoLabel("System.BuildVersion")[:2])
plugin_handle = int(sys.argv[1])

Addon_ID = xbmcaddon.Addon().getAddonInfo('id')
mysettings = xbmcaddon.Addon(Addon_ID)
Addon_Name = mysettings.getAddonInfo('name')
Addon_Version = mysettings.getAddonInfo('version')
Addon_Author = mysettings.getAddonInfo('author')
profile = xbmc.translatePath(mysettings.getAddonInfo('profile').decode('utf-8'))
home = xbmc.translatePath(mysettings.getAddonInfo('path').decode('utf-8'))
icon = os.path.join(home, 'icon.png')
fanart = os.path.join(home, 'fanart.jpg')
LocalizedString = mysettings.getLocalizedString
mycode = base64.b64decode

xmlfile = os.path.join(profile, 'settings.xml')
datafiles = os.path.join(home, 'resources', 'datafiles')
packagesLoc = xbmc.translatePath('special://home/addons/packages')

xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
m3u_thumb_regex = 'tvg-logo=[\'"](.*?)[\'"]'
m3u_regex = '#(.+?),(.+)\s*(.+)\s*'
dialog = xbmcgui.Dialog()

myDict = {';':'', '&amp;':'&', '&quot;':'"', '.':' ', '&#39;':'\'', '&#038;':'&', '&#039':'\'',\
          '&#8211;':'-', '&#8220;':'"', '&#8221;':'"', '&#8230':'...', 'u0026quot':'"'}

#skinpath   = xbmc.translatePath('special://skin')
#xbmc.log("Printing skinpath: %s"%skinpath,xbmc.LOGNOTICE)

#skinname = xbmc.getSkinDir()
#xbmc.log("Printing skinname: %s"%skinname,xbmc.LOGNOTICE)

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

def read_file(file):
	try:
		f = open(file, 'r')
		content = f.read()
		f.close()
		return content
	except:
		pass

def replace_all(text, myDict):
	try:
		for a, b in myDict.iteritems():
			text = text.replace(a, b)
		return text
	except:
		pass

def platform():
	if xbmc.getCondVisibility('system.platform.android'):
		return 'android'
	elif xbmc.getCondVisibility('system.platform.linux'):
		return 'linux'
	elif xbmc.getCondVisibility('system.platform.windows'):
		return 'windows'
	elif xbmc.getCondVisibility('system.platform.osx'):
		return 'osx'
	elif xbmc.getCondVisibility('system.platform.atv2'):
		return 'atv2'
	elif xbmc.getCondVisibility('system.platform.ios'):
		return 'ios'

def set_enabled(newaddon, data=None):
	if KodiVersion > 16:
		try:
			#xbmc.log("Printing Enabling: %s" % newaddon, xbmc.LOGNOTICE)
			setit = 1
			if data is None: data = ''
			sql = 'REPLACE INTO installed (addonID,enabled) VALUES(?,?)'
			db_path = xbmc.translatePath(os.path.join('special://profile', 'Database', 'Addons27.db'))
			conn = db_lib.connect(db_path)
			conn.execute(sql, (newaddon, setit,))
			conn.commit()
		except:
			pass
	else:
		pass

def setall_enable():
	if KodiVersion > 16:
		try:
			addonfolder = xbmc.translatePath(os.path.join('special://home', 'addons'))
			contents = os.listdir(addonfolder)
			#xbmc.log('%s: %s' % ('ADDON FOLDER', contents), xbmc.LOGNOTICE)
			db_path = xbmc.translatePath(os.path.join('special://profile', 'Database', 'Addons27.db'))
			conn = db_lib.connect(db_path)
			conn.executemany('update installed set enabled=1 WHERE addonID = (?)', ((val,) for val in contents))
			conn.commit()
		except:
			pass
	else:
		pass

def extract_all(_in, _out, dp):
	zin = zipfile.ZipFile(_in,  'r')
	nFiles = float(len(zin.infolist()))
	count = 0
	try:
		for item in zin.infolist():
			count += 1
			update = count / nFiles * 100
			dp.update(int(update))
			zin.extract(item, _out)
	except:
		return False
	return True

def key(k, e):
	dec = []
	e = base64.urlsafe_b64decode(e)
	for i in range(len(e)):
		k_c = k[i % len(k)]
		dec_c = chr((256 + ord(e[i]) - ord(k_c)) % 256)
		dec.append(dec_c)
	return "".join(dec)

def re_fresh():
	return xbmc.executebuiltin("XBMC.Container.Refresh")

def set_view(vnum):
	return xbmc.executebuiltin('Container.SetViewMode(%s)' % vnum)

def ico(s):
	return '%s/%s.png' % (iconpath, s)

def get_m3u(url):
	if url == othersources:
		mode = '111'
	else:
		mode = ''
	content = make_request(url)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		if 'script.navi-x' in url:
			pass
		else:
			exodus = xbmc.translatePath('special://home/addons/plugin.video.exodus')
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				if thumb.startswith('http'):
					if 'Exodus' in name and os.path.exists(exodus):
						addDir(name, 'exodus', 220, thumb, True)
					else:
						addDir(name, url, mode, thumb, True)
				else:
					thumb = '%s/%s' % (iconpath, thumb)
					if 'Exodus' in name and os.path.exists(exodus):
						addDir(name, 'exodus', 220, thumb, True)
					else:
						addDir(name, url, mode, thumb, True)
			else:
				if 'Exodus' in name and os.path.exists(exodus):
					addDir(name, 'exodus', 220, icon, True)
				else:
					addDir(name, url, mode, icon, True)

def get_xml(url):
	content = make_request(url)
	match = re.compile(xml_regex+'\s*<mode>(.*?)</mode>').findall(content)
	for name, url, thumb, mode in match:
		if mode == '1' or mode == '3':
			addDir(name, url, mode, thumb, False)
		else:
			addDir(name, url, mode, thumb, True)

def run_exodus():
	xbmc.executebuiltin("RunAddon(plugin.video.exodus)")

def main():
	#addDir('[COLOR lightblue][B]Viet Hai Ngoai 2[/B][/COLOR]', 'plugin://plugin.tivi9999.viettv24', 999, 'https://bitbucket.org/aznmedia/repository.azn.media/raw/master/playlists/viplist/icons/viettv24_2.png', True)
	content = make_request(mainmenu)
	#content = read_file(os.path.expanduser(r'~\Desktop\mainmenu.xml'))
	match = re.compile(xml_regex+'\s*<mode>(.*?)</mode>').findall(content)
	for name, url, thumb, mode in match:
		if mode == '1' or mode == '3':
			addDir(name, url, mode, thumb, False)
		else:
			addDir(name, url, mode, thumb, True)
	if platform() == 'windows' or platform() == 'osx':
		addDir('[COLOR violet][B]Tutorials +[/B][/COLOR]', tutsurl, 27, ico('tutsplus'), True)
	addDir('[COLOR green][B]Add-on Settings[/B][/COLOR]', 'NoURL', 2, ico('settings'), True)

def add_AVSource():
	addDir('[COLOR blue][B]Play Fshare Link Using VNOP Addon[/B][/COLOR]', 'Fshare', 45, ico('fsharevip'), True)
	addDir('[COLOR violet][B]Play Fshare Link Using VMF Addon[/B][/COLOR]', 'Fshare', 46, ico('fsharevip'), True)
	addDir('[COLOR lightgreen][B]Play Fshare Link Using Xshare Addon[/B][/COLOR]', 'Fshare', 47, ico('fsharevip'), True)
	addDir('[COLOR red][B]Play Google Drive Link Using VNOP Addon[/B][/COLOR]', 'VNOPGoogleDrive', 48, ico('GoogleDrive'), True)
	addDir('[COLOR magenta][B]Play Google Drive Link Using VMF Addon[/B][/COLOR]', 'VMFGoogleDrive', 49, ico('GoogleDrive'), True)
	addDir('[COLOR lime][B]Online Link - Link Trên Mạng[/B][/COLOR]', 'Online_AV', 40, ico('onlineav'), True)
	addDir('[COLOR yellow][B]Play Local Video/Audio File - Play Video/Audio Trong Máy[/B][/COLOR]', 'Local_AV', 42, ico('localav'), True)
	addDir('[COLOR cyan][B]Local M3U Playlist - M3U Playlist Trong Máy[/B][/COLOR]', 'localplaylist', 41, ico('local'), True)
	addDir('[COLOR orange][B]Online M3U Playlist - M3U Playlist Trên Mạng[/B][/COLOR]', 'onlineplaylist', 41, ico('online'), True)
	addDir('[COLOR lightblue][B]Local XML Playlist - XML Playlist Trong Máy[/B][/COLOR]', 'local_xml', 44, ico('localxml'), True)
	addDir('[COLOR green][B]Add-on Settings[/B][/COLOR]', 'NoURL', 2, ico('settings'), True)

def addon_settings():
	clearcache()
	mysettings.openSettings()
	sys.exit(0)

def recycle_bin():
	addDir('[COLOR yellow][B]Xoá Cache[/B][/COLOR]', 'cache', 50, ico('clearcache'), True)
	addDir('[COLOR cyan][B]Delete Packages[/B][/COLOR]', 'packages', 51, ico('delpackages'), True)
	addDir('[COLOR blue][B]Delete Thumbnails[/B][/COLOR]', 'thumbnails', 52, ico('delthumbnails'), True)
	addDir("[COLOR lime][B]Clear LastPlayed's History[/B][/COLOR]", 'LastPlayedHistory', 54, ico('clearLastPlayed'), True)

def clear_cache():  #### plugin.video.xbmchubmaintenance ####
	try:
		xbmc_cache_path = xbmc.translatePath('special://temp')
		if os.path.exists(xbmc_cache_path) == True:
			for root, dirs, files in os.walk(xbmc_cache_path):
				file_count = 0
				file_count += len(files)
				if file_count > 0:
					if dialog.yesno('Delete Kodi Cache Files', '%s %s' % (str(file_count), 'file(s) found'), 'Do you want to delete them?', '%s %s %s'%('[COLOR magenta]Muốn xoá', str(file_count), 'file(s) trong cache không?[/COLOR]')):
						clearcache()
						dialog.ok('Delete Kodi Cache Files', 'Done', "", '[COLOR magenta]Đã làm xong[/COLOR]')
				else:
					sys.exit(0)
	except:
		pass
	sys.exit(0)

def clearcache():
	try:
		xbmc_cache_path = xbmc.translatePath('special://temp')
		if os.path.exists(xbmc_cache_path) == True:
			for root, dirs, files in os.walk(xbmc_cache_path):
				for f in files:
					try:
						os.unlink(os.path.join(root, f))
					except:
						pass
				for d in dirs:
					if any(x in d for x in ['subs', 'xshare', 'temp']):
						pass
					else:
						try:
							shutil.rmtree(os.path.join(root, d))
						except:
							pass
		else:
			pass
		sys.exit(0)
	except:
		pass

def del_packages():  #### plugin.video.xbmchubmaintenance ####
	try:
		for root, dirs, files in os.walk(packagesLoc):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				if dialog.yesno('Delete Package Cache Files', '%s %s' % (str(file_count), 'file(s) found'), 'Do you want to delete them?', '%s %s %s'%('[COLOR magenta]Muốn xoá', str(file_count), 'file(s) này không?[/COLOR]')):
					for f in files:
						os.unlink(os.path.join(root, f))
					for d in dirs:
						shutil.rmtree(os.path.join(root, d))
					dialog.ok('Delete Package Cache Files', 'Done', "", '[COLOR magenta]Đã làm xong[/COLOR]')
			else:
				dialog.ok('Delete Package Cache Files', 'No zip file found.', "", '[COLOR magenta]Không tìm thấy zip file.[/COLOR]')
	except:
		pass
	sys.exit(0)

def del_thumbnails():  #### script.rawmaintenance ####
	thumbnailPath = xbmc.translatePath('special://thumbnails')
	try:
		if os.path.exists(thumbnailPath)==True:  
			if dialog.yesno('Delete Thumbnails', 'This option deletes all thumbnails.', 'Are you sure you want to do this?', '[COLOR magenta]Bạn có muốn xoá tất cả các thumbnails không?[/COLOR]'):
				for root, dirs, files in os.walk(thumbnailPath):
					file_count = 0
					file_count += len(files)
					if file_count > 0:
						for f in files:
							try:
								os.unlink(os.path.join(root, f))
							except:
								pass
				dialog.ok('Delete Thumbnails', 'Please manually restart Kodi to rebuild thumbnail library.', '[COLOR magenta]Vui lòng tự khởi động lại Kodi để tái tạo lại thư viện thumbnail.[/COLOR]')
			else:
				sys.exit(0)
	except:
		pass
	sys.exit(0)

def clear_LastPlayed():
	historyFile = xbmc.translatePath('special://profile/addon_data/plugin.video.last_played/lastPlayed.json')
	try:
		if os.path.exists(historyFile)==True:
			if dialog.yesno('Clear history cache of Last Played Add-on', 'Bạn có muốn xoá toàn bộ danh sách lưu trữ của Last Played Add-on không?'):
				os.remove(historyFile)
				dialog.ok('Clear history cache of Last Played Add-on', 'Done', "", '[COLOR magenta]Đã làm xong[/COLOR]')
			else:
				sys.exit(0)
		else:
			dialog.ok('Clear history cache of Last Played Add-on', 'Không tìm thấy danh sách lưu trữ của Last Played Add-on.')
	except:
		pass
	sys.exit(0)

def other_sources():
	get_m3u(othersources)

def other_sources_list(url, iconimage):
	content = make_request(url)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			if not 'tvg-logo' in thumb:
				thumb = iconimage
			m3u_playlist(name, url, thumb)
		except:
			pass

def m3u_playlist(name, url, thumb):
	name = re.sub('\s+', ' ', name).strip()
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if any(x in url for x in ['youtube.com/user/', 'youtube.com/channel/', 'youtube/user/', 'youtube/channel/']):
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			addDir(name, url, '', thumb, True)
		else:
			addDir(name, url, '', icon, True)
	else:
		if 'youtube.com/watch?v=' in url:
			url = ('plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1]))
		else:
			url = url
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			if 'plugin://plugin' in url:
				if 'youtube' in url:
					addDir(name, url, 1, thumb, False)
				else:
					addDir(name, url, 3, thumb, False)
			else:
				addDir(name, url, 1, thumb, False)
		else:
			if 'plugin://plugin' in url:
				if 'youtube' in url:
					addDir(name, url, 1, icon, False)
				else:
					addDir(name, url, 3, icon, False)
			elif thumb.startswith('http'):
				addDir(name, url, 1, thumb, False)
			else:
				addDir(name, url, 1, icon, False)

def other_addons():
	get_m3u(otheraddons)

def update_repo():
	xbmc.executebuiltin('XBMC.UpdateLocalAddons()')
	xbmc.executebuiltin('XBMC.UpdateAddonRepos()')
	xbmc.executebuiltin('XBMC.Container.Refresh')
	xbmc.executebuiltin('XBMC.Container.Update')

def install_repos(headTitle):
	try:
		for root, dirs, files in os.walk(packagesLoc):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	except:
		pass
	try:
		if KodiVersion > 17:
			#ReposLoc = os.path.expanduser(r'~\Desktop\allinone18.zip')
			ReposLoc = mainloc + 'allinone18.zip'
			RepoZip = os.path.basename(ReposLoc)
			repoGroup = os.path.join(packagesLoc, RepoZip)
			#ReposDataLoc = os.path.expanduser(r'~\Desktop\allinoneuserdata18.zip')
			ReposDataLoc = mainloc + 'allinoneuserdata18.zip'
			RepoDataZip = os.path.basename(ReposDataLoc)
			repoDataGroup = os.path.join(packagesLoc, RepoDataZip)
			dp = xbmcgui.DialogProgress()
			dp.create(headTitle, 'Downloading big zip file... Please wait...', '[COLOR magenta]Đang tải zip file dung lượng lớn... Vui lòng chờ...[/COLOR]')
			#shutil.copy(ReposLoc, repoGroup)
			urllib.urlretrieve(ReposLoc, repoGroup)
			#shutil.copy(ReposDataLoc, repoDataGroup)
			urllib.urlretrieve(ReposDataLoc, repoDataGroup)
			time.sleep(1)
			dp.update(0, 'Extracting zip files... Please wait...', '[COLOR magenta]Đang giải nén zip files... Vui lòng chờ...[/COLOR]')
			addonfolder = xbmc.translatePath('special://home')
			extract_all(repoGroup, addonfolder, dp)
			time.sleep(1)
			extract_all(repoDataGroup, addonfolder, dp)
			time.sleep(1)
			update_repo()
		else:
			#ReposLoc = os.path.expanduser(r'~\Desktop\allinone.zip')
			ReposLoc = mainloc + 'allinone.zip'
			RepoZip = os.path.basename(ReposLoc)
			repoGroup = os.path.join(packagesLoc, RepoZip)
			#ReposDataLoc = os.path.expanduser(r'~\Desktop\allinoneuserdata.zip')
			ReposDataLoc = mainloc + 'allinoneuserdata.zip'
			RepoDataZip = os.path.basename(ReposDataLoc)
			repoDataGroup = os.path.join(packagesLoc, RepoDataZip)
			dp = xbmcgui.DialogProgress()
			dp.create(headTitle, 'Downloading big zip file... Please wait...', '[COLOR magenta]Đang tải zip file dung lượng lớn... Vui lòng chờ...[/COLOR]')
			#shutil.copy(ReposLoc, repoGroup)
			urllib.urlretrieve(ReposLoc, repoGroup)
			#shutil.copy(ReposDataLoc, repoDataGroup)
			urllib.urlretrieve(ReposDataLoc, repoDataGroup)
			time.sleep(1)
			dp.update(0, 'Extracting zip files... Please wait...', '[COLOR magenta]Đang giải nén zip files... Vui lòng chờ...[/COLOR]')
			addonfolder = xbmc.translatePath('special://home')
			extract_all(repoGroup, addonfolder, dp)
			time.sleep(1)
			extract_all(repoDataGroup, addonfolder, dp)
			time.sleep(1)
			update_repo()
	except:
		pass
	if os.path.isfile(repoGroup) == True:
		os.remove(repoGroup)
	if os.path.isfile(repoDataGroup) == True:
		os.remove(repoDataGroup)

def tutorial_links(url):
	content = make_request(url)
	if url.endswith('m3u'):
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'plugin.program.chrome.launcher' in url:
				if 'tvg-logo' in thumb:
					thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
					if thumb.startswith('http'):
						addDir(name, url, None, thumb, True)
					else:
						thumb = '%s/%s' % (iconpath, thumb)
						addDir(name, url, None, thumb, True)
				else:
					addDir(name, url, None, icon, True)
			else:
				if 'tvg-logo' in thumb:
					thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
					if thumb.startswith('http'):
						addDir(name, url, 1, thumb, False)
					else:
						thumb = '%s/%s' % (iconpath, thumb)
						addDir(name, url, 1, thumb, False)
				else:
					addDir(name, url, 1, icon, False)
	elif url.endswith('xml'):
		match = re.compile(xml_regex).findall(content)
		for name, url, thumb in match:
			if 'plugin.program.chrome.launcher' in url:
				addDir(name, url, None, thumb, True)
			else:
				addDir(name, url, 1, thumb, False)

def youtube_menu(url):
	content = make_request(url)
	match = re.compile(xml_regex+'\s*<mode>(.*?)</mode>').findall(content)
	for name, url, thumb, mode in match:
		addDir(name, url, mode, thumb, True)

def youtube_channels(url):
	content = make_request(url)
	match = re.compile(xml_regex).findall(content)
	for name, url, thumb in match:
		addDir(name, url, None, thumb, True)

def mi_a_mi():
	content = make_request(world)
	match = re.compile(m3u_regex).findall(content)
	for items in match:
		thumb = ('%s%s' % ('http://www.giniko.com/logos/190x110/', re.compile(m3u_thumb_regex).findall(items[0])[0]))
		addDir(items[1], items[2], 1, thumb, False)

def play_other_video(url):
	item = xbmcgui.ListItem(path = url)
	xbmc.sleep(1000)
	xbmc.Player().play(url, item, False, -1)

def play_video(url):
	if url.startswith('idn'):
		url = 'http://www.giniko.com/watch.php?id=%s' % url.split('=')[-1]
		url = re.compile('file: "(.+?)"').findall(make_request(url))[0]
	else:
		url = url
	item = xbmcgui.ListItem(name, path = url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	if len(subtitle) > 0:
		try:
			xbmc.sleep(3000)
			xbmc.Player().setSubtitles(subtitle)
		except:
			pass
	return

def channelTester():
	try:
		keyb = xbmc.Keyboard('', 'Enter Channel Name [COLOR lime]- Nhập Tên Kênh (Dùng Tiếng Việt Không Dấu)[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			name = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
		keyb = xbmc.Keyboard('', 'Enter Channel URL [COLOR lime]- Nhập URL[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			url = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
		keyb = xbmc.Keyboard('', 'Enter Logo URL [COLOR lime]- Nhập Logo URL (Không Bắt Buộc)[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			thumb = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
		if len(name) > 0 and len(url) > 0:
			if len(thumb) < 1:
				thumb = icon
			if 'plugin://plugin' in url:
				addDir(name, url, 3, thumb, False)
			else:
				addDir(name, url, 1, thumb, False)
	except:
		pass

def GoogleDrive_VNOP():
	try:
		keyb = xbmc.Keyboard('', 'Enter Google Drive Link')
		keyb.doModal()
		if (keyb.isConfirmed()):
			url = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
			if 'https://drive.google.com/file/d/' in url:
				url = url.replace('https://drive.google.com/file/d/','plugin://plugin.video.thongld.vnplaylist/play/https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F') + '/View'
			elif 'https://drive.google.com/open?id=' in url:
				url = url.replace('https://drive.google.com/open?id=','plugin://plugin.video.thongld.vnplaylist/play/https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F') + '/View'
			elif 'https://drive.google.com' not in url:
				url = ('plugin://plugin.video.thongld.vnplaylist/play/https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F') + url + '/View'
		if len(url) > 0:
			thumb = 'https://bitbucket.org/aznmedia/repository.azn.media/raw/master/playlists/viplist/iconpath/GoogleDrive.png'
			addDir('VNOP Google Drive Link', url, 1, thumb, False)
	except:
		pass

def Fshare_VNOP():
	try:
		keyb = xbmc.Keyboard('', 'Enter Fshare Link')
		keyb.doModal()
		if (keyb.isConfirmed()):
			url = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
			if 'file' in url: 
				url = (url.replace('https://www.fshare.vn/file/','plugin://plugin.video.thongld.vnplaylist/play/https%3A%2F%2Fwww.fshare.vn%2Ffile%2F'))+'/FshareFile'
			elif 'folder' in url:
				url = (url.replace('https://www.fshare.vn/folder/','plugin://plugin.video.thongld.vnplaylist/fshare/https%3A%2F%2Fwww.fshare.vn%2Ffolder%2F'))+'/FshareFolder'
		if len(url) > 0:
			thumb = 'https://bitbucket.org/aznmedia/repository.azn.media/raw/master/playlists/viplist/fshare/icons/fsharevip.png'
			if 'file' in url:
				addDir('Fshare File', url, 1, thumb, False)
			elif 'folder' in url:
				addDir('Fshare Folder', url, 555, thumb, True)
	except:
		pass

def GoogleDrive_VMF():
	try:
		keyb = xbmc.Keyboard('', 'Enter Google Drive Link')
		keyb.doModal()
		if (keyb.isConfirmed()):
			url = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
			if 'https://drive.google.com/file/d/' in url:
				url = 'plugin://plugin.video.vietmediaF?action=play&url=' + url
			elif 'https://drive.google.com/open?id=' in url:
				url = 'plugin://plugin.video.vietmediaF?action=play&url=' + url.replace('https://drive.google.com/open?id=','https://drive.google.com/file/d/') + '/View'
			elif 'https://drive.google.com' not in url:
				url = ('plugin://plugin.video.vietmediaF?action=play&url=https://drive.google.com/file/d/') + url + '/View'
		if len(url) > 0:
			thumb = 'https://bitbucket.org/aznmedia/repository.azn.media/raw/master/playlists/viplist/iconpath/GoogleDrive.png'
			addDir('VMF Google Drive Link', url, 1, thumb, False)
	except:
		pass

def Fshare_VMF():
	try:
		keyb = xbmc.Keyboard('', 'Enter Fshare Link')
		keyb.doModal()
		if (keyb.isConfirmed()):
			url = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
			if 'file' in url: 
				url = ('plugin://plugin.video.vietmediaF?action=play_direct_link_play&url=') + url
			elif 'folder' in url:
				url =('plugin://plugin.video.vietmediaF/?action=play&url=') + url
		if len(url) > 0:
			thumb = 'https://bitbucket.org/aznmedia/repository.azn.media/raw/master/playlists/viplist/fshare/icons/fsharevip.png'
			if 'file' in url:
				addDir('Fshare File', url, 1, thumb, False)
			elif 'folder' in url:
				addDir('Fshare Folder', url, 555, thumb, True)
	except:
		pass
		
def Fshare_Xshare():
	try:
		keyb = xbmc.Keyboard('', 'Enter Fshare Link')
		keyb.doModal()
		if (keyb.isConfirmed()):
			url = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
			if 'file' in url: 
				url = ('plugin://plugin.video.xshare/?mode=3&page=0&url=') + url
			elif 'folder' in url:
				url = ('plugin://plugin.video.xshare/?mode=90&page=0&url=') + url
		if len(url) > 0:
			thumb = 'https://bitbucket.org/aznmedia/repository.azn.media/raw/master/playlists/viplist/fshare/icons/fsharevip.png'
			if 'file' in url:
				addDir('Fshare File', url, 1, thumb, False)
			elif 'folder' in url:
				addDir('Fshare Folder', url, 555, thumb, True)
	except:
		pass

def play_localav():
	local_av = mysettings.getSetting('local_av')
	if len(local_av) < 1:
		mysettings.openSettings()
	else:
		if os.path.exists(local_av) == True:
			name = local_av.split("\\")[-1].split("/")[-1]
			thumb = ico('localvideo')
			url = local_av
			addDir(name, url, 1,thumb, False)
		else:
			dialog.ok('Enter Logo URL [COLOR lime]- Nhập Logo URL (Không Bắt Buộc)[/COLOR]', 'Video file does not exist. Please choose another video to play.', '[COLOR magenta]Không có video này. Vui lòng chọn xem video khác.[/COLOR]')
			with open(xmlfile, 'r') as f:
				lines = f.readlines()
			with open(xmlfile, 'w') as f:
				for line in lines:
					if not 'id="local_av"' in line:
						f.write(line)
			re_fresh()

def XML_Tester():
	clearcache()
	local_xml_path = mysettings.getSetting('localxml_path')
	if len(local_xml_path) < 1:
		mysettings.openSettings()
		sys.exit(0)
	else:
		if os.path.isfile(local_xml_path):
			content = read_file(local_xml_path)
		else:
			with open(xmlfile, 'r') as f:
				lines = f.readlines()
			with open(xmlfile, 'w') as f:
				for line in lines:
					if not 'id="local_xml_path"' in line:
						f.write(line)
				dialog.ok('Warning - Cảnh Báo', '[COLOR red]%s[/COLOR]' % local_xml_path, 'File no longer exists. Please choose another XML playlist.', '[COLOR magenta]File không còn tồn tại. Vui lòng chọn danh sách XML khác.[/COLOR]')
				sys.exit(0)
			mysettings.openSettings()
	match = re.compile(xml_regex+'\s*<mode>(.*?)</mode>').findall(content)
	for name, url, thumb, mode in match:
		if mode == '1' or mode == '3':
			addDir(name, url, mode, thumb, False)
		else:
			addDir(name, url, mode, thumb, True)

def playlistTester(url):
	clearcache()
	local_path = mysettings.getSetting('local_path')
	online_link = mysettings.getSetting('online_link')
	if url == 'localplaylist':
		if len(local_path) < 1:
			mysettings.openSettings()
			sys.exit(0)
		else:
			content = read_file(local_path)
	else:
		if len(online_link) < 1:
			mysettings.openSettings()
			sys.exit(0)
		else:
			content = make_request(online_link)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

def addDir(name, url, mode, iconimage, isFolder = False):
	u = (sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) +\
		 "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage))
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	if iconimage == fanart:
		liz.setProperty('fanart_image', fanart)
	else:
		liz.setProperty('fanart_image', iconimage)
	if not isFolder:
		liz.setProperty('IsPlayable', 'true')
	elif any(x in url for x in ['plugin://plugin', 'script://script']):
		u = url
	elif any(x in url for x in ['www.youtube.com/user/', 'www.youtube.com/channel/', 'www.youtube.com/playlist/']):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
	ok = xbmcplugin.addDirectoryItem(plugin_handle, url = u, listitem = liz, isFolder = isFolder)
	return ok

mykbase = mycode('eWU3aTNkaWVtSkRENC1MUDJzZlV4dFdvM2Rf\2\n\TWs4cmJ6LWZUMGM3Rm1O\
                  UEc2dDNnenRqWTA5cW96LWZUa3RiR3hlUFBuTmZGNEpETzItSGh5dGFZ\?\=\4')
myk = mycode('YXpub\1\n\WVkaWE=\2\=\?')
base_url = 'https://bitbucket.org/aznmedia/repository.azn.media/raw/master/'
baseurl = base_url + 'playlists/viplist/'
mainloc = base_url + 'RepoZips/'
iconpath = baseurl + 'iconpath'
tutsurl = baseurl + 'tutoriallinks.m3u'
otheraddons = baseurl + 'otheraddons.txt'
othersources = baseurl + 'othersources.txt'
mainmenu = baseurl + 'mainmenu.xml'
subtitle = baseurl + 'ReservedFiles/aznmedia.srt'

params = get_params()

url = None
name = None
mode = None
iconimage = None

try: url = urllib.unquote_plus(params["url"])
except: pass
try: name = urllib.unquote_plus(params["name"])
except: pass
try: mode = int(params["mode"])
except: pass
try: iconimage = urllib.unquote_plus(params["iconimage"])
except: pass

if mode == None or url == None or len(url) < 1:
	easyinstaller = os.path.join(datafiles, 'EasyInstaller.txt')
	if os.path.exists(easyinstaller) == True:
		d = dialog.yesno('Easy Installer', '- Nhấn Có (Yes) để cài tất cả các [COLOR magenta]repos và add-ons[/COLOR]')
		if d:
			try:
				install_repos('Easy Installer')
				os.remove(easyinstaller)
				time.sleep(1)
				setall_enable()
				time.sleep(1)
				update_repo()
				time.sleep(1)
				try:
					#xbmcaddon.Addon('plugin.video.vietmediaF').setSetting(id='check', value='true')
					xbmcaddon.Addon('plugin.video.vietmediaF').setSetting(id='on_off', value='false')
					xbmcaddon.Addon('plugin.video.vietmediaF').setSetting(id='view_mode', value='true')
					xbmcaddon.Addon('plugin.video.itvplus').setSetting(id='big_icon', value='true')
					xbmcaddon.Addon('plugin.video.itvplus').setSetting(id='auto_mode', value='false')
					xbmcaddon.Addon('plugin.video.itvplus').setSetting(id='temp_mode', value='true')
				except:
					pass
				time.sleep(1)
				shutil.rmtree(datafiles)
				time.sleep(1)
				update_repo()
				time.sleep(1)
				dialog.ok('Easy Installer',"Cần phải reboot Kodi để hoàn thành việc setup. Chúc bạn thưởng thức vui vẻ!")
				xbmc.executebuiltin("XBMC.ActivateWindow(ShutdownMenu)")
			except:
				dialog.ok('Easy Installer','[COLOR magenta][B]Có lỗi xảy ra. Vui lòng thử lại sau.[/B][/COLOR]')
		else:
			sys.exit(0)
	else:
		main()
		set_view(500)


elif mode == 1:
	play_video(url)

elif mode == 2:
	addon_settings()

elif mode == 3:
	play_other_video(url)

elif mode == 18:
	youtube_menu(url)
	set_view(500)

elif mode == 19:
	youtube_channels(url)

elif mode == 27:
	tutorial_links(url)

elif mode == 40:
	channelTester()

elif mode == 41:
	playlistTester(url)

elif mode == 42:
	play_localav()

elif mode == 43:
	add_AVSource()

elif mode == 44:
	XML_Tester()

elif mode == 45:
	Fshare_VNOP()

elif mode == 46:
	Fshare_VMF()

elif mode == 47:
	Fshare_Xshare()

elif mode == 48:
	GoogleDrive_VNOP()

elif mode == 49:
	GoogleDrive_VMF()

elif mode == 50:
	clear_cache()

elif mode == 51:
	del_packages()

elif mode == 52:
	del_thumbnails()

elif mode == 53:
	recycle_bin()

elif mode == 54:
	clear_LastPlayed()

elif mode == 99:
	mi_a_mi()

elif mode == 100:
	other_addons()
	set_view(500)

elif mode == 110:
	other_sources()

elif mode == 111:
	other_sources_list(url, iconimage)

elif mode == 120:
	adult_addons()
	set_view(500)

elif mode == 121:
	adult_videos(url)

elif mode == 200:
	get_m3u(url)

elif mode == 210:
	get_xml(url)

elif mode == 220:
	run_exodus()

xbmcplugin.endOfDirectory(plugin_handle)