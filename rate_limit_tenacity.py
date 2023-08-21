import openai
from dotenv import load_dotenv
from openai.error import RateLimitError
import os
import tenacity

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# trigger rate limit error

# for _ in range(1,100):
#     openai.ChatCompletion.create(
#         model = "gpt-3.5-turbo",
#         messages= [{"role":"user","content":"hello"}],
#         max_tokens = 1
#     )

# using tenacity library
from tenacity import retry, stop_after_attempt, wait_random_exponential


def after_attempt_callback(details):
    # <RetryCallState 4408074320: attempt #2;
    tries = str(details).split(";")[0].split(":")[1].strip()
    print(tries)


@retry(
    wait=wait_random_exponential(1, 3),
    stop=stop_after_attempt(3),
    after=after_attempt_callback,
)
def completion_with_backoff(**kwargs):
    response = openai.ChatCompletion.create(**kwargs)
    res_content = response["choices"][0]["message"]["content"]
    res_total_token = response["usage"]["total_tokens"]
    return res_content, res_total_token


for i in range(0, 100):
    try:
        print("calling chat completion for i =", i)
        result = completion_with_backoff(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Coco"}],
            max_tokens=1,
        )
        text, token_count = result
        print(f"""content : {text} and total_tokens : {token_count}""")
    except tenacity.RetryError as e:
        print("Exception caught after 3 retries", e)
        break


print("Rate limit using tenacity library tested")
