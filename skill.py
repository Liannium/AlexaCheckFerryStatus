from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler

from vesselfunctions import checkferries, getseattleferries, loadterminallist, loadvessellist


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("in launch request handler")
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("in launch request handler")
        response = "I can check the status of the ferry. Just say Alexa, tell ferry status to check the status of the "\
            "blank ferry"

        handler_input.response_builder.speak(response).set_card(
            SimpleCard("Check Ferry", response)).set_should_end_session(False)
        return handler_input.response_builder.response


class CheckFerryIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("in check ferry")
        return is_intent_name("CheckFerryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = ""
        vessellist = loadvessellist()
        terminallist = loadterminallist()

        if vessellist is not None and terminallist is not None:
            response = getseattleferries(vessellist, terminallist, "SEA-BI", "Bainbridge")
        else:
            response = "The page could not be successfully accessed"

        handler_input.response_builder.speak(response).set_card(
            SimpleCard("Check Ferry", response)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class CheckEdKingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("in check ED-KING")
        return is_intent_name("CheckEdKingIntent")(handler_input)

    def handle(self, handler_input):
        response = ""
        vessellist = loadvessellist()
        terminallist = loadterminallist()

        if vessellist is not None and terminallist is not None:
            response = checkferries(vessellist, terminallist, "ED-KING", "Edmonds", "Kingston")
        else:
            response = "The page could not be successfully accessed"

        handler_input.response_builder.speak(response).set_card(
            SimpleCard("Check Edmonds Kingston", response)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class CheckMukClIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("in check MUK-CL")
        return is_intent_name("CheckMukClIntent")(handler_input)

    def handle(self, handler_input):
        response = ""
        vessellist = loadvessellist()
        terminallist = loadterminallist()

        if vessellist is not None and terminallist is not None:
            response = checkferries(vessellist, terminallist, "MUK-CL", "Mukilteo", "Clinton")
        else:
            response = "The page could not be successfully accessed"

        handler_input.response_builder.speak(response).set_card(
            SimpleCard("Check Mukilteo Clinton", response)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class CheckSeaBrIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("CheckSeaBrIntent")

    def handle(self, handler_input):
        vessellist = loadvessellist()
        terminallist = loadterminallist()

        if vessellist is not None and terminallist is not None:
            response = getseattleferries(vessellist, terminallist, "SEA-BR", "Bremerton")
        else:
            response = "The page could not be successfully accessed"

        handler_input.response_builder.speak(response).set_card(
            SimpleCard("Check Seattle Bremerton", response)).set_should_end_session(True)
        return handler_input.response_builder.response


class CheckSeattleIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("in check seattle")
        return is_intent_name("CheckSeattleIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("in check seattle")
        response = "I'm not sure which seattle ferry you mean. Next time, please specify either the Bainbridge or " \
            "Bremerton ferry"

        handler_input.response_builder.speak(response).set_card(
            SimpleCard("Check Seattle", response)).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("in session ended")
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("in session ended")
        # any cleanup logic goes here

        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("in help")
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("in help")
        response = "I can check the status of the ferry.Just say Alexa, check the status of the blank ferry"

        handler_input.response_builder.speak(response).ask(response).set_card(
            SimpleCard("Check Ferry", response))
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("in cancel")
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or \
               is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("in cancel")
        response = "Goodbye!"

        handler_input.response_builder.speak(response).set_card(
            SimpleCard("Hello World", response)).set_should_end_session(True)
        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        print("exception")
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
sb.add_request_handler(CheckFerryIntentHandler())
sb.add_request_handler(CheckEdKingIntentHandler())
sb.add_request_handler(CheckMukClIntentHandler())
sb.add_request_handler(CheckSeaBrIntentHandler())
sb.add_request_handler(CheckSeattleIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()
