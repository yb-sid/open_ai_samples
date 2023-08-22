from function_utils import functions_array, call_chat_completion
import sqlite3
import json

connection = sqlite3.connect("Chinook.db")


# define functions to to execute generated query
def ask_database(query):
    try:
        results = str(connection.execute(query).fetchall())
    except Exception as e:
        results = f"query failed with error : {e}"

    return results


def execute_function(message):
    # check if message's function has function name
    if message.function_call.name == "ask_database":
        query = json.loads(message.function_call.arguments)["query"]
        # print("extracted query is :", query)
        result_text = ask_database(query)
    else:
        result_text = f"Error : function {message.function_call.name} does not exists"

    return result_text


messages = []
messages.append(
    {
        "role": "system",
        "content": "Answer user questions by generating SQL queries against the Chinook Music Database.",
    }
)
messages.append(
    {"role": "user", "content": "Hi, who are the top 5 artists by number of tracks?"}
)

print("Initial messages : ", messages)

try:
    chat_response = call_chat_completion(messages, 500, functions=functions_array)
    assistant_message = chat_response
    print("assistant response : ", assistant_message)
    messages.append(assistant_message)
    if assistant_message.get("function_call"):
        results = execute_function(assistant_message)
        print("Result text : ", results)
        messages.append(
            {
                "role": "function",
                "name": assistant_message["function_call"]["name"],
                "content": results,
            }
        )
    print(messages)
    messages.append(
        {
            "role": "user",
            "content": "What is the name of the album with the most tracks?",
        }
    )
    chat_response = call_chat_completion(messages, 200, functions_array)
    assistant_message = chat_response
    print("assisgtant resposne : ", assistant_message)
    messages.append(assistant_message)
    if assistant_message["function_call"]:
        print("calling 2nd time")
        results = execute_function(assistant_message)
        print("2nd result = ", results)
        messages.append(
            {
                "role": "function",
                "content": results,
                "name": assistant_message["function_call"]["name"],
            }
        )

        print("final messages array is : ", messages)
except Exception as e:
    print("Error caught while calling chat completion API : ", e)


"""
Conclusion : using chat-completion API , to generate argument : (SQL query)
against schema
"""
