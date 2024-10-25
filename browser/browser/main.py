import argparse
import json
import subprocess

import html2text
import requests
from connect.utils.terminal.markdown import render


def get_proxies():
    cmd = "snapctl get --view :proxy-observe https -d"
    proc = subprocess.run(cmd.split(), capture_output=True, text=True)

    if proc.returncode != 0:
        raise RuntimeError(proc.stderr)

    proxies = json.loads(proc.stdout)
    return {
        "https": proxies["https"]["url"]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str)
    args = parser.parse_args()

    proxies = get_proxies()
    response = requests.get(args.url, proxies=proxies)

    text = html2text.html2text(response.text)
    print(render(text))
