# remote_commands
## INSTALL
1. download files
2. edit hardcoded links to the server in tk.py and client.py
3. you may edit port of the ws server and the file server
4. run `pip install websockets websocket-client`
5. at your option run `pip install pulsectl pyautogui`
6. if you don't need to control mouse / keyboard or sound, remove the `import pyautogui as pg` and` import pulse` lines from server.py and remove unnecessary commands from rules.json\
**warning:**\
the websocket server port must be one larger than the fileserver port, but you can edit it in web/fn.js
## RUN
run `python3 file.py` for website\
run `python3 server.py`\
open http://localhost:8080 in the browser or run tk.py
