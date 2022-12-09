# HanuPI
HanuPi is Raspberry pi based smart Hanukia that cn be turned on using physical buttons or Web interface.

## Features
- 2 Candle lighting sequences using physical byttons.
- Turn candles light on/off from Web interface.
- Candle lighting sequence from Web interface.
- Candle lighting sequence and play the blessing from Web interface.

## Components and Frameworks used in HanuPI
* [Loguru](https://pypi.org/project/loguru/)
* [Numpy](https://pypi.org/project/numpy/)
* [Requests ](https://pypi.org/project/requests/)
* [uvicorn](https://pypi.org/project/uvicorn/)
* [FastAPI](https://pypi.org/project/fastapi/)
* [Jinja](https://pypi.org/project/Jinja/)
* [sounddevice](https://pypi.org/project/sounddevice/)
* [soundfile](https://pypi.org/project/soundfile/)

## Parts used in HanuPI
* [Raspberry Pi 3]()
* [Raycare 12PCS LED Flameless Taper Candle Lights](https://www.amazon.com/dp/B07DFF3R8K?ref=ppx_yo2ov_dt_b_product_details&th=1)
* [Jumper Wires](https://www.aliexpress.com/item/1899750504.html?spm=a2g0o.order_list.order_list_main.16.63d65e5bOCOYlb)
* [Mini Round Momentary Push Button Switch](https://www.aliexpress.com/item/1005003120023458.html)
* [PAM8403 Super mini digital power amplifier board](https://www.aliexpress.com/item/32846373616.html)
* [8ohms speaker]()

## Bringing it all together

[![Raspberry PI Pinout](https://github.com/t0mer/HanuPI/blob/main/images/rp_pinout.png?raw=true "Raspberry PI Pinout")](https://github.com/t0mer/HanuPI/blob/main/images/rp_pinout.png?raw=true "Raspberry PI Pinout")

### Connecting the candles (Ordering Right to Left)
* Candle1 to 29 (GPIO 12)
* Candle2 to 37 (GPIO 26)
* Candle3 to 11 (GPIO 17)
* Candle4 to 13 (GPIO 27)
* Shamash to 31 (GPIO 6)
* Candle5 to 15 (GPIO 22)
* Candle6 to 16 (GPIO 23)
* Candle7 to 22 (GPIO 25)
* Candle8 to 18 (GPIO 24)
All candles using common ground.

### Connecting the Buttons
* Button1 to 10 (GPIO UART0 RX)
* Button1 to 8 (GPIO UART0 TX)
Both buttons using common 3.3V (GPIO 1)

### Connecting The amplifier
* Ground
* 5.5V
* To the speaker
* Using small PL to the speaker output.