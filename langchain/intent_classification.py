
######
# https://python.langchain.com/docs/tutorials/classification/
######

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# fyi, Retrieves API key from OPENAI_API_KEY environ

tagging_prompt = ChatPromptTemplate.from_template(
    """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Different applications I am aware of are:
- Google Calendar

application reference to the apps as:
- Google Calendar refereed to as gcal

Passage:
{input}
"""
)

class Classification(BaseModel):
    app: str = Field(description="Which SaaS application is needed."),
    app_type: str = Field(description="What type of application is needed.")
    app_reference: str = Field(description="What is the application reference?")
    action: str = Field(description="What action needs to be taken on that application.")

# LLM
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini").with_structured_output(
    Classification
)

inp = "am i required for that meeting?"
prompt = tagging_prompt.invoke({"input": inp})
response = llm.invoke(prompt)

print(response.model_dump())