# Bot Messenger :incoming_envelope:

A Python script, scheduled to run periodically, which analyzes the latest contents of HTML pages, processes them and sends the obtained data to a Telegram channel.


<div align="center">
    <img src="/images/botfather.png" width="300">
    <p>Image of BotFather obtained from Telegram (@BotFather).</p>
</div>

## Features:

1. HTML Parsing;
2. Logging;
3. External API Consumption (Telegram Bots);
4. Tasks scheduling;
5. NoSQL database;
6. Production and Development environments;
7. Docker deployment;
8. Configuration file.

## Run Locally

```bash
pip install -r requirements.txt
python main.py
```

## Docker Installation :whale:

Copy the content of `credentials_example.ini` to a new file *`credentials.ini`*, fill in the fields as you wish and execute the following command:

```bash
curl -sSL https://raw.githubusercontent.com/bartolek153/bot-messenger/main/deploy.sh | sh
```

> Docker and Git must be installed in the local machine!


---

## File Structure

<div align="center">
    <img title="Folder Structure" height="350" alt="Folder Structure" src="/images/tree.png">
</div>

</br>

* **data/** - Data Access Layer, which stores `db.json` and contains a Singleton object, that communicates with the database.
* **logs/** - Set up log handlers, accordingly to the current environment. When running in production mode, keeps history of logs in `app.log`.
* **models/** - Contains the logic necessary to gather information/data. Each area of interest is placed under a different module.
* **telegram_channels/** - communication endpoint between this script and Telegram.
* **tests/** - performs unit tests (development purposes).  
* `constants.py` - global constants accessible from anywhere in the code.
* `environment.py` - sets _Production_ or _Development_ environments.
* `helper.py` - general usage functions
* `main.py` - start point of the program, for production environment.

</br>

---

### **TODO**

* Deploy:
    - Github Workflows

* New Features:
    - Get `News` section

* Code Improvement:
    - Regular expressions
    - Asynchronous flow