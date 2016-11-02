import re
import requests
import urllib
from urllib import urlopen

def getList(url):
	playlist = []
	temp = set()
	page = requests.get(url)
	if (page.status_code == 404):
		print "404 client error"
	html = urlopen(url).read()
	string = str(html)
	#get the playlist id
	index = url.rfind('=')
	listId = url[index+1:]
	#now find re /watch?v= & listId
	#href of a link is href="/watch?v=BWRQAbxriH8&amp;index=5&amp;list=PLwgprUN2IFAtT_33QCrsPh6wzqwF88YqW"
	#i.e. /watch?v= + some random string which is not \n or \t or \r etc + list = playlist id of playlist.	
	toFind = re.compile('watch\?v=\S+list=' + listId)
	matches = re.findall(toFind,string)
	if matches:
		for u in matches:
			index = u.find('&',0,len(u))
			vidId = u[:index]
			temp.add('http://www.youtube.com/' + vidId)
	for addrs in temp:
		print addrs	

getList('https://www.youtube.com/playlist?list=PLwgprUN2IFAtT_33QCrsPh6wzqwF88YqW')
