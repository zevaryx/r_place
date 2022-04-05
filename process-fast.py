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
scale = config["scale"]

inp = "img" + sep
outp = "output" + sep


def resize(image):
    im = Image.open(image)
    im = im.crop(tuple(box))
    im = im.resize((im.width * scale, im.height * scale), resample=Image.Resampling.BOX)
    return im


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

    images = process_map(resize, images, max_workers=threads, unit="im",
                         desc="Creating timelapse", chunksize=1)
    images[0].save(final, append_images=images, save_all=True, optimize=False)
