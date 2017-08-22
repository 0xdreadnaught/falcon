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

#from bs4 import BeautifulSoup

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
	
	for item in cmsKeys:
		#if response is 200, then we can assume the path is valid and not a redirect
		p = subprocess.Popen(["curl -I " + target + item], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = p.communicate()
		
		if("200 OK" in out):
			print("Detected " + green + cmsDict[item] + yellow + " @ " + target + item )
		elif("302 Found" in out):
			print("Detected " + green + cmsDict[item] + yellow + " @ " + target + item )
	
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