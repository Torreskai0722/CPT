#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-

#with open('access_usbcam_raw.log') as f:
with open('access_usbcam_cvbridge.log') as f:
    lines = f.readlines()
    dict = {}
    for key in lines:
        dict[key] = dict.get(key, 0) + 1
    print(dict)
