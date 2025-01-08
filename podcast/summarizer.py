import html2text
import os
import parsel
import requests
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

h2t = html2text.HTML2Text()

podcasts = [
    {
        "link": "https://twit.tv/posts/transcripts/week-tech-1013-transcript",
        "title": "This Week in Tech 1013 Transcript",
        "published_date": "Jan 6th 2025"
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

    r = requests.get(p["link"])
    html = r.text
    parsel_dom = parsel.Selector(text=html)
    statements = parsel_dom.css("div.body p").getall()

    for s in statements:
        messages.append(
            {
                "role": "system",
                "content": template.format(
                    title=p["title"],
                    pub=p["published_date"],
                    transcript=h2t.handle(s)
                )
            }
        )

messages.append(
    {
        "role": "user",
        "content": "what is the summary?"
    }
)

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=messages
)

print(completion.choices[0].message)
