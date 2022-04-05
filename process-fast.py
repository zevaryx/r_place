import json
from glob import glob
from multiprocessing import cpu_count
from os import mkdir, path, sep, unlink

from PIL import Image
from tqdm.contrib.concurrent import process_map

if not path.exists("config.json"):
    print("Please copy `config.example.json` to `config.json` and edit it with what you need")
    exit(1)

with open("config.json") as f:
    config = json.load(f)

threads = max(cpu_count() - 2, 1)

box = config["top_left"] + config["bottom_right"]
width = config["bottom_right"][0] - config["top_left"][0]
height = config["bottom_right"][1] - config["top_left"][1]

scale = config.get("scale", 1)
frameskip = config.get("frameskip", 1)
fps = config.get("fps", 50)
name = config.get("name", "timelapse")

frametime = 1000 / fps

inp = "img" + sep
outp = "output" + sep


def resize(image):
    im = Image.open(image).crop(tuple(box)).resize(
        (width * scale, height * scale), resample=Image.Resampling.BOX)
    extrema = im.convert("L").getextrema()
    if extrema in [(0, 0), (1, 1)]:
        return None
    return im


if __name__ == "__main__":
    if not path.exists(outp):
        mkdir(outp)

    if not path.exists(inp):
        print("Please download https://zevs.me/rplace_archive.7z and extract it to img/")
        exit(1)

    images = sorted(glob(inp + "*.png"))
    final = outp + f"{name}.gif"
    if path.exists(final):
        unlink(final)

    images = process_map(resize, images[::frameskip], max_workers=threads, unit="im",
                         desc="Creating timelapse", chunksize=1)
    images = [x for x in images if x]
    images[0].save(final, append_images=images[1:], save_all=True,
                   optimize=False, duration=frametime)
