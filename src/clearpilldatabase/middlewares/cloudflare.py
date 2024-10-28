# import middleware_manager
from clearpilldatabase import middleware_manager
#__DIR__ = os.path.abspath(os.path.dirname(__file__))

class CloudflareMiddleware:
	@staticmethod
	def detect(response):
		return 'cf-mitigated' in response.all_headers()

	def __init__ (self, page):
		self.page = page

	def handle (self):
		raise middleware_manager.MiddlewareHandlingException
#		time.sleep(5)
#		print('[*] Injecting turnstile init bypass')
#		self.page.on('console', self.extract_challenge)
#		self.page.evaluate(open(__DIR__ + '/cloudflare_inject.js').read())
#		print('[*] Waiting for a bit, it\'s gonna refresh itself in a sec')
		#self.page.reload()
#		print('[*] Waiting for cloudflare to fail')
		#self.page.wait_for_load_state()


	def __str__(self) -> str:
		return 'Cloudflare'