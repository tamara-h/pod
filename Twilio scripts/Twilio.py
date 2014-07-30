from twilio.rest import TwilioRestClient

def doorOpen(): 
	ACCOUNT_SID = "AC42e4c31d0bb66d30387c967b1b8ebc61" 
	AUTH_TOKEN = "0de403b3b1383b04811db2ad769a646d" 
	 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	client.messages.create(
		to="447476915987", 
		from_="+441631402052", 
		body="Bad news, your front door has been left unlocked. Suggestion: lock it. xoxo, Pod",  
	)


def temp(): 
	ACCOUNT_SID = "AC42e4c31d0bb66d30387c967b1b8ebc61" 
	AUTH_TOKEN = "0de403b3b1383b04811db2ad769a646d" 
	 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	 
	client.messages.create(
		to="+447476915987", 
		from_="+441631402052", 
		body="Caution! Your house is reaching either the max/min temperature. Suggestion: either turn it up, or turn it down. xoxo, Pod",  
	)
	
def flood():
	ACCOUNT_SID = "AC42e4c31d0bb66d30387c967b1b8ebc61" 
	AUTH_TOKEN = "0de403b3b1383b04811db2ad769a646d" 
	 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	 
	client.messages.create(
		to="+447476915987", 
		from_="+441631402052", 
		body="Warning! Water levels are running high in your area. Suggestion: flee! Every Pod for themselves \o/",  
	)	


def rain():
	ACCOUNT_SID = "AC42e4c31d0bb66d30387c967b1b8ebc61" 
	AUTH_TOKEN = "0de403b3b1383b04811db2ad769a646d" 
	 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	 
	client.messages.create(
		to="447476915987", 
		from_="+441631402052", 
		body="Attention! It is raining. Suggestion: take washing inside. xoxo, Pod",  
	)
