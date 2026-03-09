# Cirno-py
A cirno themed discord bot made with pycord.

## Setup
First, clone this repository recursively:
```bash
git clone https://github.com/throwawaychris/cirno-py.git
```

Fill out your personal data into ```.env_example``` and rename to ```.env```
```bash
mv .env_example .env
```

## Configuration
Bot config is managed in ```utils/config.py```. Do not change bot related directory paths in the config.

## Running
Start the dockerfile
```bash
docker-compose up -d --build
```