import json
from glob import glob
from os import mkdir, path, sep, unlink

import imageio
import numpy as np
from PIL import Image
from tqdm import tqdm

if not path.exists("config.json"):
    print("Please copy `config.example.json` to `config.json` and edit it with what you need")
    exit(1)

with open("config.json") as f:
    config = json.load(f)

box = config["top_left"] + config["bottom_right"]
width = config["bottom_right"][0] - config["top_left"][0]
height = config["bottom_right"][1] - config["top_left"][1]

scale = config.get("scale", 1)
frameskip = config.get("frameskip", 1)
fps = config.get("fps", 50)

frametime = 1000 / fps

inp = "img" + sep
outp = "output" + sep

if __name__ == "__main__":
    if not path.exists(outp):
        mkdir(outp)

    if not path.exists(inp):
        print("Please download https://zevs.me/rplace_archive.7z and extract it to img/")
        exit(1)

    images = sorted(glob(inp + "*.png"))
    final = outp + "timelapse.gif"
    if path.exists(final):
        unlink(final)

    with imageio.get_writer(final, mode="I", fps=fps) as writer:
        for fname in tqdm(images[::frameskip], unit="im", desc="Creating timelapse"):
            image = imageio.imread(fname)
            im = Image.fromarray(image).crop(tuple(box)).resize(
                (width * scale, height * scale), resample=Image.Resampling.BOX)
            image = np.array(im)
            writer.append_data(image)
