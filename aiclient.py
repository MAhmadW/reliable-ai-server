import random
from os import getenv

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = getenv('OPENAI_KEY') 
PERPLEXITY_AI_API_KEY = getenv('PERPLEXITY_KEY') 

class AI():
	def __init__(self):
		self.client = None # Current AI client object
		self.default_model = ''
		self.clients = {} # A dict of clients
		self.client_names = []

		print('Abstract AI client constructed')

	def initialize_clients(self):
		# You can initialize as many clients as you'd like
		self.clients['openai'] = {"client":OpenAI(api_key= OPENAI_API_KEY), "default_model": "gpt-4"}
		self.clients['perplexity'] = {"client":OpenAI(api_key= PERPLEXITY_AI_API_KEY, base_url='https://api.perplexity.ai'), "default_model": "sonar-pro"}

		self.client_names = list(self.clients.keys())

		self.client = self.clients[self.client_names[0]]['client']

		self.default_model = self.clients[self.client_names[0]]['default_model']

		print(f'AI clients initialized: {", ".join(self.client_names)}')

	def switch_to_fallback(self):
		randomized_fallback = random.choice(self.client_names[1:])
		self.client = self.clients[randomized_fallback]['client']
		self.default_model = self.clients[randomized_fallback]['default_model']

		print(f'Switched to fallback client: {randomized_fallback}')
		
	def switch_to_default(self):
		self.client = self.clients[self.client_names[0]]['client']
		self.default_model = self.clients[self.client_names[0]]['default_model']

		print(f'Switched to defult client: {self.client_names[0]}')
