from flask import Flask, render_template, url_for, request, redirect
import configparser
import os
from .logger import debug, info

app = Flask(__name__)

def load_config(config_file:str):
    info("Loading config...")
    debug("create logger parser")
    config = configparser.ConfigParser()
    debug(f"loading config from: {config_file}")
    if not config.read(config_file):
        raise FileNotFoundError(f"Unable to find {config_file}")
    
    connection_config = 'connection'
    if connection_config not in config:
        raise KeyError(f"Section {connection_config} not found in the {config_file}")

    host = config[connection_config].get('host', '127.0.0.1')  # Default to localhost
    port = config[connection_config].getint('port', 5000)      # Default to port 5000
    debug_mode = config[connection_config].getboolean('debug', False)  # Default to False

    return host, port, debug_mode

def render_menue(title:str, description:str, options:list):
    return render_template('index.html', baseURL=url_for("option"),
                           page={"title": title, "description": description},
                           options=options)

@app.route("/")
def index():
    return render_menue("HitAndPlay", "a fun game",                         
                        options=[{"id": 100, "text": "Play"},
                                {"id": 100, "text": "About"},
                                {"id": 100, "text": "Leaderboard"}])

@app.route("/option")
def option():
    return redirect(url_for("/"))

def run():
    info("Starting app...")
    host, port, debug_mode = load_config('config.ini')
    app.run(host=host, port=port, debug=debug_mode)

if __name__ == '__main__':
    run()
