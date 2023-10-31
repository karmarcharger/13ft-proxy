# 13ft-proxy
13ft with proxy support
![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/karmarcharger/13ft-proxy-march/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/karmarcharger/13ft-proxy-march)
[![Docker Image Size](https://badgen.net/docker/size/karmarcharger/13ft-proxy-march?icon=docker&label=image%20size)](https://hub.docker.com/r/karmarcharger/13ft-proxy-march)

Docker container for 13ft https://github.com/wasi-master/13ft

## Changes:

Changed from using /article http post to /link http get, when inside a page and click any link, it will try to feed it back into this container and load it instead of directly loading the page based on url.

added proxy support to the requests (tested working with ubuntu's squid proxy)

added garbage collection and setted port to 8083 by default, fixed the requirements by adding requests

## Environment variables:
| Env | Default | Example | Description |
| - | - | - | - |
| `PROXY` | - | `192.168.1.100:8123` | Put the URL:port of your proxy **optional|
| `HOSTNAME` | - | `host.myserver.com` | Put the domain/ip of this container so that link redirect works  **required|

## Docker Command
<pre>docker run -p 8084:8084 -e PROXY="192.168.1.100:8123" -e HOSTNAME="host.myserver.com"  karmarcharger/13ft-proxy-march:latest</pre>

## Docker compose
<pre>
version: '3.3'
services:
    13ft-proxy-march:
        ports:
            - '8084:8084'
        environment:
            - PROXY=192.168.1.100:8123
            - HOSTNAME=host.myserver.com
        image: 'karmarcharger/13ft-proxy-march:latest'
</pre>


# from https://github.com/wasi-master/13ft
# 13 Feet Ladder

A site similar to [12ft.io](https://12ft.io) but is self hosted and works with websites that 12ft.io doesn't work with.

## What is this?

This is a simple self hosted server that has a simple but powerful interface to block ads, paywalls, and other nonsense. Specially for sites like medium, new york times which have paid articles that you normally cannot read. Now I do want you to support the creators you benefit from but if you just wanna see one single article and move on with your day then this might be helpful

## How does it work?

It pretends to be GoogleBot (Google's web crawler) and gets the same content that google will get. Google gets the whole page so that the content of the article can be indexed properly and this takes advantage of that.

## How do I use it?

First make sure you have [python](https://python.org) installed on your machine, then go to a terminal (`Command Prompt` on Windows, `Terminal` on Mac) and run the following command:

```sh
python -m pip install flask
```

If that doesn't work retry but replace `python` with `py`, then try `python3`, then try `py3`

Then download the file `portable.py` and run it, click [this link](https://realpython.com/run-python-scripts/) for a tutorial on how to run python scripts

Then follow these simple steps

### Step 1

![step 1 screenshot](screenshots/step-1.png)
Go to the website at the url shown in the console

### Step 2

![step 2 screenshot](screenshots/step-2.png)
Click on the input box

### Step 3

![step 3 screenshot](screenshots/step-3.png)
Paste your desired url

### Step 4

![step 4 screenshot](screenshots/step-4.gif)
Voilà you now have bypassed the paywall and ads

### Alternative method

You can also append the url at the end of the link and it will also work. (e.g if your server is running at `http://127.0.0.1:5000` then you can go to `http://127.0.0.1:5000/https://example.com` and it will read out the contents of `https://example.com`)

This feature is possible thanks to [atcasanova](https://github.com/atcasanova)
