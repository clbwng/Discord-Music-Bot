//MUSIC PLAYING DISCORD BOT
//HACK THE NORTH 2021 SUBMISSION

import discord
import youtube_dl
from discord.ext import commands
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from discord.utils import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
import time
import pafy
import asyncio

TOKEN = "ODg4NjM2MzM1NTE3MjI1MDIw.YUVlFA.4D0wHxDlwLGbh2l8nHG_II2BtXU"

client = commands.Bot(command_prefix = ".")

players = {}
global song_list
song_list = []

@client.event
async def on_ready():
    print("bot ready")

@client.command(pass_context=True)
async def join(ctx):
    print(ctx.message.author.voice)
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(pass_context=True)
async def leave(ctx):
    #server = ctx.message.guild.voice_clients[0]
    
    print(ctx.message.guild)
    await ctx.voice_client.disconnect()

@client.command(pass_context=True)
async def queue(ctx, num):
    song_queue = []
    for i in range (0,int(num)):
        try:
            song_queue.append(get_youtube_url(song_list[i]))
        except:
            song_queue.append(get_youtube_url(song_list[29-i]))
    for url in song_queue:
        await play_song(ctx, url)



@client.command(pass_context=True)
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command(pass_context=True)
async def play(ctx, *args):
    print("song playing")
    global song_list
    song_list = []

    user_input = ' '.join(args)
    url = get_youtube_url(user_input)
    

    user_list = user_input.split(',')
    song = user_list[0]
    artist = user_list[1][1:]
    
    try:
        song_list += find_by_key(song, artist)
        print(song_list)
    except:
        await ctx.send("We couldn't find matches for your song bro :(")
    await play_song(ctx, url)

async def play_song(ctx, url):

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing() 
        video = pafy.new(url)
        await asyncio.sleep(video.length)
    else:
        await ctx.send("Already playing song")
        return


op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome('/Users/clbwn/OneDrive/Desktop/chromedriver', options=op)    


def find_by_key(song, artist):
    songs_in_key = []

    driver.get('https://www.songkeyfinder.com/')

    search_artist = driver.find_element_by_xpath('//*[@id="topbar"]/form/input[1]')
    search_song = driver.find_element_by_xpath('//*[@id="topbar"]/form/input[2]')

    search_artist.send_keys(artist)
    search_song.send_keys(song)
    search_song.send_keys(Keys.ENTER)

    driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[2]/td[2]/a').click()
    song_key = driver.find_element_by_xpath('//*[@id="content"]/h2[2]/span[1]')
    key = song_key.text
    key = key[7:]

    driver.find_element_by_partial_link_text("Songs by Key").click()
    driver.find_element_by_partial_link_text(key).click()

    table = driver.find_element_by_xpath('//*[@id="content"]/table/tbody')

    for row in table.find_elements_by_css_selector('tr'):
        songs_in_key.append(row.text[:-5])
    songs_in_key = songs_in_key[1:]
    random.shuffle(songs_in_key)
    return songs_in_key
    

def get_youtube_url(song):
    driver.get('https://www.google.com/')
    search_bar = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    
    search_bar.send_keys(song)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(1)

    url = driver.find_element_by_css_selector('div.twQ0Be > a').get_attribute('href')
    return url

client.run(TOKEN)
