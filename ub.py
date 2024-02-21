from telethon.sync import TelegramClient, events

import asyncio

import os

import sys

import yt_dlp

import subprocess

import io

import traceback

import requests

from PIL import Image, ImageFont

import time

from bs4 import BeautifulSoup

api_id = 21447825

api_hash = "6c074053121dd6489ead2910821395b9"

bot_token = "7063842591:AAFmErAZwWsfFI53k0Q3EY7Zy47h4PwEXnA"

owner = 6721958943

BOT = TelegramClient("9XO", api_id, api_hash).start(bot_token=bot_token)

print(BOT.get_me())

BOT.send_message(owner, "HELLO")

start = time.time()

@BOT.on(events.NewMessage(pattern="/start"))

async def hello(event):

    global start

    end = time.time()

    r = await event.respond("pro")

    await asyncio.sleep(2)

    await r.edit(f"pong .. {end-start}")

@BOT.on(events.NewMessage(pattern="\.restart"))

async def restart(event):

    await event.reply("X")

    python = sys.executable

    os.execl(python, python, *sys.argv)

@BOT.on(events.NewMessage(pattern="\.eval"))

async def dlpro(event):

    r = await event.reply("processing...")

    try:

        text = event.text.split(maxsplit=1)[1]

    except IndexError:

        if event.is_reply:

            reply = await event.get_reply_message()

            text = reply.text

        return await r.edit("gib some text")

    file = io.StringIO()

    sys.stdout = file

    try:

        exec(text)

    except Exception:

        file.write(traceback.format_exc())

    sys.stdout = sys.__stdout__

    if len(file.getvalue()) > 4096:

        f = open("eval.txt", "w")

        f.write(file.getvalue())

        return await r.respond(file="eval.txt")

    return await r.edit(file.getvalue())

@BOT.on(events.NewMessage(pattern="\.gpt"))

async def gpt(event):

    text = event.text.split(maxsplit=1)

    if event.is_reply and not len(text) == 2:

        msg = await event.get_reply_message()

        query = msg.text

    elif len(text) == 2:

        query = text[1]

    else:

        return await event.edit("bhen ke loude kya question hai tera ")

    reply = await event.reply("...")

    text = query

    params = {"model_id": 5, "prompt": text}

    try:

        req = requests.post("https://lexica.qewertyy.dev/models", params=params)

    except Exception as e:

        return await reply.edit(str(e))

    if req.status_code == 200:

        req = req.json()

        content = req["content"]

        text = f"Gpt: \n\n {content}"

        return await reply.edit(text)

    else:

        return await reply.edit("Mar gya bhai tera")

@BOT.on(events.NewMessage(pattern="\.bash", from_users=owner))

async def bas(event):

    r = await event.respond("peru....")

    args = event.text.split(maxsplit=1)

    if not len(args) == 2:

        return await r.edit("Give some bash cmd")

    else:

        a = subprocess.run(args[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

        out = "<pre><code>FUCKSES</code></pre>"

        if a.stdout:

            out = a.stdout

        elif a.stderr:

            out = a.stderr

        else:

            pass

        if len(out) > 4096:

            with open('bash.text', 'w') as file:

                file.write(out)

            return await event.respond(f"<pre><code class=\"language-bash\">{args[1]}</code></pre>", file='bash.text', parse_mode='html') 

        return await r.edit(f"<pre><code class=\"language-EOR_OP\">{out}</code></pre>", parse_mode='html')

@BOT.on(events.MessageEdited(pattern="/eval", from_users=owner))

@BOT.on(events.NewMessage(pattern="/eval"))

async def eval(event):

	try:		args = event.text.split(maxsplit=1)[1]

	except IndexError:

		return await event.edit('Give some Python Code')

	OLDOUT = sys.stdout

	OLDER = sys.stderr

	NEWOUT = sys.stdout = io.StringIO()

	NEWER = sys.stderr = io.StringIO()

	stdout, stderr, exc, = None, None, None

	try:

		value = await aexec(args, event)

	except Exception:

		value = None

		exc = traceback.format_exc()

	NEWOUTT = NEWOUT.getvalue()

	NEWERR = NEWER.getvalue()

	sys.stdout = OLDOUT

	sys.stderr = OLDER

	edit = ''

	if exc:

		edit = exc

	elif NEWOUTT:

		edit = NEWOUTT

	elif NEWERR:

		edit = NEWERR

	else:

		edit = '<pre><code>SUCKSEXX</code></pre>'

#	final_output = "EVAL : ♡\n "

	final_output = f"<pre><code>{args}</code></pre>"

#	final_output += "OUTPUT: ☆\n"

	final_output += f"<pre><code>{edit.strip()}</code></pre> \n"

	if len(final_output) > 4096:

		with open('eval.text',  'w') as file:

			file.write(final_output)

			file.close()

		await event.respond(f'<pre><code class=language-Python >{args}</code></pre>',file='eval.text', parse_mode='html')

	else:

#		if args[0] == ".ev":

#			return await event.respond(f'<pre><code class=language-EOR_OP>{edit.strip}</code></pre>', parse_mode='html')

		await event.respond(final_output, parse_mode='html')

async def aexec(code, event):

    exec((

        "async def __aexec(event):"

        + "\n p = print"

        + "\n owner = 6871789911"

        + "\n r = await event.get_reply_message()"

        + "\n HOST='Pydroid 3 v.7.02_arm64' "

        + "\n chat = event.chat_id"

        	)

        + "".join(f"\n {l_}" for l_ in code.split("\n"))

    )

    return await locals()["__aexec"](event)

BOT.run_until_disconnected()
