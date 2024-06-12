from pydantic import BaseModel
from llama_index.core import PromptTemplate
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.chat_engine import CondenseQuestionChatEngine
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)


documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine(
    response_mode="tree_summarize")


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

chat_engine = CondenseQuestionChatEngine.from_defaults(
    query_engine=query_engine,
    verbose=True,
)
