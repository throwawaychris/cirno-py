import discord

from discord.ext import commands
from discord import option
from discord.commands import permissions

from utils import log

logger = log.Logger(__name__)

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await logger.on_load(__class__.__name__)

    # Ping command
    @discord.slash_command(name="ping", description="Replies back with pong and latency")
    async def ping(self, ctx: discord.ApplicationContext):
        """
        Ping the bot and get latency back
        """

        await logger.on_execute(ctx.command.name, ctx.author)

        await ctx.respond(f'Pong! *(Latency: {round(self.bot.latency * 1000)})*')

    @discord.slash_command(name="owner", description="Replies who owns me")
    async def owner(self, ctx):
        """
        Get the bot owner
        """

        await logger.on_execute(ctx.command.name, ctx.author)

        owner = self.bot.get_user(self.bot.owner_id)
        print(type(self.bot.owner_id))

        await ctx.respond(f"{owner} ({self.bot.owner_id}) is my owner!")

        if self.bot.owner_ids:
            await ctx.send_followup(f"Other owners: {self.bot.owner_ids}")

    # About command group
    about = discord.SlashCommandGroup("about", "About various things")

    # About the bot
    @about.command(name="me", description="Get info about the bot")
    async def me(self, ctx: discord.ApplicationContext):
        """
        Get information about the bot
        """
        await logger.on_execute(ctx.command.name, ctx.author)

        bot_owner = await self.bot.fetch_user(self.bot.owner_id)
        bot_user = await self.bot.fetch_user(self.bot.user.id)

        # Embed
        info_board = discord.Embed(
            title=bot_user.display_name,
            description=f"A **{bot_user.display_name}** themed discord bot powered by *pycord!*",
            colour=discord.Colour.blue()
        )

        if hasattr(bot_user, "banner") and bot_user.banner is not None:
            info_board.set_image(url=bot_user.banner.url)

        info_board.set_thumbnail(url=f"{self.bot.user.display_avatar.url}")
        info_board.add_field(name="Created by", value="throwawaychris", inline=True)
        info_board.add_field(name="Owner", value=f"{bot_owner}", inline=True)

        await ctx.respond(embed=info_board)

    # About a member
    @about.command(name="member", description="Get info about a member")
    @option("member", description="Enter user to get info about", required=True)
    async def member(self, ctx: discord.ApplicationContext, member: discord.Member):
        """
        Get information about a member
        """
        
        await logger.on_execute(ctx.command.name, ctx.author)

        # Embed
        info_board = discord.Embed(
            title=member.display_name,
            description=f"A member of ***{ctx.guild.name}***!",
            colour=discord.Colour.blue()
        )

        if hasattr(self.member, "banner") and member.display_banner is not None:
            info_board.set_image(url=f"{member.display_banner.url}")

        info_board.set_thumbnail(url=f"{member.display_avatar.url}")
        info_board.add_field(name="Created at", value=member.created_at.strftime("%Y, %B %d"), inline=True)
        info_board.add_field(name="Joined at", value=member.joined_at.strftime("%Y, %B %d"), inline=True)

        await ctx.respond(embed=info_board)

    # About the guild
    @about.command(name="guild", description="Get info about the server")
    async def guild(self, ctx: discord.ApplicationContext):
        """
        Get information about the discord server
        """
        
        await logger.on_execute(ctx.command.name, ctx.author)

        this_server = ctx.guild

        #embed
        info_board = discord.Embed(
            title=this_server.name,
            description=this_server.description,
            colour=discord.Colour.blue()
        )

        if this_server.banner:
            info_board.set_image(url=this_sever.banner.url)
        
        info_board.set_author(name=f"ID: {this_server.id}", icon_url=this_server.icon.url)
        info_board.set_thumbnail(url=this_server.icon.url)
        info_board.add_field(name="Alive since:", value=this_server.created_at.strftime("%Y, %B %d"))
        info_board.add_field(name="Members:", value=this_server.member_count)
        info_board.add_field(name="Owner:", value=this_server.owner)

        await ctx.respond(embed=info_board)

    # Avatar command
    @discord.slash_command(name="avatar", description="Get user avatar")
    @option("member", description="Enter user to get avatar of", required=True)
    async def avatar(self, ctx: discord.ApplicationContext, member: discord.Member):
        """
        Get a user member avatar image link
        """
        
        await logger.on_execute(ctx.command.name, ctx.author)
        
        await ctx.respond(
            f"Here's an avatar of **{member.name}**!",
            embed = discord.Embed(image = member.avatar.url)
            )

    # Banner command
    @discord.slash_command(name="banner", description="Get user banner")
    @option("member", description="Enter user to get banner of", required=True)
    async def banner(self, ctx: discord.ApplicationContext, member: discord.Member):
        """
        Get the user's banner image url
        """
        
        await logger.on_execute(ctx.command.name, ctx.author)
        
        # If it's the bot
        if member == self.bot.user:
            # Have to fetch the id, because banner is not populated at start
            bot_user = await self.bot.fetch_user(self.bot.user.id)

            if bot_user.banner:
                await ctx.respond(bot_user.banner.url)
                await ctx.send_followup(f"Here's my banner!")
                return

        # Get banner if user has banner
        if hasattr(member, "banner") and member.banner is not None:
            await ctx.respond(member.banner)
            await ctx.send_followup(f"Here's an banner of {member.name}!")
        else:
            await ctx.respond(f"Couldn't fetch {member.display_name}'s banner...", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))