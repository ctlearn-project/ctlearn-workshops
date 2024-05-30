#!/usr/bin/env python

import argparse
import logging
import glob
import os
import subprocess as sp
import numpy as np


def main():

    parser = argparse.ArgumentParser(
        description=("Script to run reduction from simtel files to DL1 hdf5 files with the ctapipe-process tool"))
    parser.add_argument('--input_dir', '-i',
                        help='input directory',
                        default="./")
    parser.add_argument('--pattern', '-p',
                        help='pattern to mask unwanted files',
                        default="*")
    parser.add_argument('--type',
                        help='particle type',
                        default="gamma")
    parser.add_argument('--config', '-c',
                        help='ctapipe config file',
                        default="/fefs/aswg/workspace/tjark.miener/ctlearn_workshop2024/configs/ctapipe_standard_LST1_config.json")
    parser.add_argument('--output_dir', '-o',
                        help='output directory',
                        default="./")

    args = parser.parse_args()

    # Input handling
    abs_file_dir = os.path.abspath(args.input_dir)
    files = np.sort(glob.glob(os.path.join(abs_file_dir, args.pattern)))

    for file in files:
        print(f"Inputfile: '{file}'")
        output_file = f"{args.output_dir}/{file.split('/')[-1].replace('simtel_corsika', f'{args.type}').replace('simtel.gz', 'r1.dl1.h5')}"
        print(f"Outputfile: '{output_file}'")
        cmd = [
             f"ctapipe-process",
             "-t 1",
             "--overwrite",
             f"--input={file}",
             f"--output={output_file}",
             f"--config={args.config}",
             "--write-images",
             "--write-parameters",
             f"--DataWriter.write_waveforms=True",
             "--log-level=ERROR"
            ]
        sp.run(cmd)
    return        

if __name__ == "__main__":
    main()

