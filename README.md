# Open AI API + LangChain 

- Repository contains several custom implementation of openai-cookbook examples  https://github.com/openai/openai-cookbook/tree/main

- GPT-3.5-turbo Model Supports functions , which are great way to generate dynamic arguments using ChatCompletion API.  

- This allows for more structred way to interact with API.   
Example :  https://platform.openai.com/docs/guides/gpt/function-calling


- Langchain : (https://python.langchain.com/docs/get_started/introduction) 
    - Framework for developing applications using LLM
    - Langchain is a wrapper around multiple API's like OpenAI , humans.ai , google palm
    - Features Extensive API for interacting with models , output parsing and external data agents
    - A `Chain` in langchain are combination of LLM+prompts , and they can be combined to form a flow of conversation.
    - **Vectors, Stores, and Embeddings Extend LLM Functionality**

        - Large Language Models (LLMs) come with a limitation related to context length when engaging in conversations. Vectors, vector stores, and embeddings play a crucial role in addressing this limitation.

        - LLMs, by themselves, have a restricted context capacity during conversations. However, the integration of vectors, vector stores, and embeddings extends their capabilities and enables them to overcome this constraint.
    - Agents extend the functionality of LLMs by allowing LLM to interact with external APIs.



- CADTH : https://www.cadth.ca/reimbursement-review-reports

    - Use LLM and Langchain to analyse evidence of reimbursement reports.




