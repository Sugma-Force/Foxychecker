#!/bin/python3
import string
import argparse
import requests

parser=argparse.ArgumentParser()
parser.add_argument('-p', '--proxylist', type=str, help='Proxy list', required=True)
parser.add_argument('-o', '--outfile', type=str, help='Output file', required=True)
args=parser.parse_args()
proxylist=args.proxylist
outfile=args.outfile
URL='https://icanhazip.com'
to=3

ASCII='''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⠀⢀⡴⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠀⠀⢠⠎⠀⠀⠀⠀⠀⣠⢧⠀⠀⠀⠀⠀⣇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⢠⠇⠀⠀⠀⠀⠀⡴⠁⠈⡄⠀⠀⠀⠀⢸⡀
⠀⠀⠀⠀⠀⠀⢰⠃⠀⠀⠀⠀⠀⡼⠀⠀⣸⠀⠀⠀⠀⢀⠞⠀⠀⠀⣿⠀⠀⠀⠀⠀⡇
⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⡰⠁⠀⠀⠋⠀⠀⠀⠀⢊⠀⠀⠀⠀⡿⠀⠀⠀⠀⠀⡿
⠀⠀⠀⠀⠀⡎⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠘⡆⠀⠀⠀⡇⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⡸⠀⠀⠀⠀⠀⡰⠋⠉⠙⠛⠛⠿⣿⣶⣶⣶⣶⡼⣄⠀⢠⡇⠀⠀⠀⠀⣸⠀
⠀⠀⠀⢠⠃⠀⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⡇⠈⢦⠘⡇⠀⠀⠀⢀⠇⠀
⠀⠀⠀⡎⠀⠀⠀⠀⡸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⡿⠀⠀⠀⢳⡇⠀⠀⠀⡸⠀⠀
⠀⠀⡸⠀⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠁⠀⠀⠀⠀⢡⠀⠀⢠⠃⠀⠀
⠀⢰⠃⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⢇⠀⡼⠀⠀⠀
⢠⠃⠀⠀⠀⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀⠀⠀⠀⠀⢸⠀⡇⠀⠀⠀
⢻⠀⠀⠀⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⢈⣀⠇⠀⠀⠀
⠈⣆⠀⠀⠀⠘⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠀⠀⠀⠀⠀⠀⠀⢸⢻⠀⠀⠀⠀
⠀⢸⢦⠀⠀⠀⠈⠢⣀⡀⠀⠀⠀⠀⠀⠀⠀⢀⣔⠁⠀⠀⠀⠀⠀⠀⠀⡜⣸⠀⠀⠀⠀
⠀⣸⡼⠳⡀⠀⣀⡒⠤⣌⣑⣦⣀⠀⡠⢴⠒⠁⠈⠑⠤⣀⡀⠀⠀⢀⡜⡡⣿⠀⠀⠀⠀
⠀⠙⠃⠀⠱⡈⠳⡬⢉⣉⡒⣾⣟⠃⠀⣸⠀⠀⠀⠀⠀⠀⠉⠀⣠⠿⣊⡼⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠢⣈⣦⠀⠀⠀⠁⠀⢀⠇⠀⠀⠀⠀⠀⠀⠀⠶⣿⣯⠟⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠛⠃⠀⠀⠀⢠⠎⠀⠀⠀⠀⠀⠀⠀⠀⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀
Foxychecker - Brought to you by Xxxosmo
Check your shit properly
'''

def check_proxy(proxy):
	try:
		session=requests.Session()
		session.headers['User-Agent']='Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'
		session.max_redirects=3
		proxy=proxy.split('\n',1)[0]
		request=session.get(URL, proxies={"http": proxy, "https": proxy}, timeout=to, allow_redirects=True)
		proxyip=(request.text).strip()
		onlyip="".join(i for i in proxy if i in (string.digits +".:")).strip(":").split(":")[0]
		if proxyip==onlyip:
			return proxy
		else:
			return
	except Exception as e:
		pass
	return

def process():
	proxyfile=open(proxylist)
	good=0
	bad=0
	checked=0
	for proxy in proxyfile:
		try:
			if check_proxy(proxy):
				good+=1
				validfile=open(outfile, 'a')
				validfile.write(proxy)
				validfile.close()
			else:
				bad+=1
			checked+=1
		except Exception as e:
			pass
		print('||', 'Good proxies:', good, '||', 'Bad proxies:', bad, '||', 'Checked proxies:', checked, '||', '\r', end='', flush=True)
	return

print(ASCII)
print('Checking proxies...')
process()
