
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, FormValidationAction


class ValidateHealthForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_health_form"


class HealthForm(FormAction):

    def name(self):
        return "health_form"

    @staticmethod
    def required_slots(tracker): #returns the list of slots that needs to be filled before the submit method is invoked

        if tracker.get_slot('confirm_exercise') == True:
            return ["confirm_exercise", "exercise", "sleep", "diet", "stress", "goal"]
        else: #All slots exept excercise slot
            return ["confirm_exercise", "sleep","diet", "stress", "goal"]

    def submit( #Let's us execute whatever we want, once the required forms are filled
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        return []

    #optional - tell rasa how to fill the slots by extracting data from users responses
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "confirm_exercise": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
                self.from_intent(intent="inform", value=True),
            ],
            "sleep": [
                self.from_entity(entity="sleep"),
                self.from_intent(intent="deny", value="None"),
            ],
            "goal": [
                self.from_text(intent="inform"),
            ],
        }

