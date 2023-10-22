# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API
# IMPORT MYSQL.CONECTOR. ALLOWS ACCESS TO MYSQL SERVER
import discord
import mysql.connector

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# GETS THE FILE WITH ALL PRIVATE INFORMATION
secret = open("secret.txt").readlines()

# CONNECTS TO MYSQL SERVER
connection = mysql.connector.connect(host=secret[1],
                                        database=secret[2],
                                        user=secret[3],
                                        password=secret[4])
print(connection)

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE
@bot.event
async def on_ready():
	# CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS THE BOT IS CONNECTED TO
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILDS THAT THE BOT IS ASSOCIATED WITH
	for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS THE BOT IS IN
	print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL
@bot.event
async def on_message(message):
    # CHECKS IF THE MESSAGE THAT WAS SENT MATCHES STARTING COMMAND
	if message.content == ('quote this'):
		# GETS ALL MESSAGE DATA
		channel = message.channel
		msg = await channel.fetch_message(message.reference.message_id)

		# SET OF VARIABLES NEEDED TO SHOW RESPONSE
		content = msg.content
		time = msg.created_at
		user_id = msg.author.id
		user = await bot.fetch_user(user_id)

		# PRINTS OUT INFORMATION ABOUT THE MESSAGE
		embed=discord.Embed(title=content, 
					  description='Uttered by %s' % user.display_name,
					  timestamp=time,
					  colour=discord.Colour.gold())
		embed.set_thumbnail(url=user.display_avatar)
		await channel.send(embed=embed)
		
		# CREATES A CURSOR THAT INTERACTS WITH THE MYSQL DATABASE
		cursor = connection.cursor()
		
		# CREATES A UNIQUE ID FOR NEW MESSAGE
		cursor.execute("SELECT MAX(id) FROM messages")
		id = cursor.fetchone()[0]+1

		# ADDS THE INFORMATION ABOUT THE MESSAGE TO THE MYSQL DATABASE
		sql = "INSERT INTO messages (id, message_content, user_id, date_sent) VALUES (%s, %s, %s, %s)"
		val = (id, content, user_id, time)
		cursor.execute(sql, val)
		connection.commit()

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN
bot.run(secret[0])