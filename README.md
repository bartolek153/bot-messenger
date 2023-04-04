# Bot Messenger 

A python script, scheduled to run periodically, which analyzes the latest contents of HTML pages, processes them and sends the obtained data to a Telegram channel.

## Features:

1. HTML Parsing;
2. Logging;
3. Usage of external API (Telegram);
4. Tasks scheduling;
5. NoSQL database;
6. Production and Development environments;
7. Docker deployment;
8. Configuration file.

## **TODO**

* Deploy:
    - Create a deploy script
    - Attach data volume (db + logs)

* New Features:
    - Get `News` section
    - Pin chat messages

* Code Improvement:
    - Asynchronous flow
    - Comments and docstrings
    - Use environment variables for production and development status