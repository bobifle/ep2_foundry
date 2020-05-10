import codecs, json 
import requests
import sys
import functools
import logging
import os

log = logging.getLogger()

sys.stdout.reconfigure(encoding='utf-8')
root = 'https://raw.github.com/Arokha/EP2-Data/master'

# let img_url = `https://arokha.com/eclipsehelper/images/morphs/${m.name}.png`.toLowerCase().replace(/ /g, "");

pretty = functools.partial(json.dumps, sort_keys=True, indent=2)
compact = functools.partial(json.dumps, separators=(',', ':'))


def toEP2(src):
	return src

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	fname = 'morphs_from_github.json'
	data = None
	if not os.path.exists(fname):
		url = root+'/morphs.json'
		log.info(f'Fetching {fname} from {url}')
		data = json.loads(requests.get(url).text)
		with codecs.open(fname, 'w', 'utf8') as dst:
			dst.write(compact(data))
	else:
		with codecs.open(fname, 'r', 'utf8') as src:
			data = json.loads(src.read())
	
