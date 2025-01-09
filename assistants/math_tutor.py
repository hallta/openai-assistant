import os
import pprint
from openai import OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

from openai import OpenAI
client = OpenAI()

assistant = client.beta.assistants.create(
    instructions="""
    You are an executive assistant. Your job is to help
    me make my life simpler. Sometimes this is through
    integrating to applications and automating some
    things I need via APIs.

    For example, this might be with Google Calendar.
    I might ask about my day, who is in what meetings,
    when I have breaks, when my day starts, along with
    helping to create meetings and other tasks.
    """,
    name="Executive Assistant",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)

thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread.id,
    role="user",
    content="What's my day look like today?"
)

run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="This is a Google Calendar task"
)

if run.status == 'completed':
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    pprint.pp(messages)
else:
    print(run.status)