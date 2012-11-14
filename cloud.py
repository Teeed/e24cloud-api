'''

https://github.com/Teeed/e24cloud-api/

'''

import urllib, urllib2, cookielib, json

class CloudApi(object):
	def __init__(self):
		super(CloudApi, self).__init__()
		
		# set-up
		self._jar = cookielib.CookieJar()
		self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._jar))
		self._opener.addheaders = [('X-Requested-With', 'XMLHttpRequest'),
		('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko)'+\
			' Chrome/24.0.1312.5 Safari/537.17'), ('Referer', 'https://www.e24cloud.com/')]

	def _call(self, url, data=None, addformat=True):
		data_encoded = urllib.urlencode(data) if data != None else None

		# ?format=json || format/json ... yes, we love frameworks ;)
		r = self._opener.open('https://www.e24cloud.com/'+url+('?format=json' if addformat else ''), data_encoded)
	
		data = r.read()
		response_headers = r.info()

		if response_headers['Content-Type'] == 'application/json':
			try:
				data = json.loads(data)
			except:
				raise Exception('Failed to parse JSON')

		return data

	def login(self, login, password):
		data = self._call('login/check', {'email': login, 'password': password})

		if data['status'] != 'ok':
			raise Exception('Bad login credentials')

		return True

	def _g_aa_data(self, action, machine_id=None):
		try:
			return self._call('cloud/'+action+\
				('/id/'+machine_id if machine_id != None else ''))['aaData']
		except KeyError: # no aaData :<
			return None
		
	def get_vms_status(self):
		return self._call('cloud/vms-status')

	def get_servers(self):
		return self._g_aa_data('list-servers')

	def get_resources(self):
		return self._g_aa_data('list-resources')

	def get_logs(self, machine_id):
		return self._g_aa_data('list-logs', machine_id)

	def get_status(self, machine_id):
		return self._call('status/'+machine_id)

	def get_details(self, machine_id):
		return self._call('cloud/get-details/id/'+machine_id)
		
	def delete(self, machine_id):
		self._call('cloud/delete/id/'+machine_id+'/format/html', addformat=False)

	def create(self, coreramvalue, quotavalue, os, servername):
		data = self._call('cloud/create', {'coreramvalue': coreramvalue, 'quotavalue': quotavalue, 
			'os': os, 'servername': servername})

		return data