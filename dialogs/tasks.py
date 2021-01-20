from botbuilder.dialogs import (
    WaterfallStepContext,
    WaterfallDialog,
    ComponentDialog,
    DialogTurnResult
)
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt, ChoicePrompt, PromptValidatorContext
from botbuilder.dialogs.choices import Choice, FoundChoice
from botbuilder.core import MessageFactory, CardFactory
from botbuilder.schema import HeroCard, ActionTypes, CardAction


class Tasks(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(Tasks, self).__init__(dialog_id or Tasks.__name__)
        self.add_dialog(TextPrompt("text_prompt"))
        self.add_dialog(NumberPrompt("number_prompt",self.IsValidPhoneNumber))
        self.add_dialog(ChoicePrompt("cardPrompt"))
        self.add_dialog(WaterfallDialog("tasks_dialog",[self.details,self.details_phone,self.details_email,self.options, self.menu_val]))
        self.initial_dialog_id = "tasks_dialog"

    async def IsValidPhoneNumber(self, prompt_valid:PromptValidatorContext):
        if (prompt_valid.recognized.succeeded is False):
            await prompt_valid.context.send_activity("Hey please enter a  Valid Phone Number")
            return False
        else:
            value = str(prompt_valid.recognized.value)
            if len(value) != 10:
                await prompt_valid.context.send_activity("Hey please enter a  Valid Phone Number")
                return False
        return True

    async def details(self, waterfall_step: WaterfallStepContext):
        reply = MessageFactory.text("Enter your name")
        return await waterfall_step.prompt("text_prompt", PromptOptions(prompt=reply))
    
    async def details_phone(self, waterfall_step: WaterfallStepContext):
        reply = MessageFactory.text("Enter your phone number")
        return await waterfall_step.prompt("number_prompt", PromptOptions(prompt=reply))
    
    async def details_email(self, waterfall_step: WaterfallStepContext):
        reply = MessageFactory.text("Enter your email")
        return await waterfall_step.prompt("text_prompt", PromptOptions(prompt=reply))

    async def options(self, waterfall_step:WaterfallStepContext):
        reply = MessageFactory.list([])
        reply.attachments.append(self.function_task_hero_card())
        return await waterfall_step.prompt("text_prompt", PromptOptions(prompt=reply))

    async def menu_val(self, waterfall_step:WaterfallStepContext):
        found_choice = waterfall_step.result.lower()
        if found_choice == 'python':
            await waterfall_step.context.send_activity(MessageFactory.text("python"))
            return await waterfall_step.end_dialog()
        elif found_choice == 'java':
            await waterfall_step.context.send_activity(MessageFactory.text("java"))
            return await waterfall_step.end_dialog()
        else:
            await waterfall_step.context.send_activity(MessageFactory.text("Enter a valid option."))
            return await waterfall_step.begin_dialog(Tasks.__name__)

    def function_task_hero_card(self):
        card = HeroCard(
            text="Choose one option.",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="Python", value="Python"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Java", value="Java"
                )
            ]
        )
        return CardFactory.hero_card(card)
