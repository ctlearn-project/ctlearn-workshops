#!/usr/bin/env python

import argparse
import logging
import glob
import os
import re
import time
import subprocess as sp
import numpy as np

def main():

    parser = argparse.ArgumentParser(
        description=("Script to run ctapipe-merge tool with DL1 hdf5 files"))
    parser.add_argument('--input_dir', '-i',
                        help='input directory',
                        default="./")
    parser.add_argument('--pattern', '-p',
                        help='pattern to mask unwanted files',
                        default="*.h5")
    parser.add_argument('--type',
                        help='particle type',
                        default="gamma")
    parser.add_argument('--num_outputfiles', '-n',
                        help='number of output files',
                        default=2,
                        type=int)
    parser.add_argument('--output_dir', '-o',
                        help='output directory',
                        default="./")

    args = parser.parse_args()

    # Input handling
    abs_file_dir = os.path.abspath(args.input_dir)
    input = np.sort(glob.glob(os.path.join(abs_file_dir, args.pattern)))

    run_numbers = []
    for file in input:
        run_numbers.append([int(s) for s in re.findall(r'\d+', file.split("/")[-1])][-4])
    run_numbers = np.sort(run_numbers)

    for runs in np.array_split(run_numbers, args.num_outputfiles):
        output_file = f"{args.output_dir}/{args.type}_theta_16.087_az_108.090_runs{runs[0]}-{runs[-1]}.r1.dl1.h5"
        print(f"Outputfile: '{output_file}'")
        cmd = [
             "sbatch",
             "-A",
             "aswg",
             #"--partition=long",
             "--partition=short",
             "--mem-per-cpu=32G",
             f"ctapipe-merge",
             "--overwrite",
             "--MergeTool.skip_broken_files=True",
             f"--output={output_file}",
            ]
        for run in runs:
            cmd.append(f"{abs_file_dir}/{args.type}_theta_16.087_az_108.090_run{run}.r1.dl1.h5")
        sp.run(cmd)

    return

if __name__ == "__main__":
    main()

