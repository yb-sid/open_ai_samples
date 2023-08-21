import openai
from openai.error import RateLimitError
import os
from dotenv import load_dotenv
import backoff


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def call_completion(**kwargs):
    response = openai.ChatCompletion.create(**kwargs)
    res_content = response["choices"][0]["message"]["content"]
    res_total_token = response["usage"]["total_tokens"]
    return res_content, res_total_token


"""
{'target': <function retryable_call_completion at 0x10431bba0>,
 'args': (), 
 'kwargs': {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': 'mercedes'}],
   'max_tokens': 5},
     'tries': 1, 'elapsed': 3.6e-05, 
     'wait': 0.7699950247486302, 
     'exception': RateLimitError(message='Rate limit reached for default-gpt-3.5-turbo in organization org-Ipkgjb8eV212suWndEgA3XmD on requests per min. Limit: 3 / min. Please try again in 20s. Contact us through our help center at help.openai.com if you continue to have issues. Please add a payment method to your account to increase your rate limit. Visit https://platform.openai.com/account/billing to add a payment method.', http_status=429, request_id=None)}
"""


def retry_callback(details):
    # print(details)
    print(f"Retry attempt {details['tries']} triggered due to exception")


@backoff.on_exception(
    backoff.constant, RateLimitError, max_tries=3, on_backoff=retry_callback
)
def retryable_call_completion(**kwargs):
    return call_completion(**kwargs)


for i in range(1, 100):
    try:
        content, token_count = retryable_call_completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "mercedes"}],
            max_tokens=1,
        )

        print(f"""resposne :: content : {content} and total_tokens : {token_count}""")
    except openai.OpenAIError as e:
        print("Max retires done Exception caught :", e._message)
        break

print("rate limit with backoff tested")
