import codecs, json 
import requests
import sys
import functools
import logging
import os
import argparse

log = logging.getLogger('ep')
parser = argparse.ArgumentParser(description='Generate FVTT json data for the ep2 system.')
parser.add_argument('src')
parser.add_argument('dst')
args = parser.parse_args()

sys.stdout.reconfigure(encoding='utf-8') #type: ignore
img_root_url = 'https://arokha.com/eclipsehelper/images/morphs'

pretty = functools.partial(json.dumps, sort_keys=True, indent=2)
compact = functools.partial(json.dumps, separators=(',', ':'))
bopen = open
open = functools.partial(codecs.open, encoding='utf8')

def getData(fname: str) -> list:
	data = None
	with open(fname, 'r') as src:
		data = json.loads(src.read())
	return data

# return the image location
# fetch the url from the web if needed and serialize it on disk
def getImage(what: str, serialize_in: str) -> str:
	target = ''
	url = img_root_url + f'/{what}'	
	target = serialize_in + '/'+ what
	if not os.path.exists(target):
		# get it from the url
		rsp = requests.get(url)
		if 'image' in rsp.headers['Content-Type']:
			with bopen(target, 'wb') as dst:
				for chunk in rsp:
					dst.write(chunk)
	return 'systems/ep2/' + target if target else target

def convert_morphs(data: list) -> list:
	converted = []
	for m in data: # morphs
		img = getImage(m.pop('image') or 'none.png', 'icons/items/morphs')
		cm = {'name': m.pop('name'), 'type': 'morph', 'data': m, 'img': img}
		# remove undesirable fields from EP2 data
		m.pop('id')
		# change movement_rate structure
		mr = m.pop('movement_rate')
		m['movement_rate'] = {mov.pop('movement_type').lower(): mov for mov in mr}
		converted.append(cm)
	return converted

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	with open(args.dst, 'w') as dst:
		dst.write(pretty(convert_morphs(getData(args.src))))
	
