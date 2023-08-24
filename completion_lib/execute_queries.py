from test_data import (
    test_query_gen_messages,
    test_schema,
    FUNCTION_ARRAY,
    test_correction_messages,
    test_basic_messages,
)
from completion_util import call_completion_wrapper
import json

"""
Test out query generation
"""


def test_gen_query():
    try:
        assistant_response = call_completion_wrapper(
            messages=test_query_gen_messages,
            model="gpt-3.5-turbo",
            functions=FUNCTION_ARRAY,
            max_tokens=600,
            db_schema=test_schema,
            is_question=True,
            is_correction=False,
        )

        if assistant_response["function_call"]:  # response is a object extending dict
            print(
                f"""Function query generated : {json.loads(assistant_response.function_call.arguments)["query"]}"""
            )

    except Exception as exception:
        print("Exception caught while calling completion API , ", exception)


"""
Test Query correction sample
"""


def test_correction_query():
    try:
        assistant_response = call_completion_wrapper(
            messages=test_correction_messages,
            model="gpt-3.5-turbo",
            functions=FUNCTION_ARRAY,
            max_tokens=600,
            db_schema=test_schema,
            is_question=False,
            is_correction=True,
        )

        if (
            assistant_response.function_call
            and assistant_response.function_call.arguments
        ):
            response_json = json.loads(assistant_response.function_call.arguments)
            print(
                f"""Corrected query is : {response_json["query"]} from  error : {response_json["error_message"]}"""
            )

    except Exception as ex:
        print("Exception caught in calling Completion API : ", ex)


def test_basic_chat_completions():
    try:
        response = call_completion_wrapper(
            messages=test_basic_messages, max_tokens=100, model="gpt-3.5-turbo"
        )
        print(f"Chat completion response for basic call is : {response}")
    except Exception as ex:
        print("Exception caught in calling Completion API : ", ex)


# test_gen_query()
# test_correction_query()
test_basic_chat_completions()
