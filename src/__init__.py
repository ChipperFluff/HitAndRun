from flask import Flask, render_template, url_for, request, redirect
import configparser
import json
from pathlib import Path

# Assuming logger.py is properly structured as a module
from .logger import debug, info

app = Flask(__name__)

def load_config(config_file: Path):
    info("Loading config...")
    debug("Creating config parser")
    config = configparser.ConfigParser()
    debug(f"Loading config from: {config_file}")
    
    if not config.read(config_file):
        raise FileNotFoundError(f"Unable to find {config_file}")
    
    section = 'connection'
    if section not in config:
        raise KeyError(f"Section {section} not found in the {config_file}")

    host = config[section].get('host', '127.0.0.1')
    port = config[section].getint('port', 5000)
    debug_mode = config[section].getboolean('debug', False)

    return host, port, debug_mode

def render_menu(title: str, description: str, options: list):
    return render_template('index.html', baseURL=url_for("index"),
                           page={"title": title, "description": description},
                           options=options)

def load_menu(file: Path):
    debug(f"Loading menu from: {file}")
    if not file.is_file():
        raise FileNotFoundError(f"Unable to find {file}")

    with file.open("r") as menu_file:
        menu = json.load(menu_file)
    
    options = [{"id": f"{option['next']}:{id}", "text": option['text']}
               for id, option in menu['options'].items()]
    
    return render_menu(menu["page"]["title"], menu["page"]["description"], options)

@app.route("/")
def index():
    info("Rendering index menu...")
    return load_menu(Path("game/start.json"))

@app.route("/option")
def option():
    info("Redirecting to index...")
    return redirect(url_for("index"))

def run():
    info("Starting app...")
    config_path = Path('config.ini')
    host, port, debug_mode = load_config(config_path)
    app.run(host=host, port=port, debug=debug_mode)
