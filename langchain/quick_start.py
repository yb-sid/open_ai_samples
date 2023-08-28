from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(openai_api_key=openai_key)  # default model is davinci-003 outdated


chat_model = ChatOpenAI(openai_api_key=openai_key)

# print(f"""llm call : {llm.predict("Hi !")}""")

# print(f"""Chat_model call : {chat_model.predict("Hello")}""")


question_text = "What would be a good name for a company that makes colorful socks?"

# print(
#     f"""llm answer for questions : {question_text} is : \n  {llm.predict(question_text)}"""
# )

# print(
#     f"""chat_model answer for questions : {question_text} is : \n  {chat_model.predict(question_text)}"""
# )


from langchain.schema import HumanMessage

messages = [HumanMessage(content=question_text)]

# output is a ChatMessage
# print(f"""llm answer for questions is :\n {llm.predict_messages(messages)}""")

# print(
#     f"""chat_model answer for questions is : {chat_model.predict_messages(messages)}"""
# )


# prompt templating

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

template = (
    "You are a helpful assistant that translates {input_language} to {output_language}."
)

system_message_prompt = SystemMessagePromptTemplate.from_template(template)

human_template = "{text}"

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

formatted_messages = chat_prompt.format_messages(
    input_language="English", output_language="Hindi", text="Clap you hands"
)

print("formatted messages from template is : ", formatted_messages)
###############
# LLM-CHAIN


from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser


class CommaSeparatedListParser(BaseOutputParser):
    """Parse output of LLM call to comma separated list"""

    def parse(self, text: str):
        print("text is : ", text)
        return text.strip().split(", ")


template = """You are a helpful assistant who generates comma separated lists.
A user will pass in a category, and you should generate 5 objects in that category
in a comma separated list.ONLY return a comma separated list, and nothing more."""

system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

chain = LLMChain(
    llm=chat_model, prompt=chat_prompt, output_parser=CommaSeparatedListParser()
)

print("Chain for 'Colors' : ", chain.run("colors"))
