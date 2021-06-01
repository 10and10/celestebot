from discord.ext import commands
import discord

import subprocess

import json

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_mod(ctx):
        return ctx.author.guild_permissions.manage_channels

    @commands.command(aliases=['addcommand', 'newcommand'])
    @commands.check(is_mod)
    async def setcommand(self, ctx, command, *, message):
        self.bot.custom_commands["!" + command] = message
        with open('custom_commands.json', 'w') as f:
            json.dump(self.bot.custom_commands, f)

        await ctx.send(f"Set message for command {command}")

    @commands.command(aliases=['deletecommand'])
    @commands.check(is_mod)
    async def removecommand(self, ctx, command):
        del self.bot.custom_commands["!" + command]
        with open('custom_commands.json', 'w') as f:
            json.dump(self.bot.custom_commands, f)

        await ctx.send(f"Removed command {command}")
        
    @commands.check(is_mod)
    @commands.command(hidden=True)
    async def pull(self, ctx):
        out = subprocess.check_output("git pull", shell=True).decode("utf-8")
        if "Already up to date." in out:
            await ctx.send('No changes.')
        else:
            await ctx.send("Files changed (or some stupid error idk)")
            
    
    @commands.check(is_mod)
    @commands.command(name='reload', hidden=True, usage='<extension>')
    async def _reload(self, ctx, ext):
        """Reloads an extension"""
        try:
            self.bot.reload_extension(f'cogs.{ext}')
            await ctx.send(f'The extension {ext} was reloaded!')
        except commands.ExtensionNotFound:
            await ctx.send(f'The extension {ext} doesn\'t exist.')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'The extension {ext} is not loaded! (use !load)')
        except commands.NoEntryPointError:
            await ctx.send(f'The extension {ext} doesn\'t have an entry point (try adding the setup function) ')
        except commands.ExtensionFailed:
            await ctx.send(f'Some unknown error happened while trying to reload extension {ext} (check logs)')
            self.bot.logger.exception(f'Failed to reload extension {ext}:')
            
    @commands.check(is_mod)
    @commands.command(name='load', hidden=True, usage='<extension>')
    async def _load(self, ctx, ext):
        """Loads an extension"""
        try:
            self.bot.load_extension(f'cogs.{ext}')
            await ctx.send(f'The extension {ext} was loaded!')
        except commands.ExtensionNotFound:
            await ctx.send(f'The extension {ext} doesn\'t exist!')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'The extension {ext} is already loaded.')
        except commands.NoEntryPointError:
            await ctx.send(f'The extension {ext} doesn\'t have an entry point (try adding the setup function)')
        except commands.ExtensionFailed:
            await ctx.send(f'Some unknown error happened while trying to reload extension {ext} (check logs)')
            self.bot.logger.exception(f'Failed to reload extension {ext}:')
    

def setup(bot):
    bot.add_cog(Admin(bot))
