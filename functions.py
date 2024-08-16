import discord

class Funcs:

    @staticmethod
    async def checker(token: str):
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        try:
            await client.login(token)
            bot_user = await client.fetch_user(client.user.id)
            # print("Valid Token")
            bot_info = {
                "name": bot_user.name,
                "id": bot_user.id,
                "bio": bot_user.bio if hasattr(bot_user, 'bio') else "No bio available",
                "avatar_url": str(bot_user.avatar.url) if bot_user.avatar else None
            }

            return bot_info
        except discord.errors.LoginFailure:
            print("Invalid Token")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        finally:
            await client.close()


    async def inviter(token: str):
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)
        await client.login(token)
        print(f"Logged in as: {client.user}")    
        try:
            # Logging in with the bot token


            invite_info = []

            # Iterate through all guilds the bot is in
            for guild in client.guilds:
                invites = await guild.invites()
                guild_invites = [
                    {
                        "guild_name": guild.name,
                        "guild_id": guild.id,
                        "url": invite.url,
                    }
                    for invite in invites
                ]
                invite_info.extend(guild_invites)

            print(invite_info)
            return invite_info

        except discord.errors.LoginFailure:
            print("Invalid Token")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        finally:
            await client.close()