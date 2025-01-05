import os
from openai import OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

######
# https://platform.openai.com/docs/guides/function-calling
######

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
            },
        },
    }
]

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
        {
          "role": "user",
          "content": "What's the weather like in Paris today?"
        }
    ],
    tools=tools,
)

print(completion.choices[0].message.tool_calls)