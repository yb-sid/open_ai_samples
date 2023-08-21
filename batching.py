"""
there are 2 kinds of limits : 

1. request/min
2. tokens/min

for req/min create one large(er) messages list [{role:text},....]
call api once 
"""

import openai
from openai.error import OpenAIError
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def call_completion(**kwargs):
    response = openai.ChatCompletion.create(**kwargs)
    return response["choices"][0]["message"]["content"]


# List of prompts to be batched
prompts = [
    "Are you an artist ?",
    "Ferrari , is ",
    "Coco is ",
    "next to milky way is ",
]

# Create messages for each prompt
messages = [{"role": "user", "content": prompt} for prompt in prompts]

print(f"initial messages is : {messages}")
# Add the system instruction
system_instruction = {
    "role": "system",
    "content": """Generate a response for all previous user prompts,
    answer each prompt as an independent entity,
    use a python list notation to return result,
    answer of each prompt should not be more than 10 words""",
}
messages.append(system_instruction)

print(f"\nmessages after instruction is : {messages} ")
reply = call_completion(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=500,
)

print(f"\nreply from API is : {reply}")

"""
conclusion , batching with ChatCompletion api not suitable
challenges
1. if batching is used , supplying context is challenge 
2. if max token is reached , response can be incomplete
3. model tries to relate all prompts as much as possible, 
difficult to make prompts independent

https://github.com/openai/openai-cookbook/blob/main/examples/How_to_handle_rate_limits.ipynb
example is with older completion API  
"""
