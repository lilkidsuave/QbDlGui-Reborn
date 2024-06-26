# QbDlGui-Reborn

QbDlGui-Reborn is a gui for qobuz-dl by @vitiko98 and @lilkidsuave

## Features

- Download albums, tracks, artists, and playlists from Qobuz.
- Supports various quality levels.
- Embed album art into files.
- Web GUI for easy interaction.
- Easy to setup via Docker Compose.
- Runs on Flask via Gunicorn with Gevent.

## Installation

### Docker

Before using the docker compose, make sure to edit your /downloads bind.
Same goes for the docker command below.

```
docker run -d --name qbdlgui -p 5000:5000 -v Directory:/downloads ghcr.io/lilkidsuave/qbdlgui-reborn:latest
```

Access the web gui via localhost:5000

### Host Install

1. Clone the repository and cd into:

```
https://github.com/lilkidsuave/QbDlGui-Reborn.git
```
```
cd QbDlGui-Reborn
```

2. Virtual Environment: Consider using a virtual environment to isolate the dependencies for the project. This can help avoid conflicts between different versions of libraries. You can create a virtual environment using:

```
python3 -m venv qbdl
source qbdl/bin/activate
```

3. Install the dependencies:

#### Alpine (exactly like the docker image)

```
apk add gcc musl-dev libffi-dev openssl-dev
```
```
pip install -r requirements.txt
```
#### Debian/Ubuntu

```
apt-get update && apt-get install -y gcc libc-dev libffi-dev libssl-dev
```
```
pip install -r requirements.txt
```

#### Fedora

```
dnf install -y gcc glibc-devel libffi-devel openssl-devel
```
```
pip install -r requirements.txt
```

#### Arch

```
pacman -Sy --noconfirm gcc glibc libffi openssl
```
```
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

Refer to the existing documentation for command-line usage.

### Web GUI

To use the web GUI, follow these steps:

1. Run the web GUI script:


```
gunicorn -b 0.0.0.0:5000 --worker-class=gevent --workers=4 qbdl_gui:app
```


2. Open a web browser and navigate to:

```
http://0.0.0.0:5000/
```
```
localhost:5000
```

3. Enter your Qobuz email, password, download URL, download location, and quality.
4. Click the "Download" button to start the download.

## Contributing

Please refer to the existing guidelines for contributing to this project.
