from botbuilder.core import TurnContext, ActivityHandler, ConversationState, MessageFactory, CardFactory, UserState
from botbuilder.dialogs import DialogSet,WaterfallDialog, WaterfallStepContext, ComponentDialog, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt,NumberPrompt,PromptOptions, ChoicePrompt
from botbuilder.schema import HeroCard, CardAction, ActionTypes
from botbuilder.dialogs.choices import Choice

from dialogs.menu import Menu
from data_models import UserProfile

class BotDialog(ConversationState):
    def __init__(self, conversationstate: ConversationState):
        super(BotDialog, self).__init__(BotDialog.__name__)
        self.con_statea = conversationstate
        self.state_prop = self.con_statea.create_property("dialog_set")
        self.dialog_set = DialogSet(self.state_prop)
        self.dialog_set.add(TextPrompt("text_prompt"))
        self.dialog_set.add(NumberPrompt("number_prompt"))
        self.dialog_set.add(ChoicePrompt("cardPrompt"))
        self.dialog_set.add(Menu(Menu.__name__))
        self.dialog_set.add(WaterfallDialog("main_dialog",[self.StartMessage, self.FinalMessage]))

    async def StartMessage(self,waterfall_step:WaterfallStepContext) -> DialogTurnResult:
        await waterfall_step.context.send_activity(MessageFactory.text("Welcome Basil, How can I help you."))
        return await waterfall_step.begin_dialog(Menu.__name__)

    
    async def FinalMessage(self, waterfall_step:WaterfallStepContext) -> DialogTurnResult:
        # user_profile : UserProfile() = waterfall_step.result
        # await waterfall_step.context.send_activity(MessageFactory.text(f"Inside the botDialog final Message = {user_profile.stud_details}"))
        await waterfall_step.context.send_activity(MessageFactory.text("Thank you!"))
        return await waterfall_step.end_dialog()



    async def on_turn(self,turn_context:TurnContext):
        dialog_context = await self.dialog_set.create_context(turn_context)

        if(dialog_context.active_dialog is not None):
            await dialog_context.continue_dialog()
        else:
            await dialog_context.begin_dialog("main_dialog")

        await self.con_statea.save_changes(turn_context)
    