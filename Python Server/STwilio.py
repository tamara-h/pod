from twilio.rest            import TwilioRestClient

class TwilioMessages():
    prefix          = ""
    suffix          = "xoxo, Pod"
    flood           = "Warning! Water levels are running high in your area. Suggestion: flee! Every Pod for themselves \o/"
    rain            = "Attention! It is raining. Suggestion: take washing inside."
    tempHighWarn    = "Caution! Your house is at, or close to, the maximum temperature. Suggestion: turn it down."
    tempLowWarn     = "Caution! Your house is at, or close to, the minimum temperature. Suggestion: turn it up."
    doorLeftOpen    = "Bad news, your front door has been left unlocked. Suggestion: lock it."
    extremeHeat     = "Your house is above 3,000*C. Looks like you annoyed the Russians. Pod has not yet been upgraded to allow it to accurately give advice for nuclear wars, but we'll be sure to inform you when it can!"
    
    messageTemplate = "{}{} {}"
    

class TwilioClient():
    enabled = True
    template = "{} xoxo, Pod"
    
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

if __name__ == "__main__":
    TwilioClient.sendMessage("Hi, this is Pod telling you that the Twilio script has been launched in debug mode and is sending every text. They should be in this order: Flood, rain, maximum temperature, minimum temperature, unlocked doors and finally nuclear strike warning.")
    TwilioClient.sendMessage(TwilioMessages.flood)
    TwilioClient.sendMessage(TwilioMessages.rain)
    TwilioClient.sendMessage(TwilioMessages.tempHighWarn)
    TwilioClient.sendMessage(TwilioMessages.tempLowWarn)
    TwilioClient.sendMessage(TwilioMessages.doorLeftOpen)
    TwilioClient.sendMessage(TwilioMessages.extremeHeat)
