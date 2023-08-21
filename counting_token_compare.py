import tiktoken


######################################################################
# count tokens for chat completion API calls
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """return number of tokens used by a list of messages"""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Error : Model not found , using cl100k_base encoding")
        encoding = tiktoken.get_encoding("cl100k_base")

    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-3.5-turbo":
        # print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        # return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}.
              See https://github.com/openai/openai-python/blob/main/chatml.md for 
              information on how messages are converted to tokens."""
        )

    """
    {
        "role": "system",
        "content": "text",

    },
    {
        "role" : "user",
        "content" : "Summarize the text"
    }
    """
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        print(f"""message is : {message}""")
        for key, value in message.items():
            curr_len = len(encoding.encode(value))
            print(f"""num_tokens from current value is : {curr_len}""")
            num_tokens += curr_len
            if key == "name":
                num_tokens += tokens_per_name

    num_tokens += 3  # last reply ,  3 token for "assistant"

    return num_tokens


example_messages = [
    {
        "role": "system",
        "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English.",
    },
    {
        "role": "system",
        "content": "New synergies will help drive top-line growth.",
    },
    {
        "role": "system",
        "content": "Things working well together will increase revenue.",
    },
    {
        "role": "system",
        "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage.",
    },
    {
        "role": "system",
        "content": "Let's talk later when we're less busy about how to do better.",
    },
    {
        "role": "user",
        "content": "This late pivot means we don't have time to boil the ocean for the client deliverable.",
    },
]

import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
for model in [
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo",
]:
    print(model)
    # example token count from the function defined above
    print(
        f"""{num_tokens_from_messages(example_messages, model)} prompt tokens counted by num_tokens_from_messages()."""
    )
    # example token count from the OpenAI API
    response = openai.ChatCompletion.create(
        model=model,
        messages=example_messages,
        temperature=0,
        max_tokens=1,  # setting max tokens for output/completion
    )
    # print("response json is : ",response)
    print(
        f'{response["usage"]["prompt_tokens"]} prompt tokens counted by the OpenAI API.'
    )
    print()


"""
each message is an object, which uses either 3/4 tokens based on model
each object in a message , only value is encoded

encoding of response is not stable to count tokens
"""
