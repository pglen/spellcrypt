#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string
from datetime import date

import spemod

#bigarr = []
#boundsig = []
#boundstr = []
#boundarr = []

# Start of program:

if __name__ == '__main__':


    spemod.init()

    #print("interpret" , "'" + sys.argv[1] + "'" );
    arr = sys.argv[1].split()
    ''' xx in range(len(arr) / 2):
        xxx = arr[xx * 2]; yyy =  arr[xx * 2 + 1]
        print (spemod.revwcoord (int(xxx), int(yyy)), end = " ")'''

    for xx in range(len(arr)):
        print (spemod.revword (int(arr[xx])), end = " ")

    print("")


