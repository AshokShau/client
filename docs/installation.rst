Installation
============

Requirements
------------
- Python 3.9+
- Telegram API key from `my.telegram.org/apps`
- TDLib or tdjson
- deepdiff
- aio-pika

Install with TDLib included
---------------------------
.. code-block:: bash

   pip install --upgrade pytdbot[tdjson]

For better performance, install orjson or ujson:

.. code-block:: bash

   pip install orjson
   # or
   pip install ujson

Manual TDLib Installation
-------------------------
.. code-block:: bash

   pip install pytdbot

Then build TDLib from `source <https://github.com/tdlib/td#building>`_ and specify the path using ``Client.lib_path``.

Development Version
------------------
.. code-block:: bash

   pip install --pre pytdbot