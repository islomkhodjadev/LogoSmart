import os

from openai import OpenAI

import os

# Get the current script directory
current_directory = os.path.dirname(__file__)
file_path = os.path.join(current_directory, "context.txt")


def get_ai_response(user_message, content, extra_data=None):
    print(extra_data, "salom")
    client = OpenAI(api_key="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")
    # print(os.getenv("gpt_token"))

    # print(data)
    if extra_data is not None:
        content += extra_data

    completion = client.chat.completions.create(
        # model="ft:gpt-3.5-turbo-0125:swift-launch::8yOs8Oro",
        model="gpt-3.5-turbo",
        temperature=0.4,
        messages=[
            {"role": "system", "content": content}, {"role": "user", "content": user_message}
        ]
    )

    ai_response = completion.choices[0].message
    print(ai_response.content)
    return ai_response.content
