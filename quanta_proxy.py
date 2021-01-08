#
#	Author: Pulsar
#	YouTube: https://www.youtube.com/channel/UCVo0vjlE50dn2LFynrGe9yA
# 	GitHub: https://www.github.com/Woodnet
# 	Twitter: https://twitter.com/7Pulsar
#	Logdatei: log.html (could be changed)
#	Python-Version: Python 3.8.2
#	Recommended OS: Windows 10
#	--> Please write a comment on GitHub-issues.
#
import socket,os,time,sys
from datetime import datetime
from threading import Thread
from threading import *
from _thread import *
from colorama import Fore,init,Style

#colors
init()
h = Style.BRIGHT
w = h + Fore.WHITE
r = h + Fore.RED
g = h + Fore.GREEN
c = h + Fore.CYAN
#

def uhrzeit():
	t = datetime.now()
	uhrzeit = "%s:%s:%s"%(t.hour,t.minute,t.second)
	return uhrzeit

def p(nachricht):
	print(w+"INFO: %s"%(nachricht))

def s():
	print(g+"INFO: Abgeschlossen")

def f(__fehlermeldung):
	#print(r+"FEHLER: %s"%(__fehlermeldung))
	log("__FEHLER__: %s"%(__fehlermeldung))

class quanta_proxy:
	def __init__(self,proxy_adresse,proxy):
		self.proxy_adresse = proxy_adresse
		self.proxy = proxy

	def starten(self):
		maximale_verbindungen = library['proxy']['maximale_verbindungen']
		proxy.bind(self.proxy_adresse)
		proxy.listen(maximale_verbindungen)

def handle_client(client_socket,client_adresse,__packet):
	#p("Daten werden aus Packet entnommen..")
	try:
		data = __packet.decode()
		decoded = True
	except Exception:
		data = __packet
		decoded = False
	try:
		first_line = data.split("\n")[0]
		url = first_line.split(" ")[1]

		http_pos = url.find("://")
		if (http_pos == -1):
			temp = url
		else:
			temp = url[(http_pos + 3):]

		port_pos = temp.find(":")

		webserver_pos = temp.find("/")
		if (webserver_pos == -1):
			webserver_pos = len(temp)
		webserver = ""
		port = -1

		if (port_pos == -1 or webserver_pos < port_pos):
			port = 80
			webserver = temp[:webserver_pos]
		else:
			port = int(temp[(port_pos + 1):][:webserver_pos - port_pos -1])
			webserver = temp[:port_pos]
		#s()
		if (decoded == True):
			data = data.encode()
		__proxy_server__(webserver,port,client_socket,data,client_adresse)
	except Exception as e:
		f(e)

def __proxy_server__(webserver,port,client_socket,data,client_adresse):
	try:
		#p("Eine Verbindung wird zum Client hergestellt..")
		__s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP
		__s.connect((webserver,port))
		#s()
		#p("Daten werden zum Client geschickt..")
		__s.send(data)
		#s()
		while True:
			#p("Warte auf Packet vom Client..")
			__antwort_client = __s.recv(library['proxy']['buffer_size'])
			#s()
			if (len(__antwort_client) > 0):
				#p("Packet wird zum Client geschickt..")
				client_socket.send(__antwort_client)
				#s()
				dar = float(len(__antwort_client))
				dar = float(dar / 1024)
				dar = "{}.3s".format(dar)
				print(w+"INFO: Erfolgreiche Anfrage {} => {} <= {}".format(client_adresse[0],dar,webserver))
				log("<<<[#]>>> Erfolgreiche Anfrage => {} => {} <= {}".format(client_adresse[0],dar,webserver))
			else:
				break
		__s.close()
		#proxy.close()
	except socket.error as e:
		__s.close()
		#proxy.close()
		f(e)

def log(LOG):
	__log_dateiname = library['logs']['dateiname']
	datei = open(__log_dateiname,"a")
	datei.write("<p class='text_wh'>%s</p>\n"%(LOG))
	datei.close()

library = {
	'proxy':{
		'IP':"",
		'PORT':"",
		'maximale_verbindungen':10,
		'buffer_size':10000,
	},
	'logs':{
		'dateiname':"log.html",
	},
}

__unavailable_ports = ["80","8080","443"]

def get_addr():
	while True:
		__ip = input("Proxy-IP = ") #Your IP
		__port = input("Proxy-Port = ") #Your PORT
		if (__port not in __unavailable_ports):
			if (__port == "" or __port == " "):
				__port = 4415
			break

		else:
			print("Please use an available Port! Example: 5555")

os.system("cls") #Windows -default
if __name__ == '__main__':
	(IP,PORT) = get_addr()
	buff_size = library['proxy']['buffer_size']
	library['proxy']['PORT'] = int(__port)
	proxy_adresse = (library['proxy']['IP'],library['proxy']['PORT'])
	proxy = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP
	__proxy = quanta_proxy(proxy_adresse,proxy)
	p("Starte Proxy..")
	try:
		__proxy.starten()
		s()
	except Exception as e:
		f(e)
	p("Proxy ist nun erreichbar: %s:%s"%(library['proxy']['IP'],library['proxy']['PORT']))
	while True:
		try:
			(client_socket,client_adresse) = proxy.accept()
			__packet = client_socket.recv(buff_size)
			start_new_thread(handle_client, (client_socket,client_adresse,__packet))
		except KeyboardInterrupt:
			p("Proxy wurde durch CTRL+C beendet")
			break
	proxy.close()
	n = input("Proxy wurde geschlossen>>> ")
	sys.exit()
