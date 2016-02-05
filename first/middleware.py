from django.core.urlresolvers import resolve


class AuthorityMiddleware:
	"""
	Middleware for user-object access layer
	"""
	
	def process_request(self, request):
		print('------')
		print('user in middleware: ' + str(request.user))
		print('  post:' + str(request.POST))
		print('  path:' + str(request.path))
		
		result = resolve(request.path)
		print(result)
		
		return None
