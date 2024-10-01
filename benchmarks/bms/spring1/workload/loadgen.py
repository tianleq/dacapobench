#!/usr/bin/env python3

import os.path
import sys
from zipfile import ZipFile
from pathlib import Path

max_requests = 2048

src_files = []

def unzip_src_files(src, dest):

    with ZipFile(os.path.join(src, "src.zip"), "r") as file:
        for info in file.filelist:
            filename = info.filename
            if not filename.startswith("java.base"):
                continue
            src_files.append(filename)

            output_path = Path(os.path.join(dest, "src-files", filename)).resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with file.open(filename, "r") as input, open(output_path, "wb") as output:

                output.write(input.read())



def generate_workload(dest):
    dummy_digest = "     0 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX "
    with open(os.path.join(dest, "requests.list"), "w") as requests, open(os.path.join(dest, "source.list"), "w") as src:
        for file in src_files[:max_requests]:
            print(f"{dummy_digest}G/compile?file={file}", file=requests)
            p = Path(os.path.join(dest, "src-files", file)).resolve()
            print(f"{p}", file = src)



if __name__ == "__main__":
    args = sys.argv[1:]
    src, dest  = args[0], args[1]
    unzip_src_files(src, dest)
    # generate_workload(dest)