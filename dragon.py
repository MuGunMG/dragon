import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import youtube_dl
import re
import json
import os.path

FILENAME = 'data.json'



MAX_WORDS = 100

client = commands.Bot(command_prefix='.')
client.remove_command('help')

def load_words(filename):
    if not os.path.isfile(filename):
        return {}

    with open(filename, encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    return data

def save_words(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

    return True



data = load_words(FILENAME)

@client.event
async def on_message(message):
    args = message.content.split()

    # 봇이 채팅 치면 skip
    if message.author == client.user:
        return

    prefix = args[0]

    if prefix != "용용님":
        return

    command = args[1] if len(args) > 1 else []
    parameters = args[2:] if len(args) > 2 else []

    if not command:
        e = discord.Embed(title="왜불러?", colour=0x00FF15)
        await client.send_message(message.channel, embed=e)

    elif command == "개발자":
        em = discord.Embed(title="개발자는 무군MG#9978 입니다!", colour=0x000000)
        em.add_field(name="공동 개발자를 구합니다!", value="무군MG#9978로 문의주세요")
        await client.send_message(message.channel, embed=em)
        return
    
    elif command == "업뎃":
        em = discord.Embed(title="용용봇 1.1 업데이트", colour=0x000000)
        em.set_author(name="용용봇 패치 내역")
        em.add_field(name="저작권 관련 문제", value="디스코드 봇의 프로필에 이용된 그림이 저작권 문제로 인하여 일시적으로 내려갔습니다",inline=False)
        await client.send_message(message.channel, embed=em)

    elif command == "안녕?":
        em = discord.Embed(title="안녕?", colour=0x000000)
        em.add_field(name="공동 개발자를 구합니다!", value="무군MG#9978로 문의주세요")
        await client.send_message(message.channel, embed=em)
        return

    elif command == "초대":
        em = discord.Embed(title="여기를 클릭해 주세요", url="https://discord.com/oauth2/authorize?client_id=714068824533499984&permissions=3468352&scope=bot", colour=0x000000)
        await client.send_message(message.channel, embed=em)
        return

    elif command == "도움":
        aem = discord.Embed(title="도움말",description="명령어 목록", colour=0x00FF15)
        aem.set_author(name="용용봇 도움말")
        aem.add_field(name="용용님 안녕?",value="용용봇에게 인사합니다", inline=False)
        aem.add_field(name="용용님 배워 <단어> <내용>",value="용용봇을 가르칩니다\n이미 알고있는 내용은 새로 배운 내용으로대채됩니다", inline=False)
        aem.add_field(name="용용님 잊어 <단어>",value="용용봇에게 가르친 단어를 잊게 합니다",inline=False)
        aem.add_field(name="용용님 <단어>",value="용용봇에게 가르친 단어를 물어봅니다",inline=False)
        aem.add_field(name="용용님 초대",value="용용봇 초대링크를 받습니다",inline=False)
        aem.add_field(name="용용님 개발자",value="용용봇 개발자를 알아냅니다",inline=False)
        aem.add_field(name="용용님 업뎃",value="용용봇 업데이트 내역을 봅니다",inline=False)
        await client.send_message(message.channel, embed=aem)
        return

    elif command == "배워":
        if len(data) >= MAX_WORDS:
            one = discord.Embed(title="너무 많은걸 외웠어 더이상은 나도 무리야", colour=0x00FF15)
            await client.send_message(message.channel, embed=one)
            return

        if len(parameters) < 2:
            one = discord.Embed(title="뭘 배우라는거야? 똑바로 알려줘", colour=0x00FF15)
            await client.send_message(message.channel, embed=one)
            return

        word, text = parameters[0], ' '.join(parameters[1:])

        if word in data:
            one = discord.Embed(title="이미 {}(이)라고 배웠지만 바꿔줄게!".format(data[word]), colour=0x00FF15)
            await client.send_message(message.channel, embed=one)
        else:
            one = discord.Embed(title="알았어 기억해보도록 노력할게!", colour=0x00FF15)
            await client.send_message(message.channel, embed=one)
        
        data[word] = text
        
        
        
        save_words(data, FILENAME)
        return

    elif command == "잊어":

        if not parameters:
            dus = discord.Embed(title="뭘 잊으라는거야...", colour=0x00FF15)
            await client.send_message(message.channel, embed=dus)
            return

        word = parameters[0]

        if word not in data:
            f = discord.Embed(title="애초에 그런 단어는 몰랐는걸?", colour=0x00FF15)
            await client.send_message(message.channel, embed=f)
            return

        del data[word]
        s = discord.Embed(title="{}을(를) 잊어버렸어 외우라고 했다가 잊어버리라니 너무하네" .format(word), colour=0x00FF15)
        await client.send_message(message.channel, embed=s)

        save_words(data, FILENAME)
        return



    else:
        word = command

        if word not in data:
            a = discord.Embed(title="뭐라는거야? 그건 내가 모르는거야.", colour=0x00FF15)
            await client.send_message(message.channel, embed=a)
            return
        
        else:
            aaem = discord.Embed(title=data[word], colour=0x00FF15)
            await client.send_message(message.channel, embed=aaem)
            return




@client.event
async def on_ready():
    print("다음으로 로그인합니다 : ")
    print(client.user.name)
    print(client.user.id)
    print("==========")
    await client.change_presence(game=discord.Game(name="도움말은 '용용님 도움'을 입력해!", type=1))


access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
