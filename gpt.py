import logging

import openai

logging.basicConfig(level=logging.INFO)
logging.info('GPT starting...')

openai.api_key = 'sk-1mxvLHGbkaR7QvkB26B048E2183f4dFdA0D9414292Cc4a37'
openai.api_base = 'https://api.aiguoguo199.com/v1'

tempUsed = 0


def ask_gpt(message, promt, syncBot):
    wait = syncBot.send_message(message.chat.id, '⏳ Ожидайте, подготовка ответа может занять некоторое время...')
    loading = syncBot.send_message(message.chat.id, '⏳')

    comp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": promt
            }
        ],
        stream=True
    )
    next(comp)

    global tempUsed
    tempUsed += 1

    cmp = ''
    x = 0
    for gen in comp:
        try:
            x += 1
            if not gen.choices[0].delta:
                syncBot.delete_message(message.chat.id, wait.message_id)
                syncBot.edit_message_text(cmp, message.chat.id, loading.message_id)
                break

            cmp += gen.choices[0].delta.content
            if not x % 30:
                syncBot.edit_message_text(cmp + '\n\n⏳ Загрузка...', message.chat.id, loading.message_id)

        except Exception as e:
            print(repr(e))
