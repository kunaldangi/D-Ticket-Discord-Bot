"""

  ██████╗░  ░░░░░░  ████████╗██╗░█████╗░██╗░░██╗███████╗████████╗
  ██╔══██╗  ░░░░░░  ╚══██╔══╝██║██╔══██╗██║░██╔╝██╔════╝╚══██╔══╝
  ██║░░██║  █████╗  ░░░██║░░░██║██║░░╚═╝█████═╝░█████╗░░░░░██║░░░
  ██║░░██║  ╚════╝  ░░░██║░░░██║██║░░██╗██╔═██╗░██╔══╝░░░░░██║░░░
  ██████╔╝  ░░░░░░  ░░░██║░░░██║╚█████╔╝██║░╚██╗███████╗░░░██║░░░
  ╚═════╝░  ░░░░░░  ░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝░░░╚═╝░░░

"""
"""
COMMANDS:-
  - !dttcreate : to be create the ticket
  - !dtclose : to close the ticket (ticket only closed by ticket admin or ticket manager, user just only can make a close request)
  - !tsetadmin : to set a ticket admin with role name 'Ticket Admin' (Ticket Manager can use this command)
  - !tsetmanager : to set a ticket manager with role name 'Ticket Manager' (User with adminstrator permission can use this command)
Extra Feature:-  
  - !tservice (extra feature) : you can enable or disable (on/off) ticket service so noone can abuse it by make ticket channels.
  - Ticket channel cannot be create more than 10 ticket channels.
"""

import discord
from discord.ext import commands
from discord import Intents

# --- Variable ---
max_ticket_channel = 10
ticket_service = True
ticket_manager_role = "Ticket Manager" # Make these role for now
ticket_admin_role = "Ticket Admin"

bot = commands.Bot(command_prefix='!d', case_insensitive=True, intents=Intents.all())

@bot.event
async def on_ready():
  game = discord.Game("Created by DeViL#7091") # You can change rich presence
  await bot.change_presence(status=discord.Status.online, activity=game)

  print(f'Bot is online.\n Bot Name: {bot.user}!')

# ----- TICKET COMMANDS -----

# --- Ticket Create (tcreate) ---
@bot.command()
async def tcreate(ctx, *,reason):
  if ticket_service == True:
    total_ticket_channel = 0

    for channel in ctx.guild.channels:
      if "ticket" in str(channel):
        total_ticket_channel += 1

    global max_ticket_channel
    if total_ticket_channel >= max_ticket_channel:
      return await ctx.send(f"{ctx.author.mention} Please wait some time there are maxmimum ticket created!")
    
    ticket_channel = await ctx.guild.create_text_channel(f'ticket-{ctx.author.discriminator}')

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    overwrite.read_messages = False
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), overwrite=overwrite)

    await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

    for role in ctx.guild.roles:
      if ticket_manager_role in str(role) or ticket_admin_role in str(role):
        await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)

    await ticket_channel.send(f"{ctx.author.mention}, Ticket has been created!")
    
    # Embed Message
    embed = discord.Embed(title="Ticket", description="Please wait support will be with you shortly.", colour=ctx.author.colour)
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    embed.add_field(name="Created By:", value=f"{ctx.author.name}", inline=True)
    embed.add_field(name="Reason:", value=f"{reason}", inline=True)
    embed.set_footer(text="D-Ticket", icon_url=ctx.bot.user.avatar_url)

    await ticket_channel.send(embed=embed)
  else:
    await ctx.send(f"{ctx.author.mention}, Currently ticket service is off by admins. Please try again later or contact to server admin!")

# --- Ticket Close (tclose) ---
@bot.command()
async def tclose(ctx, *, reason:str):
  if is_ticket_manager(ctx) == True or is_ticket_admin(ctx) == True:

    if "ticket" in ctx.channel.name:

      return await ctx.channel.delete(reason=reason)

    else:
      return await ctx.send("Please use this command only in ticket channels.")

  else:
    for tchannel in ctx.guild.channels:

      if str(ctx.author.discriminator) in str(tchannel.name):

        if str(ctx.channel.name) in str(tchannel.name):

          await tchannel.set_permissions(ctx.author, read_messages=False, send_messages=False)
          await ctx.send(f"{ctx.author.mention}, Your ticket has been closed.")
          return await tchannel.send(f"{ctx.author.name} has requested to close the ticket. Reason: {reason}")

        else:
          return await tchannel.send(f"Please use this command here to close the ticket. {tchannel.mention}")
      
    else:
      return await ctx.channel.send("Your ticket is not found or ticket has already closed.")

      


