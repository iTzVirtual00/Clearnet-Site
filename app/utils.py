import time

import aiohttp

import settings


class RateLimit:
    _last_submit = 100

    @classmethod
    async def submit(cls):
        cls._last_submit = time.time()

    @classmethod
    async def last_submit(cls):
        return cls._last_submit


class Server_API:
    base_url = f'http://{settings.API_HOST}:{settings.API_PORT}/api'
    manage_url = f'http://{settings.API_HOST}:{settings.API_PORT}/api/manage'

    @classmethod
    async def get_all(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{cls.base_url}/all') as resp:
                songs = await resp.json()
                return songs

    @staticmethod
    async def get_all_gen():
        while True:
            songs = await Server_API.get_all()
            _last_fetch = time.time()
            while (time.time() - _last_fetch) < 10:
                yield songs

    @classmethod
    async def get_song(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{cls.base_url}/song') as resp:
                song = await resp.json()
                song = song.get('current_song').get('title')
                return song

    @staticmethod
    async def get_song_gen():
        while True:
            song = await Server_API.get_song()
            _last_fetch = time.time()
            while (time.time() - _last_fetch) < 30:
                yield song

    @classmethod
    async def get_listeners(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{cls.base_url}/listeners') as resp:
                listeners = await resp.json()
                listeners = listeners.get('listeners')
                return listeners

    @staticmethod
    async def get_listeners_gen():
        while True:
            listeners = await Server_API.get_listeners()
            _last_fetch = time.time()
            while (time.time() - _last_fetch) < 30:
                yield listeners

    @classmethod
    async def search_song(cls, title: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{cls.base_url}/search/{title}') as resp:
                reply = await resp.json()
                code = resp.status
                return reply, code

    @classmethod
    async def submit_song(cls, secret: str, song_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.put(f'{cls.manage_url}/{secret}/add/{song_id}') as resp:
                reply = await resp.json()
                code = resp.status
                return reply, code
