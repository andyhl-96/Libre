import discord
import datetime
import random
import discord.ext.commands as commands
from pytubefix import YouTube
from pydub import AudioSegment

token = open("../libre_token", "r").readline()
id = "1136776729441095720"
poll_active = False
f = open("./parable.txt", "r")
lines = f.readlines() # lines to say
f.close()
voice_client = None

bot = commands.Bot(command_prefix='%', intents = discord.Intents.all())

@bot.command(brief = "Shows all the commands")
async def helppls(ctx):
    cmds = bot.commands
    await ctx.send("# Commands: ")
    for cmd in cmds:
        await ctx.send(">>> %" + cmd.name)
        if cmd.brief != None:
            await ctx.send(cmd.brief)

@bot.command(brief = "Exile a user for being bad")
async def exile(ctx, p_id, reason):
    guild = ctx.guild
    user = await bot.fetch_user(p_id[2:len(p_id) - 1])
    await guild.kick(user)
    await ctx.send(user.name + " has been exiled for the reasons following: \n>>> " + reason)

@bot.command()
async def bruh(ctx):
    await ctx.send("@everyone")

@bot.command()
async def lpoll(interaction, p_name: str, desc: str, *args):
    options = args
    for o in options:
        if o == "-1":
            options.remove(o)
    msg = await interaction.send("@everyone \n" + "# Poll: " + p_name + "\n>>> " + desc)
    for o in options:
        await msg.add_reaction(o)
        await msg.pin()

@bot.command()
async def echo(ctx, msg):
    await ctx.send(msg)

@bot.command()
async def pwd(ctx):
    guild = ctx.guild
    channel = ctx.channel
    await ctx.send("/" + guild.name + "/" + channel.name + "/")

@bot.command()
async def ls(ctx):
    users = ctx.channel.members
    for u in users:
        await ctx.send(u.name)
# Helper function: Get or create "Muted" role
async def get_muted_role(guild):
    muted_role = discord.utils.get(guild.roles, name="Muted")
    if not muted_role:
        # Create "Muted" role if it doesn't exist
        muted_role = await guild.create_role(
            name="Muted",
            permissions=discord.Permissions(send_messages=False, speak=False),
            reason="Role for muting users"
        )
        # Apply the role to all channels in the guild
        for channel in guild.channels:
            await channel.set_permissions(muted_role, send_messages=False, speak=False)
    return muted_role

# Command: Mute a user
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    muted_role = await get_muted_role(ctx.guild)
    if muted_role in member.roles:
        await ctx.send(f"{member.mention} is already muted.")
    else:
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"{member.mention} has been muted. Reason: {reason}")

# Command: Unmute a user
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    muted_role = await get_muted_role(ctx.guild)
    if muted_role not in member.roles:
        await ctx.send(f"{member.mention} is not muted.")
    else:
        await member.remove_roles(muted_role, reason="Unmuted by command")
        await ctx.send(f"{member.mention} has been unmuted.")

@bot.command()
async def joinvc(ctx):
    global voice_client
    vc = ctx.author.voice
    if vc == None:
        return
    voice_client = await vc.channel.connect()

@bot.command()
async def quitvc(ctx):
    global voice_client
    vc = ctx.author.voice
    if vc == None:
        return
    await voice_client.disconnect()

@bot.command()
async def play(ctx, link):
    global voice_client
    vid = YouTube(link)
    stream = vid.streams.filter(only_audio=True).first()
    stream.download(filename="temp")
    audio = AudioSegment.from_file("temp.m4a", format="m4a")
    audio.export("temp.mp3", format="mp3")
    voice_client.play(discord.FFmpegPCMAudio("temp.mp3"))

@bot.command()
async def ship(ctx, m1, m2):
    user1 = await bot.fetch_user(m1[2:len(m1) - 1])
    user2 = await bot.fetch_user(m2[2:len(m2) - 1])
    await ctx.send("## Ship " + user1.name + " and " + user2.name + ":")
    comp = random.random() * 100
    await ctx.send(">> Compatibility: " + str(comp))
    if comp > 50:
        await ctx.send("I ship it")
    else:
        await ctx.send("I do not ship it.")


@bot.event
async def on_ready():
    bot.get_guild
    activities = ["with balls", "stupid games", "with the homies", "the stanley parable"]
    rand = random.randint(0, len(activities) - 1)
    activity = discord.Activity(name = activities[rand], 
            type = discord.ActivityType.playing,
            start = datetime.datetime(69, 6, 9))
    await bot.change_presence(status = discord.Status.online, activity = activity)
    print(bot.user.name + " connected")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if len(message.content) == 0:
        return
    if message.content[0] == "%":
       return
    if message.author == bot.user:
      return
    else:
      if message.author.name == "icrowave":
        await message.channel.send("didnt ask")
      elif message.author.name != "Rin":
        rand = random.randint(0, len(lines) - 1)
        await message.channel.send(lines[rand])

@bot.event
async def on_member_join(member):
    welcome = bot.get_channel(1094772293005225984)
    await welcome.send("Ah, greetings fellow gangster, and welcome, " + member.name)
    await welcome.send("Feel free to hit #introductions to tell us about yourself.")
    await welcome.send("And or #hierarchy to get some goofy ahh roles.")

bot.run(token)

