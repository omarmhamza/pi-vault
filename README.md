# pi-vault

<p align="center">
  <img width=650  src="https://i.ibb.co/SNMFNFg/pivault.png  ">

</p>
<p align="center">
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/flask">
<img alt="Docker Image Size (latest by date)" src="https://img.shields.io/docker/image-size/omarmhamza/pi-vault">
<img alt="Docker Image Version (latest by date)" src="https://img.shields.io/docker/v/omarmhamza/pi-vault">
<p>

<p align="center">
  <img  src="https://i.ibb.co/FY5FnFK/ezgif-com-gif-maker.gif ">
</p>

<h2>pi-vault is a web based software for the Raspberry Pi, it is used to store your sensitive data such as passwords in an encrypted manner. The web interface allows you to create accounts and store online credentials such as emails,usernames and passwords</h2>


<br>


# Motivation

Storing digital records has always been a hassle; I do not trust using a password managers or tools such as the built in password manager on google chrome's browser. Because, they are always prone to secuity breaches and vulnerabilities. Therefore, I decided to create my own vault on my Raspberry Pi. This way I can store whatever I like knowing that I am offline and using secure encrypted operations.  

<br>

# Install with Docker 
## Requirements


<h2> Using on a Raspberry Pi [TESTED] </h2>

<p> 64-bit CPU architecture is needed to run the mongodb database, therefore this will work on Raspberry Pi models (3/4/400) with 64-bit CPU architecture (arm64v8) and supporting OS such as Ubuntu Server/Desktop<p>

