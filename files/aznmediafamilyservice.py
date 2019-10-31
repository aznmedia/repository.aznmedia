#!/usr/bin/python
#coding=utf-8

import xbmc,os

#adultAddons=["plugin.video."+x for x in ["ccloudtv","tnp.mediashare"]]
adultAddons=["plugin.video.tnp.mediashare"]

def start_up():
	try:
		del_packages()
		remove_adult_sections()
		#add_adult_sections()
	except:
		pass

def remove_adult_sections():	# Remove adult sections on cCloudTV and MediaShare add-ons
	try:
		for addonName in adultAddons:
			addon_xml=xbmc.translatePath("special://home/addons/%s/resources/settings.xml"%addonName)
			if os.path.exists(addon_xml):
				if addonName=="plugin.video.ccloudtv":
					with open(addon_xml) as f:
						content=f.read()
						if not ('		<setting type="lsep" label="Adult Section"/>\n		<setting id="enable_adult_section" type="bool" label="Enable Adult Section (by enabling, you confirm you are 18+)" default="false" />') in content:
							pass
						else:
							content=content.replace('		<setting type="lsep" label="Adult Section"/>\n		<setting id="enable_adult_section" type="bool" label="Enable Adult Section (by enabling, you confirm you are 18+)" default="false" />\n','')
							with open(addon_xml,"w") as f:
								f.write(content)
				elif addonName=="plugin.video.tnp.mediashare":
					with open(addon_xml) as f:
						content=f.read()
						if not ('  <category label="[COLOR magenta]Adults[/COLOR]">\n    <setting id="adult" type="bool" label="[COLOR red][B]For Adults 18+[/B][/COLOR]" default="false" />\n  </category>') in content:
							pass
						else:
							content=content.replace('  <category label="[COLOR magenta]Adults[/COLOR]">\n    <setting id="adult" type="bool" label="[COLOR red][B]For Adults 18+[/B][/COLOR]" default="false" />\n  </category>\n','')
							with open(addon_xml,"w") as f:
								f.write(content)
			else:
				pass
	except:
		pass

def add_adult_sections():	# Add adult sections back to cCloudTV and MediaShare add-ons
	try:
		for addonName in adultAddons:
			addon_xml=xbmc.translatePath("special://home/addons/%s/resources/settings.xml"%addonName)
			if os.path.exists(addon_xml):
				if addonName=="plugin.video.ccloudtv":
					with open(addon_xml) as f:
						content=f.read()
						if '		<setting type="lsep" label="Adult Section"/>\n		<setting id="enable_adult_section" type="bool" label="Enable Adult Section (by enabling, you confirm you are 18+)" default="false" />' in content:
							pass
						else:
							content=content.replace('	<category label="General">','	<category label="General">\n		<setting type="lsep" label="Adult Section"/>\n		<setting id="enable_adult_section" type="bool" label="Enable Adult Section (by enabling, you confirm you are 18+)" default="false" />')
							with open(addon_xml,"w") as f:
								f.write(content)
				elif addonName=="plugin.video.tnp.mediashare":
					with open(addon_xml) as f:
						content=f.read()
						if '  <category label="[COLOR magenta]Adults[/COLOR]">\n    <setting id="adult" type="bool" label="[COLOR red][B]For Adults 18+[/B][/COLOR]" default="false" />\n  </category>\n</settings>' in content:
							pass
						else:
							content=content.replace('</settings>','  <category label="[COLOR magenta]Adults[/COLOR]">\n    <setting id="adult" type="bool" label="[COLOR red][B]For Adults 18+[/B][/COLOR]" default="false" />\n  </category>\n</settings>')
							with open(addon_xml,"w") as f:
								f.write(content)
			else:
				pass
	except:
		pass

def del_packages(): 	# Delete all add-on zipfiles in packages
	try:
		for root, dirs, files in os.walk(xbmc.translatePath('special://home/addons/packages')):
			file_count = 0
			file_count += len(files)
			for f in files:
				os.unlink(os.path.join(root, f))
			for d in dirs:
				shutil.rmtree(os.path.join(root, d))
	except:
		pass

if __name__=="__main__":
	start_up()