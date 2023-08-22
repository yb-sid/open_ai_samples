"""
use optional : function parameter in chat completion API 
enable models to generate function arguments based on spec provided

**chat completion API , will not invoke or execute the methods.

request : 
{
    "model" : "gpt-3.5-turbo", required
    "messages": [] ,** required
    "functions" : [{
        "name" : "name of function to be called" # required,
        "description" : "what does the functio do" , # optional but useful 

    }] # list of functions , model may generate JSON parameters for 

}
refer example :
https://platform.openai.com/docs/guides/gpt/function-calling
"""


# imports
import openai
from openai.error import OpenAIError
import os
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

GPT_MODEL = "gpt-3.5-turbo"

functions_spec = [
    {
        "name": "get_current_weather",
        "description": "get current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The name of city or town , e.g : New Delhi",
                },
                "format": {
                    "type": "string",
                    "enum": ["celcius", "fahrenheit"],
                    "description": "Temparature unit to use. Infer based on location",
                },
            },
            "required": ["location", "format"],
        },
    },
    {
        "name": "get_n_day_weather_forecast",
        "description": "Get an N-day weather forecast",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "format": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use. Infer this from the users location.",
                },
                "num_days": {
                    "type": "integer",
                    "description": "The number of days to forecast",
                },
            },
            "required": ["location", "format", "num_days"],
        },
    },
]


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    for message in messages:
        if message["role"] == "system":
            print(
                colored(
                    f"system: {message['content']}\n", role_to_color[message["role"]]
                )
            )
        elif message["role"] == "user":
            print(
                colored(f"user: {message['content']}\n", role_to_color[message["role"]])
            )
        elif message["role"] == "assistant" and message.get("function_call"):
            print(
                colored(
                    f"assistant: {message['function_call']}\n",
                    role_to_color[message["role"]],
                )
            )
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(
                colored(
                    f"assistant: {message['content']}\n", role_to_color[message["role"]]
                )
            )
        elif message["role"] == "function":
            print(
                colored(
                    f"function ({message['name']}): {message['content']}\n",
                    role_to_color[message["role"]],
                )
            )


# call completions
@retry(wait=wait_random_exponential(multiplier=2, max=40), stop=stop_after_attempt(3))
def call_chat_completion(
    message_array, max_tokens, functions=None, function_call=None, model=GPT_MODEL
):
    custom_args = {"model": model, "messages": message_array, "max_tokens": max_tokens}

    if functions is not None:
        custom_args.update({"functions": functions})
    if function_call is not None:
        custom_args.update(
            {"function_call": function_call}
        )  # if functions is present default 'auto'
    # print(custom_args)
    try:
        response = openai.ChatCompletion.create(**custom_args)
        print("token used is : ", response.usage.total_tokens)
        # print("full API response : ", response)
        return response.choices[0].message
    except OpenAIError as e:
        print("OpenAIError caught : ", e._message)


# create functions to be supplied to "functions" parameter to openai API
# To describe a function that accepts no parameters, provide the value {"type": "object", "properties": {}}.


system_message = {
    "role": "system",
    "content": "Don't make assumptions about values to provide to function , ask clarifying quetions",
}

user_message = {"role": "user", "content": "What is the weather like today ?"}
messages = [system_message, user_message]
# call the API with functions
response_message = call_chat_completion(messages, 250, functions=functions_spec)

# check tokens without functions
# call_chat_completion(messages, 250)
messages.append(response_message)
# pretty_print_conversation(messages)

# provide your inputs
input_message = {"role": "user", "content": "I'm in New Delhi"}
messages.append(input_message)
message_response = call_chat_completion(messages, 100, functions=functions_spec)
print(message_response)
print(message_response.get("function_call").get("name"))
messages.append(message_response)
# pretty_print_conversation(messages)

function_args_json = json.loads(
    message_response.function_call.arguments
)  # a dictionary


"""
model can generate function arguments 
by directly using user input or use user input 
to generate argument from previous knowledge
** note : functions use tokens as well , same as prompts 
"""
