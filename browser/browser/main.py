import argparse
import subprocess

import html2text
import requests
from connect.utils.terminal.markdown import render

def get_proxies():
    proxies = {}
    return proxies


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str)
    args = parser.parse_args()

    proxies = get_proxies()
    response = requests.get(args.url, proxies=proxies)

    text = html2text.html2text(response.text)
    print(render(text))
