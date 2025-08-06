#!/usr/bin/env python3
import os
import sys
from aiohttp import web
from aiohttp import ClientSession

# The url the alerts should be forwarded to.
# Format: http[s]://{host}:{port}/
PUSHOVER_BASEURL = https://api.pushover.net/1/messages.json
# The token for the Pushover application
# Example: cGVla2Fib29v
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")
# User token for Pushover
USER_KEY = os.environ.get("USER_KEY")

# The ip address the service should listen on
# Defaults to localhost for security reasons
LISTEN_HOST = os.environ.get("LISTEN_HOST", "127.0.0.1")
PORT = 31662


routes = web.RouteTableDef()

# Endpoint for verifying that the service is running
@routes.get("/status")
async def get_status(request):
    return web.Response(status=200)

# Listen to post requests on / and /message
@routes.post("/")
@routes.post("/message")
async def on_message(request):
    content = await request.json()
    # The content of the alert message
    message = content["text"].strip().partition("\n")
    # Extract notification title from the message
    title = message[0].strip()
    message = message[2].strip()
    print(f"========== {title} ==========")
    print(message)
    print(f"{len(title) * '='}======================")

    # Forward the alert to pushover
    pushover_resp = await send_pushover_message(message, APPLICATION_TOKEN, USER_KEY, title=title)

    # Check for http reponse status code 'success'
    if pushover_resp.status == 200:
        print(">> Forwarded successfully\n")
    elif pushover_resp.status in [400, 401, 403]:
        print(f">> Unauthorized! Token APPLICATION_TOKEN='{APPLICATION_TOKEN}' is incorrect\n")
    else:
        print(f">> Unknown error while forwarding to Pushover. Error Code {pushover_resp.status}")

    # Return the pushover status code to truenas
    return web.Response(status=pushover_resp.status)

# Send an arbitrary alert to pushover
async def send_pushover_message(message, token, user_key, title=None, priority=None):
    # Parameters
    params = {"token": token,
              "user": user_key,
              "message": message}

    # Optional Pushover features
    if title:
        params["title"] = title
    if priority:
        params["priority"] = priority

    async with ClientSession() as session:
        async with session.post(PUSHOVER_BASEURL, headers=headers, params=params) as resp:
            return resp

if __name__ == "__main__":
    # Check if env variables are set
    if APPLICATION_TOKEN == None:
        sys.exit("Set Pushover Application Token via 'APPLICATION_TOKEN={token}'!")
    if USER_KEY == None:
        sys.exit("Set Pushover user or group key via 'USER_KEY={token}'!")

    # Listen
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host=LISTEN_HOST, port=PORT)
