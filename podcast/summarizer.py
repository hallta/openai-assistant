import os
from openai import OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

podcasts = [
    {
        "link": "https://twit.tv/posts/transcripts/week-tech-1013-transcript",
        "title": "This Week in Tech 1013 Transcript",
        "published_date": "Jan 6th 2025",
        "transcript": "stuff happened"
    }
]

# 1. curl the link
# 2. nav the DOM
# 3. body.textual.p[1..]

messages = []
template = """

~~~ 
Title: {title}
Published: {pub}
Transcript:
{transcript}
~~~ 
"""

for p in podcasts:
    messages.append(
        {
            "role": "system",
            "content": template.format(
                title=p["title"],
                pub=p["published_date"],
                transcript=p["transcript"]
            )
        }
    )

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=messages
)

print(completion.choices[0].message)
