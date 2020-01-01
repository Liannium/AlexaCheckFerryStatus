from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler

import requests
import json
import re
from vesselfunctions import getbiseattleferries


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = "I can check the status of the ferry."

        handler_input.response_builder.speak(response).set_card(
            SimpleCard("Check Ferry", response)).set_should_end_session(False)
        return handler_input.response_builder.response


class SEABIIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CheckFerryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = ""
        terminalurl = "https://www.wsdot.wa.gov/ferries/vesselwatch/Terminals.ashx"
        vesselurl = "https://www.wsdot.com/ferries/vesselwatch/Vessels.ashx"

        vesselresp = requests.get(vesselurl)
        terminalresp = requests.get(terminalurl)

        if vesselresp.status_code == 200 and terminalresp.status_code == 200:
            vessels = json.loads(vesselresp.text)
            vessellist = vessels["vessellist"]

            regex = r'new Date\(\d*\)'
            terminalstring = re.sub(regex, "null", terminalresp.text, flags=re.MULTILINE)
            terminals = json.loads(terminalstring)
            terminallist = terminals["FeedContentList"]

            response = getbiseattleferries(vessellist, terminallist)
        else:
            response = "The page could not be successfully accessed"

        handler_input.response_builder.speak(response).set_card(
            SimpleCard("Check Ferry", response)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = "I can check the status of the ferry"

        handler_input.response_builder.speak(response).ask(response).set_card(
            SimpleCard("Check Ferry", response))
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or \
               is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = "Goodbye!"

        handler_input.response_builder.speak(response).set_card(
            SimpleCard("Hello World", response)).set_should_end_session(True)
        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, I didn't get that"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SEABIIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()
