#!/usr/bin/python
#coding=utf-8

import xbmc,xbmcaddon,os,re

adultAddons=["plugin.video."+x for x in ["adulthideout","AznKodiAdult","beeg.com","beegcom","cherrypie","empflix","ero-tik","erotik","fantasticc","javstream","jfh","korea-xxx","likuoo","lubetube","pornhub","tube8","uwc","videodevil","woodrocket","xxx-o-dus","XXXtreme","you.jizz"]]

thongAddons=["plugin.video.kodi4vn."+x for x in ["bilutv","launcher","moviebox","phimbathu","xomgiaitri"]]

def start_up():
	try:
		xbmcaddon.Addon("plugin.video.azn.media").setSetting(id="enable_adult_section", value="false")	# Disable adult section on AznMedia add-on at startup.
		hide_adult_addons()
		#show_adult_addons()
		noAds()
	except:
		pass

def hide_adult_addons():	# Hide all adult add-ons installed by AznMedia add-on
	try:
		for addonName in adultAddons:
			addon_xml=xbmc.translatePath("special://home/addons/%s/addon.xml"%addonName)
			if os.path.exists(addon_xml):
				with open(addon_xml) as f:
					content=f.read()
					match=re.compile("<provides>(.*?)</provides>").findall(content)
					if "video" in match:
						content=content.replace("<provides>%s</provides>"%match[0],"<provides></provides>")
						with open(addon_xml,"w") as f:
							f.write(content)
					else:
						pass
			else:
				pass
	except:
		pass

def show_adult_addons():	# Show all adult add-ons installed by AznMedia add-on
	try:
		for addonName in adultAddons:
			addon_xml=xbmc.translatePath("special://home/addons/%s/addon.xml"%addonName)
			if os.path.exists(addon_xml):
				with open(addon_xml) as f:
					content=f.read().replace("<provides></provides>","<provides>video</provides>")
				with open(addon_xml,"w") as f:
					f.write(content)
			else:
				pass
	except:
		pass

def noAds():	# Remove VietTV24's ads.
	try:
		for addonName in thongAddons:
			default_py=xbmc.translatePath("special://home/addons/%s/default.py"%addonName)
			if os.path.exists(default_py):
				if "xomgiaitri" in default_py:
					with open(default_py,"r+") as f:
						data = ''.join([i for i in f if not "i1I1iI . doModal ( )" in i])
						f.seek(0)
						f.write(data)
						f.truncate()
				else:
					with open(default_py,"r+") as f:
						data = ''.join([i for i in f if not "doModal" in i])
						f.seek(0)
						f.write(data)
						f.truncate()
			else:
				pass
	except:
		pass

if __name__=="__main__":
	start_up()