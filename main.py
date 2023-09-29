import os
from dotenv.main import load_dotenv
from discord.ext import commands
import discord
import subprocess
import threading

server_up = False
start_server_thread = None
end_server_thread = None
server_process = None
backtomain = False

def start_mc_serv():
    global server_process
    bat_path = "E:\spigot1.20\start.bat"
    print("Thread Started!")
    server_process = subprocess.Popen(bat_path, shell=True, stdin=subprocess.PIPE)




def stop_mc_server(): #start programming the end thread here
    global server_process
    global server_up
    global backtomain
    global start_server_thread
    try:
        server_process.stdin.write(b'stop\n')
        server_process.stdin.flush()
        start_server_thread.join()
        start_server_thread = None
        backtomain = True

    except Exception as e:
        print(f"Error sending 'stop' command to the server: {e}")



    server_up = False
    print("Server shut down!")






def main():
    global server_up
    global start_server_thread
    global end_server_thread


    client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    load_dotenv()

    @client.event
    async def on_ready():
        print(f"{client.user.name} has connected to Discord.")
        await client.change_presence(activity=discord.Game(name="Awaiting server start command!"))

    @client.command()
    async def startserver(ctx):
        global server_up
        global start_server_thread
        global end_server_thread
        if not server_up:
            server_up = True
            await ctx.send("Starting Server...")
            await client.change_presence(activity=discord.Game(name="Running the Server!"))

            start_server_thread = threading.Thread(target=lambda: start_mc_serv())
            start_server_thread.start()

            await ctx.send('Server is up!')
        else:
            await ctx.send("The server is already running!")

    @client.command()
    async def stopserver(ctx):
        global server_process
        global start_server_thread
        global end_server_thread
        global server_up
        global backtomain

        if server_process and server_process.poll() is None:
            if end_server_thread is None:
                end_server_thread = threading.Thread(target=lambda: stop_mc_server())
            end_server_thread.start()
            if backtomain:
                end_server_thread.join()
                end_server_thread = None
                server_up = False
                await client.change_presence(activity=discord.Game(name="Awaiting server start command!"))
                await ctx.send("Server shut down successfully!(PLEASE WAIT A MIN OR 2 TO START AGAIN!)")
        else:
            await ctx.send("Server isn't running.")



    client.run(os.getenv("DISCORD_TOKEN"))

if __name__ == '__main__':
    main()
