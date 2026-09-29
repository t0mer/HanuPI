# HanuPI

HanuPI is a Raspberry Pi based smart Hanukia (Hanukkah menorah). Nine LED candles (eight candles plus
the Shamash) are wired to the Pi's GPIO pins and can be lit with two physical push buttons or from a
small web interface served by the Pi. The web interface can also play the Hanukkah blessing
(`hanuka.wav`) through a speaker connected to the Pi's audio output.

## Table of Contents

- [Features](#features)
- [How it works](#how-it-works)
- [Components and Frameworks used in HanuPI](#components-and-frameworks-used-in-hanupi)
- [Parts used in HanuPI](#parts-used-in-hanupi)
- [Bringing it all together](#bringing-it-all-together)
- [Installation](#installation)
- [Running as a service](#running-as-a-service)
- [Usage](#usage)
- [API reference](#api-reference)
- [Security notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- 2 candle lighting sequences using physical buttons:
  - **Button 1** lights the Shamash and then candles 1–8 one by one (2 seconds apart), keeps them on
    for 4 seconds and turns everything off.
  - **Button 2** lights all candles at once, keeps them on for 4 seconds and turns everything off.
- Turn individual candles on/off from the web interface by clicking their flames.
- Candle lighting sequence from the web interface (candles stay lit until turned off).
- Candle lighting sequence and playing the blessing from the web interface.
- Turn all candles off from the web interface.
- The web interface polls the candle state every 500 ms, so it also reflects changes made with the
  physical buttons.
- Short "self-test" sweep of all candles on startup.

<!-- TODO: screenshot of the web interface -->

## How it works

`hanupi.py` is a single Python script that:

1. Configures the GPIO pins with [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) using **physical
   (BOARD) pin numbering**: nine outputs for the candles and two inputs (with internal pull-down
   resistors, rising-edge detection, 800 ms debounce) for the buttons.
2. Loads `hanuka.wav` into memory with `soundfile` and plays it with `sounddevice` on the default
   audio output.
3. Runs a [FastAPI](https://fastapi.tiangolo.com/) app with `uvicorn` on port **80** (all
   interfaces), serving the web UI (`templates/index.html` plus static files from `dist/`) and a
   small HTTP API.

Note that HanuPI does not calculate the date or the current night of Hanukkah; you choose which
candles to light.

## Components and Frameworks used in HanuPI

* [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)
* [Loguru](https://pypi.org/project/loguru/)
* [NumPy](https://pypi.org/project/numpy/)
* [Uvicorn](https://pypi.org/project/uvicorn/)
* [FastAPI](https://pypi.org/project/fastapi/)
* [Jinja2](https://pypi.org/project/Jinja2/)
* [sounddevice](https://pypi.org/project/sounddevice/)
* [soundfile](https://pypi.org/project/soundfile/)

## Parts used in HanuPI

* Raspberry Pi 3
* [Raycare 12PCS LED Flameless Taper Candle Lights](https://www.amazon.com/dp/B07DFF3R8K?ref=ppx_yo2ov_dt_b_product_details&th=1)
* [Jumper Wires](https://www.aliexpress.com/item/1899750504.html?spm=a2g0o.order_list.order_list_main.16.63d65e5bOCOYlb)
* [Mini Round Momentary Push Button Switch](https://www.aliexpress.com/item/1005003120023458.html) (x2)
* [PAM8403 Super mini digital power amplifier board](https://www.aliexpress.com/item/32846373616.html)
* 8 ohm speaker

## Bringing it all together

[![Raspberry Pi Pinout](https://github.com/t0mer/HanuPI/blob/main/images/rp_pinout.png?raw=true "Raspberry Pi Pinout")](https://github.com/t0mer/HanuPI/blob/main/images/rp_pinout.png?raw=true "Raspberry Pi Pinout")

The code uses **physical pin numbers** (`GPIO.BOARD`). The BCM GPIO numbers are listed for reference.

### Connecting the candles (ordering right to left)

| Candle  | Physical pin | BCM GPIO |
|---------|--------------|----------|
| Candle1 | 29           | GPIO 5   |
| Candle2 | 37           | GPIO 26  |
| Candle3 | 11           | GPIO 17  |
| Candle4 | 13           | GPIO 27  |
| Shamash | 31           | GPIO 6   |
| Candle5 | 15           | GPIO 22  |
| Candle6 | 16           | GPIO 23  |
| Candle7 | 22           | GPIO 25  |
| Candle8 | 18           | GPIO 24  |

All candles use a common ground.

<!-- TODO: verify whether current-limiting resistors are used between the GPIO pins and the LED candles -->

### Connecting the buttons

| Button   | Physical pin | BCM GPIO                | Action                        |
|----------|--------------|-------------------------|-------------------------------|
| Button1  | 10           | GPIO 15 (UART0 RX)      | Light candles one by one      |
| Button2  | 8            | GPIO 14 (UART0 TX)      | Light all candles at once     |

Both buttons use a common 3.3V (physical pin 1). The inputs use the Pi's internal pull-down
resistors, so pressing a button pulls the pin high.

### Connecting the amplifier

* Ground
* 5V
* The speaker to the amplifier's speaker output
* A small audio plug (3.5 mm) from the Pi's audio jack to the amplifier input

## Installation

HanuPI must run on a Raspberry Pi (it imports `RPi.GPIO`).

1. Install the system packages needed for GPIO access and audio playback (`sounddevice` needs
   PortAudio and `soundfile` needs libsndfile):

   ```bash
   sudo apt update
   sudo apt install -y git python3-pip python3-rpi.gpio libportaudio2 libsndfile1
   ```

2. Clone the repository and install the Python dependencies into a virtual environment. A venv is
   required on Raspberry Pi OS Bookworm and later, where a system-wide `pip install` is refused
   with `externally-managed-environment`. `--system-site-packages` keeps the apt-installed
   `RPi.GPIO` importable inside the venv:

   ```bash
   git clone https://github.com/t0mer/HanuPI.git
   cd HanuPI
   python3 -m venv --system-site-packages venv
   venv/bin/pip install -r requirements.txt
   ```

3. Run it from the repository directory (the script loads `hanuka.wav`, `templates/` and `dist/`
   from the current working directory). Port 80 requires root privileges, so run the venv's
   Python with `sudo`:

   ```bash
   sudo venv/bin/python hanupi.py
   ```

On startup all candles light up briefly one after the other and then turn off, and the log shows
`Hanukia is on`.

## Running as a service

The repository includes a systemd unit, `hanupi.service`. It expects the project files
(`hanupi.py`, `hanuka.wav`, `templates/` and `dist/`) to be located **directly in `/opt/`**
(`WorkingDirectory=/opt/`, `ExecStart=/usr/bin/python3 /opt/hanupi.py`), runs as user `pi` and
restarts automatically.

**As shipped, the unit does not work:** it runs as user `pi`, which cannot bind port 80, so the
service crash-loops. It also uses the system Python, which does not see the packages installed in
the venv. Before enabling it you must edit `hanupi.service`:

- Point `ExecStart` at the venv's Python: `ExecStart=/opt/venv/bin/python /opt/hanupi.py`.
- Allow binding port 80: either change `User=pi` to `User=root`, or keep `User=pi` and add
  `AmbientCapabilities=CAP_NET_BIND_SERVICE` to the `[Service]` section.

```bash
sudo cp -r hanupi.py hanuka.wav templates dist requirements.txt /opt/
sudo python3 -m venv --system-site-packages /opt/venv
sudo /opt/venv/bin/pip install -r /opt/requirements.txt
sudo cp hanupi.service /etc/systemd/system/
sudo nano /etc/systemd/system/hanupi.service   # apply the ExecStart and User/AmbientCapabilities edits above
sudo systemctl daemon-reload
sudo systemctl enable --now hanupi.service
sudo journalctl -u hanupi.service -f   # view logs
```

If you keep the files or the venv elsewhere, edit `WorkingDirectory` and `ExecStart` accordingly.

## Usage

Open `http://<raspberry-pi-ip>/` in a browser. The page shows the menorah and a sidebar menu (in
Hebrew):

| Menu item   | Meaning             | Action                                                              |
|-------------|---------------------|---------------------------------------------------------------------|
| הדלק        | Light               | Lights the Shamash and candles 1–8 one by one, 2 seconds apart      |
| הדלק וברך   | Light and bless     | Plays the blessing and runs the same lighting sequence              |
| כבה נרות    | Turn off candles    | Turns all candles off                                               |

Click a flame to toggle a single candle.

## API reference

All endpoints are plain `GET` requests. FastAPI's interactive documentation is available at
`/docs` (the `/` and `/light` routes are hidden from it).

| Method | Path          | Parameters                                                      | Description |
|--------|---------------|-----------------------------------------------------------------|-------------|
| GET    | `/`           | –                                                               | Web interface. |
| GET    | `/light`      | `candle` = `Shamash`, `C1`…`C8`; `status` = `1` (on) or anything else (off) | Turns a single candle on or off (see the note below). |
| GET    | `/light/all`  | –                                                               | Turns all candles off, then lights the Shamash and C1–C8 one by one (2 seconds apart). Returns after the sequence completes. |
| GET    | `/light/off`  | –                                                               | Turns all candles off. |
| GET    | `/play`       | –                                                               | Plays `hanuka.wav`. Returns when playback finishes. |
| GET    | `/status`     | `candle` = `Shamash`, `C1`…`C8`                                 | Returns `1` if the candle is on, `0` if off. |

> **Note:** in the current code the `/light/off` route handler reuses the name of the internal
> `light_off()` helper, so `/light?status=0` (and clicking a lit flame in the web interface) turns
> **all** candles off, not just the selected one.
>
> `candle` is looked up by name in the script's globals without validation, so an unknown or
> missing candle name on `/light` or `/status` returns **HTTP 500**.

Examples:

```bash
curl "http://<raspberry-pi-ip>/light?candle=C1&status=1"
curl "http://<raspberry-pi-ip>/status?candle=C1"
curl "http://<raspberry-pi-ip>/light/off"
```

## Security notes

- The web interface and API have **no authentication** and listen on all interfaces
  (`0.0.0.0:80`). Anyone who can reach the Pi can control the candles and play audio. Keep it on a
  trusted local network and do not expose it to the internet.

## Troubleshooting

- **The service fails to start with a permission error on port 80** – binding to ports below 1024
  requires root privileges, while `hanupi.service` runs as user `pi`. Set `User=root` or add
  `AmbientCapabilities=CAP_NET_BIND_SERVICE` in `hanupi.service` (see
  [Running as a service](#running-as-a-service)).
- **`ModuleNotFoundError` (e.g. `loguru`, `fastapi`)** – the dependencies are installed in the venv;
  run the script with the venv's Python (`venv/bin/python`), not the system `python3`.
- **Files not found (`hanuka.wav`, `templates`, `dist`)** – the script uses paths relative to the
  working directory. Run it from the project directory, or make sure `WorkingDirectory` in the
  service file points to the folder containing these files.
- **No sound** – the blessing plays on the default audio output. Make sure audio is routed to the
  3.5 mm jack and that the amplifier is powered.
- **Buttons trigger unexpectedly or not at all** – the buttons use physical pins 8 and 10, which are
  also the UART0 TX/RX pins. Only if the serial console is enabled in `raspi-config`, it may
  interfere with the buttons; in that case disable it there. <!-- TODO: verify -->

## Contributing

Issues and pull requests are welcome at [github.com/t0mer/HanuPI](https://github.com/t0mer/HanuPI).

## License

This project is licensed under the [MIT License](LICENSE).