# --- Set Ticket Admin (tsetadmin) ---
@bot.command()
@commands.has_permissions(send_messages=True)
async def tsetadmin(ctx, member:discord.Member):

  if ctx.author.name == member.name:
    return await ctx.send(f"{ctx.author.mention} You cannot give ticket admin role to yourself")

  else:

    for mrole in ctx.author.roles:
      if ticket_manager_role in str(mrole):

        for arole in member.roles:
          if ticket_admin_role in str(arole):
            return await ctx.send(f"{ctx.author.mention}, Mention member already have ticket admin role.")

        else:

          try:

            await member.add_roles(discord.utils.get(ctx.guild.roles, name=ticket_admin_role),reason=None, atomic=True)
            await ctx.send(f"{member.mention}, You are now ticket admin.")
            return await ctx.send(f"{ctx.author.mention}, `{member.name}` is now ticket admin.")

          except Exception as error:
            await ctx.send(f"{ctx.author.mention}, Something went wrong!")
            return print(f"Error (tsetadmin): {error}")
      
    else:
      await ctx.send(f"{ctx.author.mention}, You don't have access to set a ticket admin")

# --- Set Ticket Manager (tsetmanger) ---
@bot.command()
@commands.has_permissions(manage_roles=True)
async def tsetmanager(ctx, member:discord.Member):
  if ctx.author.name == member.name:
    return await ctx.send(f"{ctx.author.mention}, You cannot give manager role to yourself.")
  
  else:
    for role in member.roles:
      if ticket_manager_role in str(role):
        return await ctx.send(f"{ctx.author.mention}, Mention member already have ticket manager role.")
    else:
      try:
        await member.add_roles(discord.utils.get(ctx.guild.roles, name=ticket_manager_role),reason=None, atomic=True)
        await ctx.send(f"{member.mention}, You are ")
        return await ctx.send(f"{ctx.author.mention}, `{member.name}` is now ticket manager")
      except Exception as error:
        await ctx.send(f"{ctx.author.mention}, Something went wrong!")
        return print(f"Member ticket admin add role error: {error}")
    
@bot.command()
async def tservice(ctx, state:str):
  global ticket_service
  if is_ticket_manager(ctx) == True:
    if state == "on" or state == "enable":
      ticket_service = True
      return await ctx.send(f"{ctx.author.mention}, Ticket service is set to `{state}`")
    elif state == "off" or state == "disable":
      ticket_service = False
      return await ctx.send(f"{ctx.author.mention}, Ticket service is set to `{state}`")
    else:
      await ctx.send(f"{ctx.author.mention}, You have send invaild input.")
      await ctx.send(f"Correct Usage: tservice [on/off] or [enable/disable]")
  else:
    await ctx.send(f"{ctx.author.mention}, You don't have permission to use this command.")








# ----- ERROR HANDLER -----

# --- Ticket Close ---
@tclose.error
async def tcreate_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"{ctx.author.mention} Correct Usage: `tcreate [reason]`")

# --- Ticket Close ---
@tclose.error
async def tclose_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"{ctx.author.mention} Correct Usage: `tclose [reason]`")

# --- Ticket Set Admin (tsetadmin)
@tsetadmin.error
async def tsetadmin_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"{ctx.author.mention} Correct Usage: `tsetadmin [@member]`")

# --- Ticket Set Manager (tsetmanager)
@tsetmanager.error
async def tsetmanager_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(f"{ctx.author.mention} You don't have permission to use this command.")
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"{ctx.author.mention} Correct Usage: `!dtsetmanager [(mention)member]`")
  

    

# ----- FUNCTIONS -----

# --- is_ticket_manager ---
def is_ticket_manager(ctx):
  for role in ctx.author.roles:
    if ticket_manager_role in str(role):
      return True
  else:
    return False

# --- is_admin_manager ---
def is_ticket_admin(ctx):
  for role in ctx.author.roles:
    if ticket_admin_role in str(role):
      return True
  else:
    return False


bot.run('NzY0MzE1MzA1MzU0MTk5MDYx.X4EeGQ.YMd_aFSR8GFW-Ptjazm3V4ZO7BY') # Token as a string