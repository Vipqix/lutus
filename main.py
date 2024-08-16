from discord.ext import commands
from functions import Funcs
import customtkinter
import discord
import asyncio
import threading


class DiscordBot:
    def __init__(self):
        self.client = None

    async def list_servers(self, token, output_func):
        self.client = discord.Client(intents=discord.Intents(guilds=True))

        @self.client.event
        async def on_ready():
            output_func(f'Bot is connected as {self.client.user}\n')
            output_func('=================\nListing all servers and invites:\n=================\n')
            for guild in self.client.guilds:
                output_func('=================\n')
                output_func(f'- {guild.name} (ID: {guild.id})\n')
                try:
                    invites = await guild.invites()
                    if invites:
                        for invite in invites:
                            output_func(f'  - Invite: {invite.url} | Uses: {invite.uses}\n')
                    else:
                        output_func(f'  - No invites found. Creating a new invite...\n')
                        # Create a new invite for the first text channel
                        new_invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)
                        output_func(f'  - New Invite: {new_invite.url}\n')
                except discord.Forbidden:
                    output_func(f'  - No permission to view or create invites.\n')
                except discord.HTTPException as e:
                    output_func(f'  - Failed to retrieve or create invites: {e}\n')
                output_func('---\n')
            output_func('=================\n')
            await self.client.close()

        try:
            await self.client.login(token)
            await self.client.connect()
        except discord.errors.LoginFailure:
            output_func('Invalid token or failed to connect.\n')
        except Exception as e:
            output_func(f'An error occurred: {e}\n')

    async def check_bot_info(self, token, output_func):
        self.client = discord.Client(intents=discord.Intents.default())

        @self.client.event
        async def on_ready():
            user = self.client.user
            output_func('=================\n')
            output_func(f'Bot Name: {user.name}\n')
            output_func(f'Bot Bio: {user.bio if hasattr(user, 'bio') else "No bio available"}\n')
            output_func(f'Bot id: {user.id}\n')
            output_func(f'Bot Avatar: {str(user.avatar.url) if user.avatar else None}\n')
            output_func('=================\n')
            await self.client.close()

        try:
            await self.client.login(token)
            await self.client.connect()
        except discord.errors.LoginFailure:
            output_func('Invalid token or failed to connect.\n')
        except Exception as e:
            output_func(f'An error occurred: {e}\n')


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lutus")
        self.geometry(f"{480}x{580}")
        self.resizable(0, 0)

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.pack(expand=1, fill='both', pady=10, padx=10)

        # Adding tabs
        self.tabview.add("Checker")
        self.tabview.add("Inviter")

        # Checker Tab
        self.label_tab_1 = customtkinter.CTkLabel(self.tabview.tab("Checker"), text="Enter the bot token you want to check\n ! ! LOADING WILL TAKE SOME TIME ! ! ")
        self.label_tab_1.pack(padx=5, pady=5)

        self.entry_box_1 = customtkinter.CTkEntry(self.tabview.tab("Checker"))
        self.entry_box_1.pack(pady=5, padx=5, fill='x')

        self.check_button_1 = customtkinter.CTkButton(self.tabview.tab("Checker"), text="Check", command=self.run_check_token)
        self.check_button_1.pack(pady=5, padx=5, fill="x")

        self.output_box_1 = customtkinter.CTkTextbox(self.tabview.tab("Checker"))
        self.output_box_1.pack(pady=5, padx=5, fill="both", expand=1)
        self.output_box_1.insert("0.0", "Nothing checked yet.\n")

        self.clear_button1 = customtkinter.CTkButton(self.tabview.tab("Checker"), text="Clear", command=self.clear1)
        self.clear_button1.pack(pady=5, padx=5, fill="x")

        # Inviter Tab
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Inviter"), text="Enter the bot token you want to get all server invites of\n ! ! LOADING WILL TAKE SOME TIME ! ! ")
        self.label_tab_2.pack(padx=5, pady=5)

        self.entry_box_2 = customtkinter.CTkEntry(self.tabview.tab("Inviter"))
        self.entry_box_2.pack(pady=5, padx=5, fill='x')

        self.invite_button_2 = customtkinter.CTkButton(self.tabview.tab("Inviter"), text="Get Invites", command=self.run_get_invites)
        self.invite_button_2.pack(pady=5, padx=5, fill="x")

        self.output_box_2 = customtkinter.CTkTextbox(self.tabview.tab("Inviter"))
        self.output_box_2.pack(pady=5, padx=5, fill="both", expand=1)
        self.output_box_2.insert("0.0", "Nothing checked yet.\n")

        self.clear_button2 = customtkinter.CTkButton(self.tabview.tab("Inviter"), text="Clear", command=self.clear2)
        self.clear_button2.pack(pady=5, padx=5, fill="x")

    def clear1(self):
        self.output_box_1.delete("1.0", customtkinter.END)

    def clear2(self):
        self.output_box_2.delete("1.0", customtkinter.END)

    def run_check_token(self):
        token = self.entry_box_1.get()
        if token:
            bot = DiscordBot()
            threading.Thread(target=self.start_check_token, args=(bot, token)).start()

    def start_check_token(self, bot, token):
        def output_func(text):
            self.output_box_1.insert(customtkinter.END, text)

        asyncio.run(bot.check_bot_info(token, output_func))

    def run_get_invites(self):
        token = self.entry_box_2.get()
        if token:
            bot = DiscordBot()
            threading.Thread(target=self.start_get_invites, args=(bot, token)).start()

    def start_get_invites(self, bot, token):
        def output_func(text):
            self.output_box_2.insert(customtkinter.END, text)

        asyncio.run(bot.list_servers(token, output_func))


if __name__ == "__main__":
    app = App()
    app.mainloop()
