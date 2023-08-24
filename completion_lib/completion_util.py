import openai
from openai.error import OpenAIError
import os
from dotenv import load_dotenv
import backoff
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DEFAULT_MODEL = "gpt-3.5-turbo"

"""
function to update placeholder for schema with user provider schema
"""


def update_function_schema(user_schema: str, functions: list[dict]) -> list[dict]:
    """
    Parameters
    ----------
    user_schema : a string to be used as schema reference for generating SQL
    functions : a list of dicts where list[0] to be updated with schema

    Returns
    -------
    list[dict] : updated list of functions
    """
    updated_description = functions[0]["parameters"]["properties"]["query"][
        "description"
    ].replace("$schema", user_schema)
    functions[0]["parameters"]["properties"]["query"][
        "description"
    ] = updated_description

    return functions


def retry_callback(details):
    print(f"Retry attempt {details['tries']} triggered due to OpenAIError")


@backoff.on_exception(backoff.expo, OpenAIError, max_tries=4, on_backoff=retry_callback)
def call_completion_wrapper(**kwargs):
    """
    Parameters:
    **kwargs : varargs for flexibility to call chat-completion
    ** Note : messages , max_tokens are required.
    """
    message_array = kwargs.get("messages")
    max_tokens = kwargs.get("max_tokens")
    function_array = kwargs.get("functions")
    function_call = kwargs.get("function_call")
    model_name = kwargs.get("model")
    db_schema = kwargs.get("db_schema")
    is_question = kwargs.get("is_question")
    is_correction = kwargs.get("is_correction")

    return call_chat_completion(
        messages=message_array,
        max_tokens=max_tokens,
        is_question=is_question,
        is_correction=is_correction,
        db_schema=db_schema,
        model=model_name,
        functions=function_array,
        function_call=function_call,
    )


def call_chat_completion(
    messages,
    max_tokens,
    is_question=False,
    is_correction=False,
    db_schema="",
    model=DEFAULT_MODEL,
    functions=None,
    function_call=None,
):
    # prepare required arguments
    completion_req_body = {
        "messages": messages,
        "model": model,
        "max_tokens": max_tokens,
    }

    # function with schema -> user first function
    if functions is not None and is_question:
        if db_schema is None:
            raise ValueError("Schema has to be provided if question is to be Asked")
        # TODO : count token of messages+function , if more>limit call vector search
        question_function = update_function_schema(db_schema, [functions[0]])
        completion_req_body.update({"functions": question_function})
    if functions is not None and is_correction:
        correction_function = functions[1]
        completion_req_body.update({"functions": [correction_function]})
    if function_call is not None:
        completion_req_body.update({"function_call": function_call})

    print(f"""Chat-Completion API request is : {completion_req_body}""")

    try:
        start_time = time.time()
        completion_response = openai.ChatCompletion.create(**completion_req_body)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Time taken by ChatCompletion API is : {execution_time:.4f} seconds")
        return completion_response.choices[0].message
    except Exception as error:
        print("OpenAI Error caught after retries : ", error)
        raise error
