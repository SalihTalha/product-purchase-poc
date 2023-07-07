import openai


def query(message):
    openai.api_key = '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'
    messages = [{"role": "system", "content":
        "You are a intelligent assistant."}]

    # you will add the information soon
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        return reply
    else:
        return "Something is wrong with the message. "


print(query("What is 2 + 2?"))
