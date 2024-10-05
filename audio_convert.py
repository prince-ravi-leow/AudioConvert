#!/usr/bin/env python3

import subprocess
from pathlib import Path
from tqdm import tqdm

codecExt = {
    'wave' : 'wav',
    'alac' : 'm4a',
    'aac' : 'm4a'
}

ext_lower = "mp3 wav m4a opus wma flac mp4 opus ogg aiff webm ape".split()
ext_upper = [x.upper() for x in ext_lower]
valid_ext = ext_lower + ext_upper

ffmpeg_base = ["ffmpeg", "-y", "-i"]
not_verbose = ["-hide_banner", "-loglevel", "error"]

class AudioConvert:
    """
    Provide:
    - Input directory
    - Output codec
    """
    def __init__(self, output_codec, input_type = "dir", output_dir=None):
        self.output_codec = output_codec
        self.input_type = input_type
        self.output_dir = output_dir

    def get_dir_files(self, input_dir):
        if not Path(input_dir).is_dir():
            raise TypeError(f"{input_dir} not directory.")
        self.input_dir = Path(input_dir) if not input_dir == "." else Path(".").cwd() # Deal "." as input directory
        
        output_dir_name = self.input_dir.name.replace(" ", "_") + "_converted_" + f"{self.output_codec}"
        if not self.output_dir:
            self.output_dir = Path(input_dir) / output_dir_name
        self.output_dir.mkdir(exist_ok=True)
        
        self.input_files = [x for x in sorted(Path(self.input_dir).glob("*")) if str(x).split(".")[-1] in valid_ext]
    
    def get_list_files(self, input_files):
        if not isinstance(input_files, list):
            raise TypeError("Please enter list of files.")
        for f in input_files:
            if not Path(f).is_file():
                raise TypeError("Please enter list of files.")
        self.input_files = input_files
        if not self.output_dir:
            self.output_dir = Path(".").cwd()

    def convert(self, input_data):
        if self.input_type == "dir":
            self.get_dir_files(input_data)
        if self.input_type == "files":
            self.get_list_files(input_data)
        
        pbar = tqdm(self.input_files)
        for f in pbar:
            pbar.set_description(f"{f.parent} | {f.name}")
            ext = codecExt.get(f.suffix) if self.output_codec in codecExt.keys() else self.output_codec # Deal with codec not matching file extension
            output_filename = f.stem + "." + ext
            args = [
                "-acodec",
                self.output_codec,
                "-c:v",
                "copy"
                ]
            subprocess.run(
                ffmpeg_base + [str(f)] + args + not_verbose + [str(self.output_dir / output_filename)]
                )

if __name__ == "__main__":
    
    import sys
    from argparse import ArgumentParser
    
    parser = ArgumentParser(description = "Simple example: python3 audio_convert.py 'HOME - Odyssey (2014)/' 'mp3'")
    
    parser.add_argument(dest="input_directory", type=str, help="Input directory")
    parser.add_argument(dest="output_codec", type=str, help="Output codec")
    
    args = parser.parse_args()
    input_directory = args.input_directory
    output_codec = args.output_codec
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    c = AudioConvert(output_codec)
    c.convert(input_data=input_directory)
