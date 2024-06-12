from llama_index.experimental.query_engine import PandasQueryEngine
import pandas as pd

from llama_index.core import PromptTemplate

df = pd.read_csv('data/data.csv')
query_engine = PandasQueryEngine(df=df)


new_prompt = PromptTemplate(
    """
Given an input question, synthesize a response from the query results. Response should include info about: brand, model, body style (if possible), price per day for 1-3 days, location(if possible), contact person
Query: {query_str}

Pandas Instructions :
{pandas_instructions}

Pandas Output: {pandas_output}

Response:
"""
)
query_engine.update_prompts({"response_synthesis_prompt": new_prompt})
new_prompt = PromptTemplate(
    """\
You are working with a pandas dataframe in Python.
dataframe incule info about rental car. dataframe have those columns: Brand, Model(possibly include body style),Price per day for 1-3 days,Locations(city and sometimes county),Contact person
The name of the dataframe is `df`.
This is the result of `print(df.head())`:
{df_str}

Follow these instructions:
{instruction_str}
Query: {query_str}

Expression: """
)

query_engine.update_prompts({"pandas_prompt": new_prompt})
response = query_engine.query(
    "List me Audi RS6 in Spain.",
)
print(response)
