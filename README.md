# remote_commands
## INSTALL
1. install python3
2. download files
3. edit hardcoded links to the server in tk.py and client.py
4. you may edit port of the ws server and the file server
5. run `pip install websockets websocket-client` in console
6. at your option run `pip install pulsectl pyautogui`
7. if you don't need to control mouse / keyboard or sound, remove the `import pyautogui as pg` and` import pulse` lines from server.py and remove unnecessary commands from rules.json\
**warning:**\
the websocket server port must be one larger than the fileserver port, but you can edit it in web/fn.js
## RUN
run `python3 file.py` to launch the web interface\
run `python3 server.py`\
open http://localhost:8080 in the browser or run tk.py
