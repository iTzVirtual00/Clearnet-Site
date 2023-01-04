from quart import Blueprint, render_template

from app.utils import Server_API

api_router = Blueprint('api_router', __name__, url_prefix='/api')


@api_router.get('/routes')
async def api():
    return await render_template('api.html', listeners=await Server_API.get_listeners_gen().__anext__(),
                                 song_title=await Server_API.get_song_gen().__anext__())


@api_router.get('/all')
async def get_all():
    songs = await Server_API.get_all_gen().__anext__()
    return songs, 200


@api_router.get('/song')
async def current_song():
    song = await Server_API.get_song_gen().__anext__()
    return {'current_song': song}, 200


@api_router.get('/search/<title>')
async def search(title: str):
    song, code = await Server_API.search_song(title)

    if code == 404:
        return {}, 404

    song_id = list(song.keys())[0]
    song = song.get(song_id)

    return {'ID': song_id, 'added': song.get('added'), 'title': song.get('title')}, 302
