import json
from glob import glob
from os import mkdir, path, sep
from multiprocessing import Pool, cpu_count

from PIL import Image
from tqdm import tqdm

threads = cpu_count() - 2

if not path.exists("config.json"):
    print("Please copy `config.example.json` to `config.json` and edit it with what you need")
    exit(1)

with open("config.json") as f:
    config = json.load(f)

box = config["top_left"] + config["bottom_right"]
scale = config["scale"]

inp = "img" + sep
outp = "output" + sep


def chunk(lst, n):
    for i in range(0, n):
        yield lst[i::n]


def crop(index, images):
    crops = []
    for p in tqdm(images, unit="im", position=index):
        im = Image.open(p)
        cropped = im.crop(tuple(box))
        cropped = cropped.resize((cropped.width * scale, cropped.height * scale),
                                 resample=Image.Resampling.BOX)
        crops.append(cropped)
    return crops


def crop_unpack(args):
    return crop(*args)


if __name__ == "__main__":
    if not path.exists(outp):
        mkdir(outp)

    if not path.exists(inp):
        print("Please download https://zevs.me/rplace_archive.7z and extract it to img/")
        exit(1)

    images = sorted(glob(inp + "*.png"))

    args = [(i, c) for i, c in enumerate(chunk(images, threads))]
    with Pool(threads) as pool:
        crops = pool.map(crop_unpack, args)

    frames = []
    for c in crops:
        frames += c

    frames[0].save(outp + "timelapse.gif", append_images=frames[1:], save_all=True, optimize=False)
