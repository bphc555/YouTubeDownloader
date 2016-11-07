from __future__ import unicode_literals
import youtube_dl
import re
import requests
import urllib
import os
from urllib import urlopen

playlist = []

def getList(url):
	global playlist
	temp = set()
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
			temp.add('http://www.youtube.com/' + vidId)
	for addrs in temp:
		print addrs
		playlist.append(addrs)	


def my_hook(d):
	if d['status'] == 'error':
		print "Sorry an error occured"
	elif d['status'] == 'finished':
		print "Download Successfully finished"

ydl_opts = {
	'progress_hooks' :[my_hook]}

def download():
	print "The following videos will be downloaded:"
	for string in playlist:
		print string 
	#with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	#	ydl.download([url])

def getUrl():
	print "Enter your playlist"
	url = raw_input()
	url = 'https://www.youtube.com/playlist?list=PLwgprUN2IFAtT_33QCrsPh6wzqwF88YqW'
	if 'list' in url: 	#verify if url is a playlist or not
		print "ok downloading videos"
	else:
		print "Please give a valid url of playlist"
	getList(url)

def getDir():
	print "Specify your download directory"
	myDownloadDir = raw_input()
	print myDownloadDir
	os.chdir(myDownloadDir) #check for valid path if future
	print "Your videos will be stored in " + myDownloadDir
	getUrl()


if __name__ == "__main__":
	getDir()
