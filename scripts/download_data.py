"""Download the lecture 1 images to ~/cdb560-data/pERK (outside the repo)."""
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve
from zipfile import ZipFile
import shutil
import sys

import tifffile

DATA_DIR = Path.home() / "cdb560-data" / "pERK"
SAMPLES = [(1, 0), (2, 6), (3, 9), (4, 12), (5, 16), (6, 20), (7, 24), (8, 28)]
ARCHIVES = {
    0: "1MfnxSUgZAaqxQ0aYV5nVNHx5orbFeXsb",
    1: "1MhRNaJ2QpV5_AUUa3yC2ljanYGeTelO7",
}


def valid_image(path):
    try:
        image = tifffile.imread(path)
        return image.shape == (1024, 1024) and image.dtype.name == "uint16"
    except Exception:
        return False


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for channel, file_id in ARCHIVES.items():
        filenames = [
            f"A{well}_200819_ppERK_timeseries_E6T_MIP_p{position:04d}_w{channel:04d}.tif"
            for well, position in SAMPLES
        ]
        missing = [name for name in filenames if not valid_image(DATA_DIR / name)]
        if not missing:
            print(f"Channel {channel}: all 8 images are already ready. Skipping.", flush=True)
            continue
        print(f"Downloading {'nuclear' if channel == 0 else 'pERK'} images...", flush=True)
        # Temporary downloads stay outside the repo and are removed even on failure.
        with TemporaryDirectory(dir=DATA_DIR) as temporary:
            archive = Path(temporary) / "images.zip"
            urlretrieve(f"https://drive.google.com/uc?export=download&id={file_id}", archive)
            with ZipFile(archive) as zipped:
                for name in missing:
                    members = [entry for entry in zipped.infolist()
                               if Path(entry.filename).name == name
                               and "__MACOSX" not in Path(entry.filename).parts]
                    if len(members) != 1:
                        raise ValueError(f"The download does not contain exactly one copy of {name}.")
                    staged = Path(temporary) / name
                    # Copy only expected images; never extract arbitrary archive paths.
                    with zipped.open(members[0]) as source, staged.open("wb") as target:
                        shutil.copyfileobj(source, target)
                    if not valid_image(staged):
                        raise ValueError(f"The downloaded image {name} could not be read correctly.")
                    staged.replace(DATA_DIR / name)
        print(f"Channel {channel}: all 8 images are ready.", flush=True)
    print(f"Images are saved in {DATA_DIR}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("The image download could not finish. Check your internet connection and "
              "run setup.sh again. If it still fails, ask a TA.", file=sys.stderr)
        print(f"Details for your TA: {error}", file=sys.stderr)
        sys.exit(1)
