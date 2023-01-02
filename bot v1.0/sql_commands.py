import sqlite3 as sql


con = sql.connect('test.db')
table = 'test1'



with con:
	cur = con.cursor()
	cur.execute(f'''CREATE TABLE IF NOT EXISTS `{table}` (ID INTEGER PRIMARY KEY, Discord_tag string,Discord_ID string,Card_number string,Money integer, minecraft_name string)''')
	cur.execute(f'''CREATE TABLE IF NOT EXISTS `{table}1` (ID INTEGER PRIMARY KEY, Discord_tag string,Discord_ID string, amount integer, reason string)''')
	con.commit()


#add new record in table
def DataNewClient(Discord_tag:str, Discord_ID:str, minecraft_name:str):#new user into sql
	if  CheckIfExists(Discord_tag) == False:
		card_number = Discord_ID[2:]
		cur.execute(f"""INSERT INTO {table}(Discord_tag, Discord_ID,Card_number, Money, minecraft_name) VALUES ('{Discord_tag}','{Discord_ID}','{card_number}', '0','{minecraft_name}')""")
		con.commit()  # Remember to commit the transaction after executing INSERT
		return True
	else:
		return False


#check if client exists
def CheckIfExists(DiscordID):
	check = cur.execute(f"SELECT * FROM {table} WHERE Discord_ID = '{DiscordID}'").fetchone()
	con.commit()
	if check is None:
		return False
	else:
		return True




#add and withdraw
def add_money_WithDiscordID(discord_id, amount):
	cur.execute(f"SELECT Money FROM {table} WHERE Discord_ID = '{discord_id}'")
	money = int(cur.fetchone()[0])
	money = money + amount
	cur.execute(f"UPDATE '{table}' SET money = {money} WHERE Discord_ID = '{discord_id}'")
	con.commit()  # Remember to commit the transaction after executing INSERT

def Withdraw_money_WithDiscordID(discordid, amount):
	cur.execute(f"SELECT Money FROM {table} WHERE Discord_ID = '{discordid}'")
	money = int(cur.fetchone()[0])
	money = money - amount
	cur.execute(f"UPDATE '{table}' SET money = {money} WHERE Discord_ID = '{discordid}'")
	con.commit()  # Remember to commit the transaction after executing INSERT

def Withdraw_money_WithDiscordTag(Discord_tag:str, amount:int):
		cur.execute(f"SELECT Money FROM {table} WHERE Discord_tag = '{Discord_tag}'")
		money = int(cur.fetchone()[0])
		money = money - amount
		cur.execute(f"UPDATE '{table}' SET money = {money} WHERE Discord_tag = '{Discord_tag}'")
		con.commit()  # Remember to commit the transaction after executing INSERT



def add_money_WithDiscordTag(Discord_tag:str,amount:int):
	cur.execute(f"SELECT Money FROM {table} WHERE Discord_tag = '{Discord_tag}'")
	money = int(cur.fetchone()[0])
	money = money + amount
	cur.execute(f"UPDATE '{table}' SET money = {money} WHERE Discord_tag = '{Discord_tag}'")
	con.commit()  # Remember to commit the transaction after executing INSERT


#transfer p2p
def TransferMoney_WithDiscordID(From_who_ID,amount, To_who_ID):
	Withdraw_money_WithDiscordID(From_who_ID,amount)
	add_money_WithDiscordID(To_who_ID,amount)


def TransferMoney_WithDiscordTag(From_who_DiscordTag,amount, To_who_DiscordTag):
		Withdraw_money_WithDiscordTag(From_who_DiscordTag,amount)
		add_money_WithDiscordTag(To_who_DiscordTag,amount)


#return balance number
def BalanceWithTag(Discord_tag):
	cur.execute(f"SELECT Money FROM {table} WHERE Discord_tag = '{Discord_tag}'")
	money = int(cur.fetchone()[0])
	cur.execute(f"SELECT Card_number FROM {table} WHERE Discord_tag = '{Discord_tag}'")
	cardid = int(cur.fetchone()[0])

	res = [money, cardid]
	return res

def BalanceWithDiscordID(discord_ID):
	cur.execute(f"SELECT Money FROM {table} WHERE Discord_ID = '{discord_ID}'")
	money = int(cur.fetchone()[0])
	return money


def NewFine(discord_tag:str,discord_id,amount:int, reason:str):
	cur.execute(f"INSERT INTO {table}1(Discord_tag, Discord_ID, amount, reason) VALUES ('{discord_tag}','{discord_id}', '{amount}', '{reason}')")
	con.commit()

def ReadFine(discord_id:str):
	cur.execute(f"SELECT * FROM {table}1 WHERE Discord_ID = '{discord_id}'")
	fineList = cur.fetchall()
	return fineList


def seeallfines():
	cur.execute(f"SELECT * FROM {table}1")
	finelist = cur.fetchall()
	return finelist



def check_fineDiscordID(Discord_id):
	check = cur.execute(f"SELECT * from {table}1 WHERE Discord_ID = '{Discord_id}';").fetchone()
	if check is None:
		return False
	else:
		return True


def check_fineid(ID):
	check = cur.execute(f"SELECT * from {table}1 WHERE ID = '{ID}';").fetchone()
	if check is None:
		return False
	else:
		return True


def fine_amount(ID:int):
	fine = int(cur.execute(f"SELECT * FROM {table}1 WHERE ID = {ID}").fetchone()[3])
	return fine


def close_fine(discordid:str,ID:int):
	fine = [
	cur.execute(f"SELECT * FROM {table}1 WHERE ID = {ID}").fetchone()[3], 
	cur.execute(f"SELECT * FROM {table}1 WHERE ID = {ID}").fetchone()[4],
	cur.execute(f"SELECT * FROM {table}1 WHERE ID = {ID}").fetchone()[2]
	]
	amount = int(cur.execute(f"SELECT amount FROM {table}1 WHERE ID = {ID}").fetchone()[0])
	Withdraw_money_WithDiscordID(discordid, amount)
	cur.execute(f"DELETE FROM {table}1 WHERE ID = {ID}")
	con.commit
	return fine


def top():
	cur.execute(f"SELECT Discord_tag, Discord_ID, Money From {table} ORDER BY Money DESC LIMIT 5")
	list = cur.fetchall()
	return list


#NewFee('1234',55,'jo mama123')
#feelist = ReadFee('1234')



##/bank createcard vasia#1234 vasiaPro2007

#add_money(12435234657, 10)