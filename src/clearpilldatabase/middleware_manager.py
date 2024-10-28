from clearpilldatabase.middlewares import cloudflare


class MiddlewareManager:
	BACKENDS = [cloudflare.CloudflareMiddleware]

	@staticmethod
	def detect(response):
		for backend in MiddlewareManager.BACKENDS:
			if backend.detect(response):
				return backend
		return False

class MiddlewareHandlingException(Exception):
	pass