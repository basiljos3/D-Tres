
from botbuilder.dialogs import (
    WaterfallStepContext,
    WaterfallDialog,
    ComponentDialog,
    DialogTurnResult
)
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt, ChoicePrompt
from botbuilder.dialogs.choices import Choice, FoundChoice
from botbuilder.core import MessageFactory, CardFactory
from botbuilder.schema import HeroCard, ActionTypes, CardAction

from dialogs.search import Search
from dialogs.tasks import Tasks
from dialogs.alerts import Alerts
from data_models import UserProfile

class Menu(ComponentDialog):
    def __init__(self, dialog_id: str = None ):
        super(Menu, self).__init__(dialog_id or Menu.__name__)
        self.add_dialog(TextPrompt("text_prompt"))
        self.USER_INFO = "value-userInfo"
        self.add_dialog(NumberPrompt("number_prompt"))
        self.add_dialog(ChoicePrompt("cardPrompt"))
        self.add_dialog(Search(Search.__name__))
        self.add_dialog(Tasks(Tasks.__name__))
        self.add_dialog(Alerts(Alerts.__name__))
        self.add_dialog(WaterfallDialog("menu_dialog",[self.options, self.menu_val, self.continue_val, self.final_val]))
        self.initial_dialog_id = "menu_dialog"

    async def options(self, waterfall_step: WaterfallStepContext):
        reply = MessageFactory.list([])
        reply.attachments.append(self.create_hero_card())
        return await waterfall_step.prompt("text_prompt", PromptOptions(prompt=reply))


    async def  menu_val(self, waterfall_step:WaterfallStepContext):
        found_choice = waterfall_step.result.lower()
        if found_choice == 'projects':
            return await waterfall_step.begin_dialog(Search.__name__)
        elif found_choice =='technologies':
            return await waterfall_step.begin_dialog(Tasks.__name__)
        elif found_choice == 'pricing':
            await waterfall_step.context.send_activity(MessageFactory.text(""))
            return await waterfall_step.begin_dialog(Alerts.__name__)
        else:
            await waterfall_step.context.send_activity(MessageFactory.text("Enter a valid option."))
            return await waterfall_step.begin_dialog(Menu.__name__)

    async def continue_val(self, waterfall_step:WaterfallStepContext):
        # waterfall_step.values[self.USER_INFO] = waterfall_step.result
        reply = MessageFactory.list([])
        reply.attachments.append(self.continue_hero_card())
        return await waterfall_step.prompt("text_prompt", PromptOptions(prompt=reply))

    async def final_val(self, waterfall_step:WaterfallStepContext):
        found_choice = waterfall_step.result.lower()
        # user_profile : UserProfile = waterfall_step.values[self.USER_INFO]
        # await waterfall_step.context.send_activity(MessageFactory.text("Inside the Final Validation in the menu"))
        # await waterfall_step.context.send_activity(MessageFactory.text(user_profile.stud_details))
        if found_choice == 'yes':
            return await waterfall_step.begin_dialog(Menu.__name__)
        elif found_choice == 'no':
            return await waterfall_step.end_dialog()

    
    def create_hero_card(self):
        card = HeroCard(
            text="Choose one option.",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="Projects", value="Projects"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Technologies", value="Technologies"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Pricing", value="Pricing"
                )
            ]
        )
        return CardFactory.hero_card(card)


    def continue_hero_card(self):
        card = HeroCard(
            text="Do you want to continue ?",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="Yes", value="Yes"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="No", value="No"
                )
            ]
        )
        return CardFactory.hero_card(card)