#!/usr/bin/python
#coding=utf-8

# Start of asking for user input
from sys import version_info
py3 = version_info[0] > 2 # creates boolean value for test that Python major version > 2
if py3:
  response = input("Please enter 1 for creating M3U or 2 for XML: ")
else:
  response = raw_input("Please enter 1 for creating M3U or 2 for XML: ")
# End of asking for user input

import re, os, time

KodiFavourite = os.path.expanduser('~/AppData/Roaming/Kodi/userdata/favourites.xml')
m3u_dst = os.path.expanduser('~/Desktop/KodiFavourites.m3u')
xml_dst = os.path.expanduser('~/Desktop/KodiFavourites.xml')

f = open(KodiFavourite, 'r')
content = f.read()
f.close()

if response == '1':
	if os.path.exists(m3u_dst):
		os.rename(m3u_dst, m3u_dst.split('.')[0]+time.strftime("_%m%d%Y_%H%M%S.m3u"))
	ff = open(m3u_dst, 'a+')
	ff.write('#EXTM3U\n\n')
	match = re.compile('<favourite name="(.*?)"(.+?)\&quot;(.+?)\&quot;.*\)<\/favourite>').findall(content)
	for name, mode, url in match:
		url = url.replace('&amp;', '&')
		if "thumb" in mode:
			thumb = re.compile('thumb="(.*?)">').findall(mode)[0]
		else:
			thumb = "https://www.freeiconspng.com/uploads/favorites-icon-png-29.png"
		if "ActivateWindow" in mode:
			pass
		elif "PlayMedia" in mode:
			ff.write('#EXTINF:-1 tvg-logo="'+thumb+'",'+name+'\n'+url+'\n')
	ff.write('\n\n\n\n')
	ff.close()

if response == '2':
	if os.path.exists(xml_dst):
		os.rename(xml_dst, xml_dst.split('.')[0]+time.strftime("_%m%d%Y_%H%M%S.xml"))
	ff = open(xml_dst, 'a+')
	ff.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n\n<channel>\n<items>\n\n')
	match = re.compile('<favourite name="(.*?)"(.+?)\&quot;(.+?)\&quot;.*\)<\/favourite>').findall(content)
	for name, mode, url in match:
		url = url.replace('&amp;', '&')
		if "thumb" in mode:
			thumb = re.compile('thumb="(.*?)">').findall(mode)[0]
		else:
			thumb = "https://www.freeiconspng.com/uploads/favorites-icon-png-29.png"
		if "ActivateWindow" in mode:
			ff.write('<item>\n<title>'+name+'</title>\n<link>'+url+'</link>\n<thumbnail>'+thumb+'</thumbnail>\n<mode>300</mode>\n</item>\n\n')
		elif "PlayMedia" in mode:
			ff.write('<item>\n<title>'+name+'</title>\n<link>'+url+'</link>\n<thumbnail>'+thumb+'</thumbnail>\n<mode>1</mode>\n</item>\n\n')
	ff.write('</items>\n</channel>')
	ff.close()