# MARK MONitor
### Discord.py bot that tracks system resources
## Installation
1. Clone the repository
```
git clone https://github.com/Marcotrix/markmon
```

3. Create a .env file
```
TOKEN=YOUR_TOKEN_HERE
```
3. Install the required modules
```
pip install discord psutil dotenv
```
4. Run the bot
```
python3 main.py
```
## Service
To automatically run markmon, create a service:
```bash
nano /etc/systemd/system/markmon.service
```

and paste this inside it!
```
[Unit]
Description=markmon
After=network.target

[Service]
ExecStart=/usr/bin/python3 /PATH/TO/MARKMON/main.py
WorkingDirectory=/PATH/TO/MARKMON
Restart=always
RestartSec=0
StartLimitInterval=0
StartLimitBurst=0

[Install]
WantedBy=default.target
```

then run this.
```bash
sudo systemctl start markmon
sudo systemtl enable markmon
```

