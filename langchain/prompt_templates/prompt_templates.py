from langchain import PromptTemplate

template_text = "Tell me a {adjective} joke about {content}"

prompt_template = PromptTemplate.from_template(template_text)

print("Valid replacing: ", prompt_template.format(adjective="dark", content="Lions"))

# specify input variable(s) explicitly
# invalid_prompt = PromptTemplate(input_variables=["adjective"], template=template_text)


# chat prompt template

from langchain.prompts import ChatPromptTemplate

# use 2-tuple (type,content) format
template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI bot, Your name is {name}"),
        ("human", "hello"),
        ("ai", "Hello! I'm doing well."),
        ("human", "{user_input}"),
    ]
)

messages = template.format_messages(name="Jarvis", user_input="What is your name ?")

print("formatted messages (2-tuple) : ", messages)

# use MessagePromptTemplate

from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessage

template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are a helpful AI assistant that re-writes the user's text to make it sound more upbeat"
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

print(
    "formatted messages - (Message objects) ",
    template.format_messages(text="I do not like working out."),
)