- Models: (3/4) (tested on model 4)
- OS: [Ubuntu Server/Desktop](https://ubuntu.com/download/raspberry-pi) (tested)
- [Docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) installed

<h2> Using on Linux [TESTED]</h2>

- x86_64 (or amd64), armhf, and arm64 architectures distro.

- [Docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) installed

<h2> Using on Windows [NOT TESTED] </h2>

- [Docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) installed

<br>

## Install 
Make sure you got [Docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) installed

```shell
$ git clone https://github.com/omarmhamza/pi-vault.git
$ cd pi-vault
$ docker-compose up
```
Note: If you are running on Linux/Windows make sure to change parameter image "arm64v8" to "latest" in docker-compose.yaml

<br>

# Install without Docker
## Requirements
- Python 2/3
- [MongoDB database](https://docs.mongodb.com/manual/installation/)

## Install & Run

```shell
$ git clone https://github.com/omarmhamza/pi-vault.git
$ cd pi-vault
$ # it is recommended to create a virtual env for the python packages at this stage
$ export MONGO_URI="YOUR_DATABASE_CRED_HERE/vault" # your database credentials default: mongodb://localhost:27017/vault
/pi-vault$ ./install/install.sh 
/pi-vault$ # this shell script will install the python packages using pip, it will create a secret key for encryption purposes and install required data to the database needed by the application. 
/pi-vault$ python3 -m venv env # for python 2: python -m virtualenv env 
/pi-vault$ source env/bin/activate
/pi-vault$ export FLASK_APP="flasky.py" 
/pi-vault$ export FLASK_ENV="development" # or "production"
/pi-vault$ export FLASK_DEBUG= 1 # or 0 to use with production
/pi-vault$ flask run --host="0.0.0.0" --port="5000"
```


# Documentation

## What you need to know
<p>The application uses Flask on the back end and Vuejs on the front-end.<br> The structure of the project is under /app/main. It is split into views/forms/methods and class files such as Account.py. <br> All the static (css/js) is available under app/static and html templates under app/template/ The app/version is used for the about page and version/hardware spec page. Lastly, the configuration of the application is found in config.py</p>

<br>

## Encryption
The application currenlty uses standard [Fernet symmetric encryption ](https://cryptography.io/en/latest/fernet.html)(to store passwords) combined with one way hash [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2) encyption (for accounts). 

How your account and password details will look like: 

```json
[
  {
    "_id": "25418",
    "authentication": {
      "hashed": "pbkdf2:sha256:150000$TTdRTOCx$8bf39d0fe8a937f38e6b9d7b0ea861ab1bea2eb1500ce682855a59a43eb2464a",
      "face": ""
    },
    "created": "13/12/2020, 00:53:17",
    "passwords": [
      {
        "aibGDyKNDEWafuszBmftj2": {
          "encrypted": "gAAAAABf1lSTqL3ZC1MTg8mjoVJl7tBxnLNUPsRj7f-bmZjdaDKeAtAu35I07Izqq424wnaFjqheDPO3xqGw-1Kq2-HXQuznOg==",
          "website": "gAAAAABf1lST3BaA7c-X0QLIAChPQthDAuRZZz1gDIzeBtAqfwR5UCYA_D8YPaS9SDKbDhuSrbG4cbgMnSvU5lX2ILA3iympwQ==",
          "username": "gAAAAABf1lSTa-xIU11VXFsReYBWgdUEhbsgisprvEl950w8mS__5MmBnE_Kt37n4wU7WcP98d1Eqika1V8H2e5_Eb75vNTuDw==",
          "validURL": false,
          "modified": "",
          "created": "13/12/2020, 20:51:15",
          "icon": {
            "_id": 429,
            "name": "Key",
            "tags": [],
            "unicode": "f084"
          }
        }
      },
      {
        "ia696C2ioeVB9UqG6hGrqa": {
          "encrypted": "gAAAAABf1lTA9d-3K2blIK2ipJb5LaZFPsAYeOW6kVHB18YONWCPYSz1K6HZzbOde76eErDS6q9cA25rmaoaUP3Vq5FAd-Uuig==",
          "website": "gAAAAABf1lTAsri7lCs9oXkGMyxuLEOrK9yk23CBV4zSX3vAldQ1QD644LerfdWzKteBkRKLP1fXMDmzY3d721Q1pSTHLZFX5g==",
          "username": "gAAAAABf1lTARVrTBU6Z_bul8t0KdFUkEMb--Fz9pSoC-QQr2wIu0ob8E8Hu4v7TO-giNAb2Iaexpn424ezGjlo3OZbYiee67w==",
          "validURL": false,
          "modified": "",
          "created": "13/12/2020, 20:52:00",
          "icon": {
            "unicode": "f084"
          }
        }
      },
      {
        "hohbpJSzz5bZdYW2wXaPxW": {
          "encrypted": "gAAAAABf3zi4WqS1CO_CM9Y5OZ8sPvSDDgb_PNiDArVn_TNYRz0PETutTquCDP8Odo-r5aSc82zfs3LUIQps6jw8BdySzOQ2eg==",
          "website": "gAAAAABf3zi4iDcqM6izHqyBymUC9NyiM0FB_GcC2sVD53ud7tNUzZWCOho-xmM-BhAL7dy-XrSnhDr7xnXdyABVP5iyF86f5A==",
          "username": "gAAAAABf3zi4vJAGmZywFeggT6o-5d0P3uhLwMbRqyC14WS1njF5sDPuAkeiZO3pfmgWtpho9lMB0ZCr36IxXc9F4_2Z240owg==",
          "validURL": false,
          "modified": "",
          "created": "20/12/2020, 14:42:48",
          "icon": {
            "_id": 429,
            "name": "Key",
            "tags": [],
            "unicode": "f084"
          }
        }
      }
    ],
    "total_passwords": 3,
    "username": "omar"
  }
]

```

## Changing Encryption method

    You can change that by overriding Encryption class methods encrypt/decrypt in Encryption.py 

# How you can contribute (Road Map)

    ⭕ Create offline password reset method.
    ⭕ Implement a more secure way to store secret keys 
    ⭕ Support other data to store such as text, passport details or credit card information
    ⭕ Create RESTful API for the application. 
    ⭕ Create web browser extension (such as the google chrome "add password" prompt) 
    ⭕ Add login using face recoginiton.
    ⭕ Optimize secuirty policies and implement https protocol

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

<br> 

# Credits & Contributors 

- [Omar Hamza](https://github.com/omarmhamza) - Initial Work
- [WrapPixel - Ample Admin](https://www.wrappixel.com/demos/admin-templates/ampleadmin/ample-admin-lite/) - Lite Bootstrap Theme


# MIT License


Copyright (c) 2020 Omar Hamza

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.