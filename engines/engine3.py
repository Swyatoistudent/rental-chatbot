from pydantic import BaseModel
from llama_index.core import PromptTemplate
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)


class Car(BaseModel):
    """ Data model for car """
    brand: str
    model: str
    body_style: str = "Unknown"
    price_per_day_for_1_3_days: str = "need to detail"
    location: str = "Unknown"
    contact_person: str = "Unknown"


documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine( output_cls=Car,
    llm=llm,response_mode="tree_summarize")


new_summary_tmpl_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "Columns to include in response response: brand, model, body style (if possible), price per day for 1-3 days, location, contact person. "
    "Query: {query_str}\n"
    "Answer: "
)
new_summary_tmpl = PromptTemplate(new_summary_tmpl_str)
query_engine.update_prompts(
    {"response_synthesizer:summary_template": new_summary_tmpl}
)

response = query_engine.query(
    'Offer me a car from a company founded in 1939 in Italy'
)

print(response)
