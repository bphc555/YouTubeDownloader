from __future__ import unicode_literals
import youtube_dl
import re
import requests
import urllib
import os
from urllib import urlopen


#parse the playlist url to get list of videos' links. Store the links in a file.
def getList(url):
	playlist = set()
	page = requests.get(url)
	if (page.status_code == 404):
		print "404 client error"
	html = urlopen(url).read()
	string = str(html)
	#get the playlist id
	index = url.rfind('=')
	listId = url[index+1:]
	"""
	now find re /watch?v= & listId
	href of a link is href="/watch?v=BWRQAbxriH8&amp;index=5&amp;list=PLwgprUN2IFAtT_33QCrsPh6wzqwF88YqW"
	i.e. /watch?v= + some random string which is not \n or \t or \r etc + list = playlist id of playlist.	
	"""
	toFind = re.compile('watch\?v=\S+list=' + listId)
	matches = re.findall(toFind,string)
	if matches:
		for u in matches:
			index = u.find('&',0,len(u))
			vidId = u[:index]
			playlist.add('https://www.youtube.com/' + vidId)
	#store the list in a file
	fileOfLink = open("link.txt","w")	
	for addrs in playlist:
		print addrs
		fileOfLink.write(addrs)
		fileOfLink.write("\n")
	fileOfLink.close()
	download()	

# method specific to youtube-dl to download videos
def my_hook(d):
	if d['status'] == 'error':
		print "Sorry an error occured"
	elif d['status'] == 'finished':
		print "Download Successfully finished"

#options for youtube-dl
ydl_opts = {
	'progress_hooks' :[my_hook]} #explore option to resume download after errors

def download():
	print "Starting download"
	#open the file for all the links
	fileOfLink = open("link.txt","r")
	for line in fileOfLink:
		print line
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([line])
		
#get url of playlist from user, verify if it is a list
def getUrl():
	print "Enter your playlist"
	url = raw_input()
	url = 'https://www.youtube.com/playlist?list=PLwgprUN2IFAtT_33QCrsPh6wzqwF88YqW'
	if 'list' in url: 	#verify if url is a playlist or not
		print "ok downloading videos"
	else:
		print "Please give a valid url of playlist"
	getList(url)

#to set the directory where user wants to store videos
def getDir():
	print "Specify your download directory"
	myDownloadDir = raw_input()
	print myDownloadDir
	os.chdir(myDownloadDir) #check for valid path in future
	print "Your videos will be stored in " + myDownloadDir
	getUrl()


if __name__ == "__main__":
	getDir()
