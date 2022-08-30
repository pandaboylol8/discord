import discord
from discord.ext import commands
import os
import random
import openai
import sys
import time



#uncomment when you want to keep running 24/
client = commands.Bot(command_prefix = '$')

intro1 = """Please input the characteristics for the bot here. It should follow the structure: The bot [insert characteristics here]. For example, you could do: "is very kind and intellegent" or: "is Elon Musk" """
# @client.event
# async def on_message(ctx):
#   print(f"{ctx.author} said '{ctx.content}' in {ctx.channel} channel")
#   # message = input("message: ")
@client.event
async def on_ready():
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print('------')
  print("Bot is ready.")
  await client.change_presence(activity=discord.Game(name="Listening for '$chat'!"))
@client.command()
async def bitches(ctx):
  print(ctx.author.id)
  string = int(ctx.author.id)
  if string % 2 == 0:
    await ctx.send("YOU GET BITCHES :eggplant:")
  else:
    await ctx.send("YOU GET NO BITCHES")



@client.command()
async def ping(ctx):
  await ctx.send(f"Pong! latency is {round(client.latency*1000)}ms")

@client.command()
async def start(ctx):
  await ctx.send("Welcome to Chatbot by Nicholas Son. To get started, you can try the commands: $8ball [insert question here], $ping, or $chat")

@client.command(aliases=['8ball','test'])
async def _8ball(ctx, *, question):
  responses = ["It is certian.",
              "It is decidedly so.",
              "OFC",
              "no",
              "maybe?",
              "DEFINETLY NOT :rofl:",
              "I dont know man",
              "naww",
              "i would say yes"]
  await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

@client.command()
async def chat(ctx):
    chatter = ctx.author
    await ctx.send("OpenAI Discord ChatBot by: Nicholas Son")
    await ctx.send("-"*15)
    await ctx.send(intro1)


    def check(m):
        return m.content.startswith('')

    msg = await client.wait_for("message", check=check)
    char = msg.content
    await ctx.send("-"*15)

    await ctx.send("The temperature of the AI will determine how random its answers are. A lower value will result in more deterministic and set responses.It MUST be a value between 0 and 1(Just do 1 if you dont know what it means.)")
    await ctx.send("Temperature:")
    def check(m):
        return m.content.startswith('')

    msg = await client.wait_for("message", check=check)
    temp = msg.content
    await ctx.send("-"*15)
    await ctx.send(f"The bot {char}\nTemperature: {temp}")
    await ctx.send("-"*15)
    context="The following is a back and forth conversation with an AI chatbot. The chatbot "+char+".\n\nHuman: Hello\n\n AI: Hello!\n\nHuman:"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    await ctx.send("Talk to the AI: (type: '!' at anytime to stop the chat)")
    while True:
      def check(m):
        return m.content.startswith('')
      msg = await client.wait_for("message", check=check)
      input = msg.content
      asker = msg.author
      if chatter == asker:
        pass
      else:
        continue
      if input == "":
        continue
      else:
        pass
      if msg.content == "!":
        await ctx.send("conversation closing...")
        time.sleep(2)
        await ctx.send("conversation closed.")
        break
      else:
        pass
      print(input)
      start_sequence = "\nAI:"
      restart_sequence = "\nHuman: "
      response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=context+input,
        temperature=float(temp),
        max_tokens=1500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
      )
      response = (response['choices'][0]['text'])
      # print(context)
      lines = response.split("\n")
      non_empty_lines = [line for line in lines if line.strip() != ""]
      
      response_without_empty_lines = ""
      for line in non_empty_lines:
            response_without_empty_lines += line + "\n"
      response = response_without_empty_lines
      print(response)
      try:
        await ctx.send(response)
      except:
        await ctx.send("Sorry, Ai was not able to process that. Please reword your sentence and try again.")   
        continue
      context = context+input +"\n\n"+response + "\n\nHuman: "
      
      

      
    

  

client.run(os.environ['TOKEN'])
