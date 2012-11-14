e24cloud-api
============

WARNING: This is not the official API! Use at your own risk! (Written for educational purposes :D ONLY :])
Simple bot that can create/get info/delete VMs on e24cloud.com service. 

Why did I do this?
--------------------

Well.. It looks like they don't want to make their own API. Every time I asked when, they replied that they were "working on it". Their Roadmap says that the first version of API was supposed to be released until March (2012). I have no more time to send them e-mails with questions.
That's why I made this simple class...

Example
--------------------

```python
def main():
	from cloud import CloudApi

	cloudApi = CloudApi()
	cloudApi.login('LOGIN (EMAIL)', 'USER PASSWORD')

	# create VM (minmal plan, 0 additional HDD, Debian 64)
	cloudApi.create(0, 0, 2, 'Test VM')

	# get server list
	servers = cloudApi.get_servers()

	for server in servers:
		# server[0] is machine_id

		# delete server
		cloudApi.delete(server[0])

		# check if machine is online
		if server[9] == 'online':
			det = cloudApi.get_details(server[0])			

			# get its ip and root password
			print det['ip_address'], det['root_password']
```