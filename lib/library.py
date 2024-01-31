# Telethon-related imports
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import (
    User,
    InputPhoto,
    DocumentAttributeFilename,
    UserStatusOnline,
    UserStatusOffline,
)
from telethon import functions
from telethon.tl import functions, types
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeFilename
from telethon import types

# External libraries
import asyncio
import datetime
import psutil
import requests
import urllib.request
import os
import time
import sys
import re
import random
import wikipedia
import pytz
import spotipy
import io
import secrets
import string
import json
import whois
import shutil
import zipfile
import jdatetime
import qrcode
import aiohttp
from math import ceil
from yt_dlp import YoutubeDL
from spotipy.oauth2 import SpotifyClientCredentials
from googlesearch import search
from googletrans import LANGUAGES, Translator
from bs4 import BeautifulSoup
from persiantools.jdatetime import JalaliDate
from io import BytesIO
from PIL import Image
from gtts import gTTS
from pytube import YouTube
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder