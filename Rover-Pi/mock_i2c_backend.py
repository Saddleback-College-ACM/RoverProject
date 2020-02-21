#!/usr/bin/env python3
from __future__ import print_function
import socket
import sys
import os

class PyCar:
    def __init__(self):
        pass

    def control(self, steering, throttle):      
        print('Steering: {}\tThrottle: {}'.format(steering, throttle))

if __name__ == '__main__':
    car = PyCar()
    car.control(90, 90)

