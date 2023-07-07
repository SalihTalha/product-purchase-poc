import openai


def query(message):
    openai.api_key = ''
    messages = [{"role": "system", "content":
        "You are a intelligent assistant."}]
    try:
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
    except:
        return "Language Model is not available now. Please try again later or develop your own model."
