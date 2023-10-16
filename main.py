# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
	# CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS THE BOT IS CONNECTED TO.
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILDS THAT THE BOT IS ASSOCIATED WITH.
	for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS THE BOT IS IN.
	print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
    # CHECKS IF THE MESSAGE THAT WAS SENT MATCHES STARTING COMMAND.
	if message.content.startswith('test'):
		# GETS ALL MESSAGE DATA
		channel = message.channel
		msg = await channel.fetch_message(message.id)

		# SET OF VARIABLES NEEDED TO SHOW RESPONSE
		content = message.content
		time = str(msg.created_at)[:10]
		user = msg.author.id

		# PRINTS OUT INFORMATION ABOUT MESSAGE
		await channel.send(str((await bot.fetch_user(user)).display_name) + 
					 " said \"" + content + 
					 "\" at " + time)

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN IS HIDDEN IN FILE FOR PRIVACY.
bot.run(open("token.txt", "r").read())