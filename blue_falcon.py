#!/usr/local/bin/python
# coding: latin-1
#
#
#Blue Falcon Brian Peters AKA Dreadnaught
#Inspired by RED_HAWK by Tuhinshubhra AKA R3D#@X0R_2HIN
#
# @url: https://www.dreadnaught.info
# @url: https://github.com/dreadnaughtsec/falcon
#
# Copyright (c) 2017, Dreadnaught Security
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from this
# software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import subprocess
from platform import system
import os
import urlparse
import sys
import urllib2
from bs4 import BeautifulSoup

# ##############################
#        BANNER GRAB SECTION
# ##############################

def grabBanner():
	global target
	p = subprocess.Popen(["curl -I " + target], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	
	print(out)
	
	quitCheck()

# ##############################
#        CMS DETECTION SECTION
# ##############################

def detectCMS():
	print("\n") #just a little house keeping
	global target
	#Dictionary of CMS signatures
	cmsDict = {"/wp-content/": "WordPress", "/wp-login.php": "WordPress", "/wp-admin/": "WordPress", "/wp-uploads/": "WordPress", "/templates/": "Joomla!", "/misc/drupal.js": "Drupal"}
	#list with just signautes
	cmsKeys = cmsDict.keys()
	#list of html based signatures
	htmlDict = {'<meta name="generator" content="WordPress"': 'WordPress', '<meta content="WordPress': 'Wordpress', 'id="wp-admin-bar-': 'WordPress', '/wp-content/themes/': 'WordPress', "JFactory::getDocument()->setGenerator('');": 'Joomla!', 
'<meta name="generator" content="Joomla': 'Joomla!', '<meta name="generator" content="Drupal': 'Drupal', 'Static.SQUARESPACE_CONTEXT': 'SquareSpace', 'SQUARESPACE_ROLLUPS,': 'SquareSpace', 
'Adirondack5093f261e4b0979eac7cb299': 'SquareSpace', 'Adversary515c7bd0e4b054dae3fcf003': 'SquareSpace', 'Alex515c7bd0e4b054dae3fcf003': 'SquareSpace', 'Anya52a74dafe4b073a80cd253c5': 'SquareSpace', 
'Aubrey507c1fdf84ae362b5e7be44e': 'SquareSpace', 'Avenue4fd11f32c4aad9b01c9e624c': 'SquareSpace', 'Aviator507c1fdf84ae362b5e7be44e': 'SquareSpace', 'Bedford52a74dafe4b073a80cd253c5': 'SquareSpace', 
'Boutique4fdf4f21c4aad4a72790bd9b': 'SquareSpace', 'Bryant52a74dafe4b073a80cd253c5': 'SquareSpace', 'Dovetail4fef25bbe4b0ea9df05ac51e': 'SquareSpace', 'Encore507c1fdf84ae362b5e7be44e': 'SquareSpace', 
'Five503ba86de4b04953d0f49846': 'SquareSpace', 'Flatiron4fba57fde4b0f79d428daa8b': 'SquareSpace', 'Forte51e6b9e4e4b062dafa7099b9': 'SquareSpace', 'Frontrow4fb6ba24e4b000ba644d8298': 'SquareSpace', 
'Fulton52e96934e4b0ea14d0f64568': 'SquareSpace', 'Galapagos5230da18e4b0a637f7e627c5': 'SquareSpace', 'Hayden52a74dafe4b073a80cd253c5': 'SquareSpace', 'Horizon52e96934e4b0ea14d0f64568': 'SquareSpace', 
'Ishimoto4fb7a14224ac99c5fee12515': 'SquareSpace', 'Marquee515c7bd0e4b054dae3fcf003': 'SquareSpace', 'Momentum50130f5be4b00a22f5c5a82a': 'SquareSpace', 'Montauk50521cf884aeb45fa5cfdb80': 'SquareSpace', 
'Native4f6a1392e4b07090d46e7ec9': 'SquareSpace', 'Om50521cf884aeb45fa5cfdb80': 'SquareSpace', 'Pacific52e96934e4b0ea14d0f64568': 'SquareSpace', 'Peak500589fc84aed5ec11c2b672': 'SquareSpace', 
'Shift515c7bd0e4b054dae3fcf003': 'SquareSpace', 'Supply5253022fe4b0d0363260861e': 'SquareSpace', 'Wells4f9adc1524ac5df956fdf98f': 'SquareSpace', 'Wexley4fbff70b84aeca67fb3a3c56': 'SquareSpace', 
'configDomain = "www.weebly.com"': 'Weebly', '.checkout.weebly.com': 'Weebly', 'weebly_new_window"': 'Weebly', 'a title="weebly': 'Weebly', 'alt="weebly': 'Weebly', 'Code for Weebly -->': 'Weebly', 
'<meta name="generator" content="TYPO3 CMS': 'Typo3 CMS', '/typo3conf/': 'Typo3 CMS', '/typo3temp/': 'Typo3 CMS', 'website is powered by TYPO3': 'Typo3 CMS', 'jimdo_layout_css': 'Jimdo', 'jimdoData': 'Jimdo', 
'jimdoCom': 'Jimdo', 'JimdoHelpCenter': 'Jimdo', 'jimdo.com/app/cms': 'Jimdo', 'jimdo.com/app/auth': 'Jimdo', 'content="Microsoft SharePoint': 'SharePoint', '="dnn_sdLanguage': 'DNN', 'name="dnn$': 'DNN', 
'id="dnn_ControlPanel': 'DNN', 'id="dnn_mobLogin': 'DNN', '="dnn_dnn': 'DNN', '="dnn_Search': 'DNN', '="dnn$Search': 'DNN', '"/js/dnn.js': 'DNN', '/dnncore': 'DNN', 'dnn.controls': 'dnn', 'dnn_dnnBREADCRUMB': 'DNN'}
	htmlKeys = htmlDict.keys()
	
	for item in cmsKeys:
		#if response is 200, then we can assume the path is valid and not a redirect
		p = subprocess.Popen(["curl -I " + target + item], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = p.communicate()
		
		if("200 OK" in out):
			print("Detected " + green + cmsDict[item] + yellow + " @ " + target + item )
		elif("302 Found" in out):
			print("Detected " + green + cmsDict[item] + yellow + " @ " + target + item )
			
	#now to pull a copy of the page with bs4 and scrape the page for html signatures for further CMS detection
	source = urllib2.urlopen(target).read()
	soup = BeautifulSoup(source, "html5lib")
	soupString = soup.prettify().encode('utf-8')

	#iterate through all html signatures for further detection
	for item in htmlKeys:
		if item in soupString:
			print("Detected " + green + htmlDict[item] + yellow + " @ " + target + " in source with signature: " + magenta + item + yellow)
	
	quitCheck()

# ##############################
#        CDN DETECTION SECTION
# ##############################
def detectCDN():
	global target
	#setup list of CDN signatures with corresponding brand names
	cdnDict = {".cdn.cloudflare.net": "CloudFlare", ".x.incapdns.net": "Incapsula", "p-usmi00.kxcdn.com": "KeyCDN", ".akamaiedge.net": "Akamai", ".globalredir.akadns.net": "Akamai", ".akamai.net": "Akamai", ".edgesuite.net": "Akamai", 
".cloudfront.net": "CloudFront", ".eld.amazonaws.com": "CloudFront", "g5.cachefly.net": "CacheFly", ".adn.alphacdn": "EdgeCast", ".wac.edgecastcdn.net": "EdgeCast", ".adn.omicroncdn.net": "EdgeCast", ".adn.phicdn.net": "EdgeCast", 
".cdn.bitgravity.com": "BitGravity", ".global.fastly.net": "Fastly", ".map.fastly.net": "Fastly", ".stackpathdns.com": "FireBlade", ".netdna-cdn.com": "MaxCDN", ".netlify.com": "Netliify"}
	cdnKeys = cdnDict.keys()
	
	#we need to strip http and https from the target for accurate results
	if("http://" in target):
		cdnTarget = target.replace("http://", '')
	elif("https://" in target):
		cdnTarget = target.replace("https://", '')
	else:
		cdnTarget = target
	
	#p runs a dig against the target. out holds the successul output data, err holds any error data
	p = subprocess.Popen(["dig", cdnTarget], stdout=subprocess.PIPE)
	out, err = p.communicate()
	
	#now cycle through signatures and look for a match
	#print("Dig target:" + cdnTarget) #debug use only
	#print("Dig response:\n" + str(out)) #debug use only
	cdnDetected = False
	for item in cdnKeys:
		if(item in str(out)):
			print(cdnDict[item] + " Detected!")
			cdnDetected = True
			break
		
	if(not cdnDetected):
		print("No CDN Detected")
		
	quitCheck()

# ##############################
#        TARGET SECTION
# ##############################

def setTarget():
	banner()
	global target
	min_attr = ('scheme' , 'netloc')
	validURL = False
	while not validURL:
		target = raw_input("\033[1;33mEnter target URL [\033[1;35mhttp(s)://www.something.com\033[1;33m]:\033[0;0m")
		#check to see if URL is "valid"
		result = urlparse.urlsplit(target)

		if not result.scheme or not result.netloc:
			print("\033[1;31mPlease enter valid URL ...\033[1;33m")
		else:
			validURL = True
			
	mainMenu()

# ##############################
#        UI HANDLING SECTION
# ##############################

def clearScreen():
	clear = "cls" if system().lower()=="windows" else "clear" #creating the clear command for win/osx/nix
	os.system(clear)

def banner():
	clearScreen()
	#display the main menu 
	global blue
	global yellow
	global red
	global magenta
	global off
	print(blue + """	       _/_/_/_/          _/   """ + off + """  (╯°□°)╯︵ 0˙Ɩ uoᴉsɹǝʌ""" + blue + """
	      _/        _/_/_/  _/    _/_/_/    _/_/    _/_/_/    
	     _/_/_/  _/    _/  _/  _/        _/    _/  _/    _/   
	    _/      _/    _/  _/  _/        _/    _/  _/    _/    
	   _/        _/_/_/  _/    _/_/_/    _/_/    _/    _/\n\n""" + off)

def mainMenu():
	banner()
	global target
	valid = False
	while not valid:
		print("Target URL: " + target)
		print(yellow + "[" + green + "1" + yellow + "] Detect CDN\n[" + green + "2" + yellow + "] Detect CMS\n[" + green + "3" + yellow + "] Grab Banner\n[" + green + "R" + yellow + "] Reset Target URL\n[" + red + "Q" + yellow + "] Quit\n")
		select = raw_input("Please Make A Selection:")
		if(select == "1"):
			detectCDN()
			banner()
		if(select == "2"):
			detectCMS()
			banner()
		if(select == "3"):
			grabBanner()
			banner()
		if(select.upper() == "R"):
			setTarget()
		if(select.upper() == "Q"):
			sys.exit(0)

def quitCheck():
	global clear
	valid = False
	while not valid:
		answer = raw_input("\n[" + green + "M" + yellow + "]ain Menu, [" + green + "R" + yellow + "]eset Target, [" + red + "Q" + yellow + "]uit?:")
		if(answer.upper() == "M"):
			clearScreen()
			mainMenu()
		elif(answer.upper() == "R"):
			clearScreen()
			setTarget()
			mainMenu()
		elif(answer.upper() == "Q"):
			sys.exit(0)
		else:
			print("Invalid Selection")

# ##############################
#        INITIALIZATION SECTION
# ##############################

#setup color list for easy printing
yellow = "\033[1;33m"
green = "\033[1;32m"
blue = "\033[1;34m"
cyan = "\033[1;36m"
red = "\033[1;31m"
magenta = "\033[1;35m"
darkyellow = "\033[0;33m"
darkgreen = "\033[0;32m"
darkblue = "\033[0;34m"
darkcyan = "\033[0;36m"
darkred = "\033[0;31m"
darkmagenta = "\033[0;35m"
off = "\033[0;0m"


target = "No Target Set" #global for target website url
cdn = "Null"

setTarget()