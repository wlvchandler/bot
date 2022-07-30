import os
import random
import requests
import twitchio
from twitchio.ext import commands, routines

import signal
import sys

BASE_URL='https://api.twitch.tv/helix/'

import asyncio

def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=os.environ['TOKEN'], prefix='!', initial_channels=['#jaahska'])
        
        
