"""
1. give a python function as input to GPT 
2. Ask GPT to generate unit test plan , maybe elaborate
3. ask GPT to write unit test based on plan    
"""

import openai
import ast  # used for validating python code
from dotenv import load_dotenv
import os
import inspect

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def call_chat_completion_stream(**kwargs):
    response = openai.ChatCompletion.create(**kwargs)
    return response


color_prefix_by_role = {
    "system": "\033[0m",  # gray
    "user": "\033[0m",  # gray
    "assistant": "\033[92m",  # green
}


def print_messages(messages, color_prefix_by_role=color_prefix_by_role) -> None:
    """Prints messages sent to or from GPT."""
    for message in messages:
        role = message["role"]
        color_prefix = color_prefix_by_role[role]
        content = message["content"]
        print(f"{color_prefix}\n[{role}]\n{content}")


def print_message_delta(delta, color_prefix_by_role=color_prefix_by_role) -> None:
    """Prints a chunk of messages streamed back from GPT."""
    if "role" in delta:
        role = delta["role"]
        color_prefix = color_prefix_by_role[role]
        print(f"{color_prefix}\n[{role}]\n", end="")
    elif "content" in delta:
        content = delta["content"]
        print(content, end="")
    else:
        pass


def iterate_and_update_stream(stream_response, print_text):
    stream_text = ""
    for chunk in stream_response:
        delta = chunk.choices[0].delta
        if print_text:
            print_message_delta(delta)
        if "content" in delta:
            stream_text += delta.content
    return stream_text


def unit_test_from_function(
    function_to_test: str,  # python function to be tested as a string
    unit_test_package: str = "pytest",
    approx_num_cases: int = 6,
    print_text: bool = False,
    model_to_use: str = "gpt-3.5-turbo",
    temperature: float = 0.2,
    reruns_if_fail: int = 1,  # if the output code cannot be parsed, this will re-run the function up to N times
) -> str:
    """returns a unit test for a python function"""
    # step 1 , system prompt for assigning role
    system_message = {
        "role": "system",
        "content": "You are a professional Python QA Engineer.",
    }

    user_message = {
        "role": "user",
        "content": f"""Explain the python code delimited by ``` , 
        make sure to use Markdown format , with numbered list , 
        do not use more than 50 words for explaination
        ```{function_to_test}```
        """,
    }

    # form message array to send to API
    explain_messages = [system_message, user_message]
    if print_text:
        print_messages(explain_messages)

    # call completion api , note with stream
    explain_response = call_chat_completion_stream(
        model=model_to_use,
        messages=explain_messages,
        max_tokens=300,
        stream=True,
        temperature=temperature,
    )

    stream_text = iterate_and_update_stream(explain_response, True)

    explain_assistant_message = {"role": "assistant", "content": stream_text}

    # ask GPT to generate a test plan
    plan_user_message = {
        "role": "user",
        "content": f"""
            A good unit test suite , should aim to:
            - test the function for wide range of inputs
            - test edge cases that developer might have missed
            - take advantage of unit-test framework : ```{unit_test_package}``` to make it easy to write tests
            - be easy to read and understand
            - test should always pass or always fail in same way and be consitent

            write a set of {approx_num_cases} scenarios to test the function definition provided in previous prompt.
            Make sure not to use more than 200 words
        """,
    }

    # form a new message array using all previous data
    plan_messages = explain_messages + [explain_assistant_message, plan_user_message]

    if print_text:
        print_messages(plan_messages)

    plan_response = call_chat_completion_stream(
        model=model_to_use,
        messages=plan_messages,
        temperature=temperature,
        max_tokens=400,
        stream=True,
    )

    plan_stream = iterate_and_update_stream(plan_response, True)

    plan_assistant_message = {"role": "assistant", "content": plan_stream}

    # if required add more steps

    # step 3 : generate unit test

    execute_system_message = {
        "role": "system",
        "content": """You a a professional Python QA engineer.You take pride in writing unit tests.
        when asked to generate tests, you reply with code in python format.""",
    }

    execute_user_messsage = {
        "role": "user",
        "content": f"""Using Python 3 and ```{unit_test_package}``` , write a suite of units tests 
        for the function following the test case plan above, generate one test for each case in plan.
        Reply with generated code only""",
    }

    execute_messages = [
        execute_system_message,
        user_message,
        explain_assistant_message,
        plan_user_message,
        plan_assistant_message,
        execute_user_messsage,
    ]

    # call completion api for final
    execute_response = call_chat_completion_stream(
        model=model_to_use,
        messages=execute_messages,
        max_tokens=500,
        temperature=temperature,
        stream=True,
    )

    execution_stream = iterate_and_update_stream(execute_response, True)

    return execution_stream


def is_armstrong_number(number):
    digits = []
    num = number
    count = 0
    while num > 0:
        digit = num % 10
        count += 1
        digits.append(digit)
        num = num // 10

    digits = list(map(lambda x: x**count, digits))
    total = sum(digits)
    return total == number


function_as_string = inspect.getsource(is_armstrong_number)

generated_unit_test = unit_test_from_function(
    function_to_test=function_as_string,
    print_text=True,
)
print(generated_unit_test)
