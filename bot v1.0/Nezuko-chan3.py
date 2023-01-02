import os
import discord
from discord import app_commands
from discord.ext import commands
import sql_commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()

TOKEN=os.getenv('TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '!', intents=intents)
tree = bot.tree


bankmanager = "BANK"#bank manager role
police = "police"#police role


LogChat = '1057410652517433444'#log chat ID



@bot.event
async def on_ready():
	print('Logged as {0.user}'.format(bot))
	
	try:
		synced = await tree.sync()
		print(f"Synced {len(synced)} command(s)")
	except Exception as e:
		print(e)




@tree.command(name = "createcard", description = "Створити новий баланс користувачу(Тільки для банкірів)") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.checks.has_role(bankmanager)
@app_commands.describe(discordtag = "Тегніть користувача якому створюється рахунок (приклад @RedInJector)", minecraft_name = "Введіть ігровий нік гравця")
async def createcard(interaction: discord.Interaction, discordtag:str, minecraft_name:str):
	logchannel = bot.get_channel(int(LogChat))
	discordid = discordtag.translate({ ord(c): None for c in "<!@>" })
	discordtag = bot.get_user(int(discordid)) 
	check = sql_commands.DataNewClient(discordtag, discordid, minecraft_name)
	#print(interaction.user)  --> returns user tag
	##print(interaction.user.id) --> returnns id
	if check:

		card_number = ""
		for i, c in enumerate(str(discordid)[2:]):
			if i > 0 and i % 4 == 0:
				card_number += " "
			card_number += c

		embed=discord.Embed(title= "Офіційний банк Аметісу", description = f"Вашу карту офіційно відкрито Банкіром <@{interaction.user.id}>\n\n Номер карти: **{card_number}**\n Термін дії до: **01/24**\n\nВаш баланс: **0 діамант(ів)**", color=0x6f12c0)
		pfp = interaction.user.avatar.url
		pfp2 = bot.get_user(int(discordid)).avatar.url
		embed.set_thumbnail(url=pfp)
		embed.set_footer(text=f"{discordtag}",icon_url=pfp2)
		dm = await discordtag.create_dm()  # Creates a dm channel with the user
		await dm.send(embed=embed)


		await interaction.response.send_message(f"Created balance **{card_number}** for player <@{discordid}>", ephemeral = True)
		await logchannel.send(f"Created balance {card_number} for player <@{discordtag}> nick: {minecraft_name}")
	else:
		await interaction.response.send_message(f"Card {discordid[2:]} for player <@{discordid}> already exists", ephemeral = True)
	return


@tree.command(name = "topup", description = "Покласти гроші на баланс користувача(тільки для банкірів)")
@app_commands.checks.has_role(bankmanager)
@app_commands.describe(discordtag = "Тегніть користувача якому діаманти кладуться на рахунок (приклад @maksutko)", amount = "Кількість діамантів, які кладуться на рахунок")
async def topup(interaction: discord.Interaction, discordtag:str, amount:int):
	logchannel = bot.get_channel(int(LogChat))
	discordid = discordtag.translate({ ord(c): None for c in "<!@>" })
	discordtag = bot.get_user(int(discordid))
	check1 = sql_commands.CheckIfExists(discordid)
	if check1:
		if amount >=1:
			sql_commands.add_money_WithDiscordID(discordid,amount)
			balanceinfo = sql_commands.BalanceWithDiscordID(discordid)
			dm = await discordtag.create_dm()  # Creates a dm channel with the user

			embed=discord.Embed(title= "Офіційний банк Аметісу", description = f"Банкір <@{interaction.user.id}> поповнив ваш баланс на **{amount}** діамант(ів).\n\nВаш баланс: **{balanceinfo} діамант(ів)**", color=0x6f12c0)
			pfp = bot.get_user(int(discordid)).avatar.url
			pfp2 = interaction.user.avatar.url
			embed.set_thumbnail(url=pfp2)
			embed.set_footer(text=f"{discordtag}", icon_url=pfp)
			await dm.send(embed=embed)

			await interaction.response.send_message(f"Seccess! topuped:{amount} to <@{discordid}>", ephemeral = True)
			await logchannel.send(f"Bank maneger <@{interaction.user.id}>  Topuped to <@{discordid}> ({discordid})  : {amount}")
		else:
			await interaction.response.send_message(f"You cant topup < 1", ephemeral = True)
		#await dm.send(f"Manager <@{interaction.user.id}> topuped: {amount} On your balance")
	else:
		await interaction.response.send_message("something went wrong", ephemeral = True)
	return




@tree.command(name = "withdraw", description = "Зняти з рахунку користувача(тільки для банкірів)")
@app_commands.checks.has_role(bankmanager)
@app_commands.describe(discordtag = "Тегніть користувача з балансу якого знімаються діаманти (приклад @RedInJector)", amount = "Кількість діамантів, які знімаються з рахунку")
async def withdraw(interaction: discord.Interaction, discordtag:str, amount:int):
	logchannel = bot.get_channel(int(LogChat))
	discordid = discordtag.translate({ ord(c): None for c in "<!@>" })
	discordtag = bot.get_user(int(discordid))
	check1 = sql_commands.CheckIfExists(discordid)
	if check1:
		if amount >= 1:
			balance = sql_commands.BalanceWithDiscordID(discordid)
			if balance >= amount:
				sql_commands.Withdraw_money_WithDiscordTag(discordtag,amount)

				#balanceinfo = sql_commands.BalanceWithTag(discordtag)

				balance = sql_commands.BalanceWithDiscordID(discordid)

				dm = await discordtag.create_dm()  # Creates a dm channel with the user
				embed=discord.Embed(title= "Офіційний банк Аметісу", description = f"Банкір <@{interaction.user.id}> зняв кошти з вашого балансу на **{amount}** діамант(ів).\n\nВаш баланс: **{balance} діамант(ів)**", color=0x6f12c0)
				pfp = bot.get_user(int(discordid)).avatar.url
				pfp2 = interaction.user.avatar.url
				embed.set_thumbnail(url=pfp2)
				embed.set_footer(text=f"{discordtag}", icon_url=pfp)
				await dm.send(embed=embed)

				#await dm.send(f"Manager {interaction.user} withdrawed: {amount} From your balance")
				await interaction.response.send_message(f"Seccess! Withdrawed:{amount} from <@{discordid}>", ephemeral = True)
				await logchannel.send(f"Bank manager <@{interaction.user.id}>  Withdrawed from <@{discordid}>({discordid})  : {amount}")
			else:
				await interaction.response.send_message("Not enough money", ephemeral = True)
		else:
			await interaction.response.send_message(f"You cant withdraw < 1", ephemeral = True)
	else:
		await interaction.response.send_message("something went wrong", ephemeral = True)
	return





@tree.command(name = "transfer", description = "Переказати гроші іншому користувачу") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.describe(discordtag = "Тегніть користувача якому переказуєте діаманти (приклад @maksutko)", amount = "Кількість діамантів, які переказуються", comment = "Коментар до транзакції (необов'язковий)")
async def transfer(interaction: discord.Interaction,discordtag:str,amount:int, comment:str = None):
	logchannel = bot.get_channel(int(LogChat))
	discordid = discordtag.translate({ ord(c): None for c in "<!@>" })
	discordtag = bot.get_user(int(discordid))
	if interaction.user != discordtag:
		check1 = sql_commands.CheckIfExists(interaction.user.id)
		check2 = sql_commands.CheckIfExists(discordid)
		if check1 == True and check2 == True:

			if amount >=1:
				balance = sql_commands.BalanceWithDiscordID(interaction.user.id)
				if balance >= amount:
					sql_commands.TransferMoney_WithDiscordID(interaction.user.id,amount, discordid)
					comm = ""
					if comment != None:
						comm = "\n\nКоментар: " + comment

					balance = sql_commands.BalanceWithDiscordID(interaction.user.id)
					embed=discord.Embed(title= "Офіційний банк Аметісу", description = f"**{amount}** діамант(ів) успішно переказано **<@{discordid}>**  {comm} \n\nЗалишок на балансі: **{balance} діамант(ів)**", color=0x6f12c0)
					pfp = bot.get_user(int(discordid)).avatar.url
					pfp2 = interaction.user.avatar.url
					embed.set_thumbnail(url=pfp)
					embed.set_footer(text=f"{interaction.user}", icon_url= pfp2)
					
					await interaction.response.send_message(embed=embed, ephemeral = True)

					#await interaction.response.send_message(f"Succesfully transfered {amount} to <@{discordid}>")
					
					balanceinfo = sql_commands.BalanceWithDiscordID(discordid)
					embed=discord.Embed(title= "Офіційний банк Аметісу", description = f"**<@{interaction.user.id}>** переказав вам **{amount}** діамант(ів) {comm} \n\nВаш баланс: **{balanceinfo} діамант(ів)**", color=0x6f12c0)
					pfp = bot.get_user(int(discordid)).avatar.url
					pfp2 = interaction.user.avatar.url
					embed.set_thumbnail(url=pfp2)
					embed.set_footer(text=f"{discordtag}", icon_url= pfp)

					dm = await discordtag.create_dm()  # Creates a dm channel with the user
					await dm.send(embed=embed)
					await logchannel.send(f"Transfered: <@{interaction.user.id}>  -------->  <@{discordid}>    : {amount}")
				else:
					await interaction.response.send_message(f"Not enough money", ephemeral = True)
			else:
				await interaction.response.send_message(f"You cant transfer < 1", ephemeral = True)
		else:
			await interaction.response.send_message(f"Somethong went wrong", ephemeral = True)
	else:
		await interaction.response.send_message(f"You cant transfer to yourself", ephemeral = True)
	return



@tree.command(name = "balance", description = "Перевірити стан рахунку")
async def Playerbalance(interaction: discord.Interaction):
	check1 = sql_commands.CheckIfExists(interaction.user.id)
	if check1:
		balanceinfo = sql_commands.BalanceWithDiscordID(interaction.user.id)
		card_number = ""
	#insert spaces between numbers 4565478915983248 ---> 4565 4789 1598 3248
		for i, c in enumerate(str(interaction.user.id)[2:]):
			if i > 0 and i % 4 == 0:
				card_number += " "
			card_number += c

		embed=discord.Embed(title="Офіційний банк Аметісу", description=f"Номер карти: **{card_number}** \nТермін дії до: **01/24**  \n\nВаш баланс: **{balanceinfo} діамант(ів)**", color=0x6f12c0)
		pfp = interaction.user.avatar.url
		embed.set_thumbnail(url=pfp)
		embed.set_footer(text=f"{interaction.user}", icon_url=pfp)
		await interaction.response.send_message(embed=embed, ephemeral = True)
		#await interaction.response.send_message(f"you have {balance}!")
	else:
		await interaction.response.send_message(f"You dont have a balance", ephemeral = True)
	return




@tree.command(name = "forbes", description = "Топ 5 найбагатших клієнтів банку")
async def forbes(interaction: discord.interactions):
	list = sql_commands.top()
	message = ""
	n = 1
	topID = list[0]
	
	
	for row in list:
		statement = ""
		rowint = int(row[2])
		if rowint > 1000000:
			statement = "> 1 000 000"
		elif rowint > 500000:
			statement = "> 500 000"
		elif rowint > 200000:
			statement = "> 200 000"
		elif rowint > 100000:
			statement = "> 100 000"
		elif rowint > 80000:
			statement = "> 80 000"
		elif rowint > 50000:
			statement = "> 50 000"	
		elif rowint > 20000:
			statement = "> 20 000"	
		elif rowint > 10000:
			statement = "> 10 000"		
		elif rowint > 8000:
			statement = "> 8 000"	
		elif rowint > 5000:
			statement = "> 5 000"	
		elif rowint > 2000:
			statement = "> 2 000"				
		elif rowint > 1000:
			statement = "> 1 000"	
		elif rowint > 800:
			statement = "> 800"
		elif rowint > 500:
			statement = "> 500"		
		elif rowint > 200:
			statement = "> 200"	
		elif rowint > 100:
			statement = "> 100"	
		else:
			statement = "< 100"	

		message = message + f"**{n}**. {row[0]} **{statement}** (діамантів)\n\n"
		n += 1
	

	embed=discord.Embed(title="Список Forbes - найбагатші гравці", description=message, color=0xF0E345)
	embed.set_footer(text = "   Приблизна оцінка статків")
	discordtag = bot.get_user(int(topID[1]))
	pfp = discordtag.avatar.url
	embed.set_thumbnail(url=pfp)
	#embed.set_footer(text=f"{interaction.user}", icon_url=pfp)
	await interaction.response.send_message(embed=embed, ephemeral = True)








@tree.command(name = "fine_add", description = "Накласти штраф на гравця(тільки для поліції)")
@app_commands.checks.has_role(police)
@app_commands.describe(discordtag = "Тегніть користувача на якого накладається штраф (приклад @maksutko)", amount = "Кількість діамантів", reason = "Причина")
async def add_fee(interaction: discord.integrations,discordtag:str, amount:int, reason:str):
	logchannel = bot.get_channel(int(LogChat))
	discordid = discordtag.translate({ ord(c): None for c in "<!@>" })
	discordtag = bot.get_user(int(discordid))
	check1 = sql_commands.CheckIfExists(discordid)
	if (check1 == True) and (amount) >= 1:
		sql_commands.NewFine(discordtag,discordid, amount, reason)
		#lol change
		thumburl = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.amazon.pl%2FWidmann-Kostium-NYPD-Police-Officer%2Fdp%2FB00KZ1VWCY&psig=AOvVaw3gY15iYUqkoiwxFYVxBGUk&ust=1672423417899000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCPCYhu-0n_wCFQAAAAAdAAAAABAE"

		embed = discord.Embed(title="Виписано штраф", description=f"**{amount}** діамант(-ів) гравцю <@{discordid}> \n**По причині:** {reason} \n\n\t**Виписано!**", color = 0xFF0000)
		embed.set_footer(text=interaction.user,icon_url=interaction.user.avatar.url)
		embed.set_thumbnail(url=thumburl)
		await interaction.response.send_message(embed=embed, ephemeral = True)


		embed = discord.Embed(title="Вам виписано штраф!", description=f"Причина: **{reason}** \nДо сплати: **{amount}** діамант(-ів)", color = 0xFF0000)
		embed.set_footer(text="",icon_url="")
		dm = await discordtag.create_dm()  # Creates a dm channel with the user
		await dm.send(embed=embed)

		await logchannel.send(f"**<@{discordid}>**  Був оштрафований  **<@{interaction.user.id}>** на **{amount}**")
	else:
		await interaction.response.send_message(f"Щось пішло не так", ephemeral = True)

@tree.command(name = "fine_see", description = "Переглянути накладені штрафи")
async def see_fine(interaction: discord.integrations):
	check1 = sql_commands.CheckIfExists(interaction.user.id)
	check2 = sql_commands.check_fineDiscordID(interaction.user.id)
	if check1 == True and check2 == True:
		message = ""
		fines = sql_commands.ReadFine(interaction.user.id)
		for row in fines:
			message = message + f"ID: {row[0]} Fine: {row[2]} Reason: {row[3]}\n"
		await interaction.response.send_message(f"```{message}```", ephemeral = True)
	elif check2 == False:
		await interaction.response.send_message(f"У вас немає несплачених штрафів", ephemeral = True)
	else:
		await interaction.response.send_message(f"Щось пішло не так", ephemeral = True)



@tree.command(name = "fine_see_all", description = "Вивести список усіх штрафів(тільки для поліції)")
@app_commands.checks.has_role(police)
async def see_someones_fine(interaction: discord.integrations):
	#discordid = discord_tag.translate({ ord(c): None for c in "<!@>" })
	#discord_tag = bot.get_user(int(discordid))
	#check1 = sql_commands.CheckIfExists(discord_tag)
	#check2 = sql_commands.check_finetag(discord_tag)
	#if check1 == True and check2 == True:
	message = ""
	fines = sql_commands.seeallfines()
	if fines != []:
		for row in fines:
			message = message + f"ID: {row[0]}  Player: {row[1]}   Fine: {row[3]} Reason: {row[4]}\n"
		await interaction.response.send_message(f"```{message}```", ephemeral = True)
	else:
		await interaction.response.send_message(f"```Немає штрафів```", ephemeral = True)
	#elif check1:
	#	await interaction.response.send_message(f"You dont have any fines", ephemeral = True)
	#else:
	#	await interaction.response.send_message(f"Somethong went wrong", ephemeral = True)



@tree.command(name = "fine_pay", description = "Оплатити штраф")
@app_commands.describe(fine_id = "Введіть ID штрафа (Його можна побачити в команді /see_fine)")
async def close_fine(interaction: discord.integrations, fine_id:int):
	logchannel = bot.get_channel(int(LogChat))
	check1 = sql_commands.CheckIfExists(interaction.user.id)
	check2 = sql_commands.check_fineid(fine_id)
	if check1 == True and check2 == True:
		balance = sql_commands.BalanceWithDiscordID(interaction.user.id)
		fine1 = sql_commands.fine_amount(fine_id)
		if balance >= fine1:
			fine = sql_commands.close_fine(interaction.user.id, fine_id)

			

			thumburl = "http://cedarfit.com/wp-content/uploads/2017/08/fitness-bank.jpg"
			embed = discord.Embed(title="Штраф сплачено!", description=f"Штраф: **{fine[0]} діамантів** \n**По причині:** {fine[1]} \n\n\t**Сплачено!**", color = 0x32CD32)
			embed.set_footer(text=str(interaction.user),icon_url=str(interaction.user.avatar.url))
			embed.set_thumbnail(url=thumburl)

			
			
			dm = await interaction.user.create_dm()  # Creates a dm channel with the user
			await dm.send(embed=embed)

			if interaction.user.id == fine[2]:
				await logchannel.send(f"**<@{interaction.user.id}>** Сплатив штраф ({fine[0]}) По причині: {fine[1]}")

			if fine[2] != interaction.user.id:
				embed = discord.Embed(title="Штраф сплачено!", description=f"<@{interaction.user.id}> сплатив ваш штраф: **{fine[0]} діамантів** \n**По причині:** {fine[1]}", color = 0x32CD32)
				discordtag = bot.get_user(fine[2])
				dm = await discordtag.create_dm()  # Creates a dm channel with the user
				await dm.send(embed=embed)
				await logchannel.send(f"**<@{interaction.user.id}>** Сплатив за <@{fine[2]}> штраф ({fine[0]}) По причині: {fine[1]}")
				
			#await dm.send(f"```Ви сплатили штраф: {fine[0]} З причиною: {fine[1]}```")
			


			
			await interaction.response.send_message(f"Успішно оплачено!", ephemeral = True)
		else:
			await interaction.response.send_message("У вас недостатньо коштів!", ephemeral = True)
	else:
		await interaction.response.send_message(f"Щось пішло не так", ephemeral = True)


@tree.error
async def on_app_command_error(interaction, error):
	if isinstance(error, app_commands.MissingRole):
		await interaction.response.send_message(error, ephemeral = True)
	elif isinstance(error, app_commands.NoPrivateMessage):
		await interaction.response.send_message(error, ephemeral = True)
	else:
		raise error


@tree.command(name = "asd")
async def test(interaction: discord.Interaction):
	#discordid = discordtag.translate({ ord(c): None for c in "<!@>" })
	#user = bot.get_user(int(discordid))
	#dm = await user.create_dm()  # Creates a dm channel with the user
	#await dm.send("What you want to send")  # Sends the user the message
	#print(discordid)
	#print(user)

	await interaction.response.send_message("asdsd")




bot.run(TOKEN)