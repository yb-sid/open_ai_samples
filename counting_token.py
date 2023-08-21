import tiktoken
from tiktoken import Encoding

# get encoding for a model
model_encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

# text into encoding
encoded_lst = model_encoding.encode("The quick brown fox jumps quickly")

# print(encoding_list)


def get_num_token(text: str, encoding_name: str) -> int:
    """returns number of tokens in a text for a given model encoding"""
    encoding = tiktoken.get_encoding(encoding_name)
    token_list = encoding.encode(text)
    return len(token_list)


# cl100k_base , for gpt-3.5-turbo and gpt-4

num_tokens = get_num_token("Write a python code for QuickSort", "cl100k_base")
print("token length : ", num_tokens)

encoded_list = [791, 4062, 14198, 39935, 35308, 6288]

text_decoded = model_encoding.decode(encoded_list)
print(text_decoded)


byte_decoded_text = [
    model_encoding.decode_single_token_bytes(token) for token in encoded_list
]

print("byte decoded text = ", byte_decoded_text)

#############
# comparing encodings


def compare_encoding(text: str) -> None:
    """print comparison between three encodings"""
    print(f"""\n Example String is : {text} \n""")

    for encoding_name in ["cl100k_base", "p50k_base", "gpt2"]:
        encoding = tiktoken.get_encoding(encoding_name)
        token_integers = encoding.encode(text)
        num_tokens = len(token_integers)

        token_bytes = [
            encoding.decode_single_token_bytes(token) for token in token_integers
        ]

        print(f""" {encoding_name} : {num_tokens} token""")
        print(f"""token encoded into integers : {token_integers}""")

        print(f""" token bytes : {token_bytes}""")


compare_encoding("if you're happy and you know")
# pk_50k and gpt are almost same encoding
compare_encoding("what is the number of active customers last 30 days")
