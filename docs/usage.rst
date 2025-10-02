Usage
=====

Basic Example
-------------
.. code-block:: python

   import asyncio
   from pytdbot import Client, types

   client = Client(
       token="YOUR_BOT_TOKEN",
       api_id=12345,
       api_hash="YOUR_API_HASH",
       files_directory="BotDB",
       database_encryption_key="your_encryption_key",
       td_verbosity=2,
       td_log=types.LogStreamFile("tdlib.log", 104857600),
   )

   @client.on_updateNewMessage()
   async def print_message(c: Client, message: types.UpdateNewMessage):
       print(message)

   @client.on_message()
   async def say_hello(c: Client, message: types.Message):
       msg = await message.reply_text(
           f"Hey {await message.mention(parse_mode='html')}! I'm cooking up a surprise... 🍳👨‍🍳",
           parse_mode="html"
       )
       async with message.action("choose_sticker"):
           await asyncio.sleep(5)
           await msg.edit_text("Boo! 👻 Just kidding.")

   client.run()

Examples
--------
Check out the `examples directory <https://github.com/pytdbot/client/tree/main/examples>`_ for more examples.

- `Echo Bot <https://github.com/pytdbot/client/blob/main/examples/echobot.py>`_
- `Chat ID Bot <https://github.com/pytdbot/client/blob/main/examples/chatIDBot.py>`_
- `Keyboard Bot <https://github.com/pytdbot/client/blob/main/examples/keyboardBot.py>`_

Advanced Usage
-------------
For more advanced usage, please refer to the API Reference.
