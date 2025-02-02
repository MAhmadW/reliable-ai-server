from fastapi import FastAPI, Request, Response
from aiclient import AI

ai = AI()
ai.initialize_clients()

app = FastAPI()

@app.post("/ai/message")
async def send_message(request: Request, response: Response):
	try:
		message_body = await request.json()

		ai_response = ai.client.chat.completions.create(
			model= ai.default_model,
			messages= [
				{
					'role': 'user',
					'content': message_body['content']
				}
			]
		)

		response.status_code = 200

		return {'message': ai_response.choices[0].message}

	except Exception as e:
		print(e)
		response.status_code = 500
		return {}

@app.post("/ai/status")
async def parse_status(request: Request, response: Response):
	try:
		notification_body = await request.json()
		if (notification_body.get('incident')):

			# Incident
			print('OpenAI incident webhook triggered')
			
			# If the API is affected
			if ('API' in [component['name'] for component in notification_body['incident']['components']]):

				api_status = [component for component in notification_body['incident']['components'] if component['name'] == 'API'][0]['status']

				if api_status == 'operational':
					# If it is operational
					ai.switch_to_default()

				else:
					# Otherwise, set to fallback
					ai.switch_to_fallback()
					
		elif (notification_body.get('component')):
				# Component update
			print('OpenAI component webhook triggered')

			# If the API is the component
			if (notification_body['component']['name'] == 'API'):
				new_status = notification_body['component_update']['new_status']

				if new_status == 'operational':
					# If it is operational
					ai.switch_to_default()

				else:
					# Otherwise, set to fallback
					ai.switch_to_fallback()

		else:
			print(f'Service status received an unrecognized webhook type:\n{notification_body}')
			response.status_code = 200
			return {}

	except Exception as e:
		print(e)
		response.status_code = 400 # Retry webhook
		return {}
