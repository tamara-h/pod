from twilio.rest            import TwilioRestClient

class TwilioMessages():
    prefix          = ""
    suffix          = "xoxo Pod"
    flood           = "Warning! Water levels are running high in your area. Suggestion: flee! Every Pod for themselves \o/"
    rain            = "Attention! It is raining. Suggestion: take washing inside."
    tempWarn        = "Caution! Your house is reaching either the max/min temperature. Suggestion: either turn it up, or turn it down."
    doorLeftOpen    = "Bad news, your front door has been left unlocked. Suggestion: lock it."
    
    messageTemplate = "{}{} {}"
    

class TwilioClient():
    enabled = True
    template = "{} xoxo Pod"
    
    def __init__(self):
        self.ACCOUNT_SID = "AC42e4c31d0bb66d30387c967b1b8ebc61"
        self.AUTH_TOKEN  = "0de403b3b1383b04811db2ad769a646d"

        self.client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)
        
    def sendMessage(self, message, phoneNo = "447476915987"):
        if self.enabled:
            print("[INFO] Sent text '{}' to {}".format(TwilioMessages.messageTemplate.format(TwilioMessages.prefix, message, TwilioMessages.suffix), phoneNo))
            self.client.messages.create(
                to      = phoneNo,
                from_   = "441631402052",
                body    = TwilioMessages.messageTemplate.format(TwilioMessages.prefix, message, TwilioMessages.suffix)
                )
        else:
            print("[WARNING] Request sent to Twilio; Twilio has been disabled in the server script")
