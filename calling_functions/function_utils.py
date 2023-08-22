from db_utils import get_database_info


database_info = get_database_info()

# format database info into text
database_info_text = "\n".join(
    [
        f"Table : {table['table_name']}\nColumns: {','.join(table['column_names'])}"
        for table in database_info
    ]
)

# print(database_info_text)  # 280 tokens

functions_array = [
    {
        "name": "ask_database",
        "description": """Use this function for answer user questions about music database.
        Input/Argument should be a fully formed SQL query""",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""SQL query extraction information to answer user's question.
                    SQL should be written using following schema delimited by ```:
                    ```{database_info_text}```
                    The query should be returned in plain text, not in JSON.
                    """,
                }
            },
            "required": ["query"],
        },
    }
]

import openai
from openai.error import OpenAIError
import os
from dotenv import load_dotenv
from tenacity import wait_random_exponential, retry, stop_after_attempt

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-3.5-turbo"


@retry(wait=wait_random_exponential(2, 40), stop=stop_after_attempt(3))
def call_chat_completion(
    message_array, max_tokens, functions=None, function_call=None, model=MODEL
):
    completion_args = {
        "model": model,
        "messages": message_array,
        "max_tokens": max_tokens,
    }

    if functions is not None:
        completion_args.update({"functions": functions})
    if function_call is not None:
        completion_args.update({"function_call": function_call})

    try:
        response = openai.ChatCompletion.create(**completion_args)
        print("token used is : ", response.usage.total_tokens)
        return response.choices[0].message
    except OpenAIError as e:
        print("OpenAIError caught : ", e._message)
        raise e
