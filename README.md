# r_place

An r/place timelapse generator

## Instructions

1. [Install Python](https://python.org)
2. Save this script somewhere safe (or `git clone`)
3. [Download my archive](https://zevs.me/rplace_archive.7z) and extract it to `img/`
4. Copy `config.example.json` to `config.json` and modify it to match what you need
5. Open Command Prompt/Powershell/Terminal and run the following:
```sh
cd path/from/step2
pip install -U -r requirements.txt
# For high speed and high resource usage
python process-fast.py
# For low speed and low resource usage
python process-slow.py
```

`process-fast.py` ***will use*** a lot of resources, both CPU and RAM. If you have a low amount of both, use `process-slow.py`

## Configuration Options

| Option | Description | Required | Default |
|--------|-------------|----------|---------|
| `top_left` | Top left pixel of bounding box | Yes | |
| `bottom_right` | Bottom right pixel of bounding box | Yes | |
| `scale` | Resolution scaling factor | No | 1 |
| `frameskip` | Skip `n` images between frames, 1 to not skip | No | 1 |
| `fps` | Target fps | No | 50 |

## **WARNING**
Running `process-fast.py` script on a large area with a high scale ***will crash either the program or your computer***

To generate highly upscaled versions of timelapses, please use `process-slow.py`

This program comes with no warranty or guarantees. Use at your own risk.
