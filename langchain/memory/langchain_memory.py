"""
LangChain: Memory
- LLMs do not remembers previous context of questions 
"""
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI

_ = load_dotenv(find_dotenv())  # load all .env file variable
chat_model = ChatOpenAI(temperature=0.0)


"""
1. Conversation Buffer Memory
use langchain to manage chat history
"""
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

buffer_memory = ConversationBufferMemory()

conversation = ConversationChain(llm=chat_model, memory=buffer_memory, verbose=True)

print(
    conversation.predict(input="Hi , my name is Slim-Shady")
)  # predict returns a string -> AI response
print(conversation.predict(input="How many stars are present in observable universe ?"))
print(conversation.predict(input="What was my name again ?"))


print("memory buffer is : ", buffer_memory.buffer)
print("memory history : ", buffer_memory.load_memory_variables({}))

# explicit addition to memory
buffer_memory = ConversationBufferMemory()
buffer_memory.save_context({"input": "Hi My name is ..."}, {"output": "slim_shady"})

print("Explicit memory is : ", buffer_memory.buffer)
###########
# ConversationBufferMemory - as chat grows , memory can be huge and more tokens will be used
# this is an issue with cost and context limit
###########
