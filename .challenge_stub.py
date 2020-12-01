#!/usr/bin/env python3

import os
import sys
import traceback
import ipdb as pdb

from utils import *


def main():
    pass


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
