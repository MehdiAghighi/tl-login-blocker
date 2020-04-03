from telethon import TelegramClient, events, types, functions, sync
import socks
import configparser
import logging
import asyncio

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Loading Environment varriables
config = configparser.ConfigParser()
config.read('config.ini')


async def main():
    clients = []

    for i in range(1, int(config['GENERAL']['ACCOUNTS']) + 1):
        client = TelegramClient(
            'Login Blocker #' + str(i),
            config['ACCOUNT.' + str(i)]['API_ID'],
            config['ACCOUNT.' + str(i)]['API_HASH'],
            proxy=(socks.SOCKS5, '127.0.0.1',
                   8383) if config['GENERAL']['USE_PROXY'] == "TRUE" else False
        )
        clients.append(client)

    @events.register(events.NewMessage(func=lambda event: event.sender_id == 777000))
    async def messageFromTelegram(event):
        if 'Login code:' in event.raw_text:
            await event.message.forward_to(257816718)

    @events.register(events.NewMessage())
    async def new(event):
        print(event.stringify())

    for client in clients:
        client.add_event_handler(messageFromTelegram)
        # client.add_event_handler(new)
        await client.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
