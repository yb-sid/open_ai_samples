from langchain.prompts import StringPromptTemplate
from pydantic import BaseModel, validator

PROMPT_TEMPLATE = """
Given the function name and source code , generate an english language explaination of the function.
Function Name : {function_name},
Source Code : 
{source_code},
Explaination:
"""


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


import inspect


# define a Custom prompt template class
class FunctionExplainerPromptTemplate(StringPromptTemplate, BaseModel):
    @validator("input_variables")
    def validate_input_variables(cls, v):
        """validate input_variable are correct , custom logic"""
        if len(v) != 1 or "function_name" not in v:
            raise ValueError("input_variables should only contain function_name")
        return v

    def format(self, **kwargs):
        function_name = kwargs.get("function_name")
        code_as_text = inspect.getsource(function_name)

        prompt = PROMPT_TEMPLATE.format(
            function_name=function_name.__name__, source_code=code_as_text
        )

        return prompt

    def _prompt_type(self) -> str:
        return "function-explainer"


func_explainer_tempalate = FunctionExplainerPromptTemplate(
    input_variables=["function_name"]
)

# generate a prompt based on defined function

function_prompt = func_explainer_tempalate.format(function_name=is_armstrong_number)

print("Function prompt is : \n", function_prompt)
