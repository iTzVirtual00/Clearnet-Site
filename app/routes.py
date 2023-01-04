from quart import Blueprint, render_template, request, flash, redirect, url_for, copy_current_app_context, current_app\
    , Request

import settings
from app.utils import Server_API, RateLimit

bp_router = Blueprint('routers', __name__, url_prefix='/')


@bp_router.get('')
async def index():
    return await render_template('index.html', listeners=await Server_API.get_listeners_gen().__anext__(),
                                 song_title=await Server_API.get_song_gen().__anext__())


@bp_router.get('about')
async def about():
    return await render_template('about.html', listeners=await Server_API.get_listeners_gen().__anext__(),
                                 song_title=await Server_API.get_song_gen().__anext__())


@bp_router.get('mirrors')
async def mirrors():
    return await render_template('mirrors.html', listeners=await Server_API.get_listeners_gen().__anext__(),
                                 song_title=await Server_API.get_song_gen().__anext__())


@bp_router.get('donate')
async def donate():
    return await render_template('donate.html', listeners=await Server_API.get_listeners_gen().__anext__(),
                                 song_title=await Server_API.get_song_gen().__anext__())


@bp_router.get('community')
async def community():
    return await render_template('community.html', listeners=await Server_API.get_listeners_gen().__anext__(),
                                 song_title=await Server_API.get_song_gen().__anext__())


@bp_router.get('source')
async def source():
    await Server_API.get_song_gen().__anext__()
    return await render_template('source.html', listeners=await Server_API.get_listeners_gen().__anext__(),
                                 song_title=await Server_API.get_song_gen().__anext__())


@bp_router.get('songs')
async def songs():
    return await render_template('songs.html', listeners=await Server_API.get_listeners_gen().__anext__(),
                                 song_title=await Server_API.get_song_gen().__anext__(),
                                 songs=await Server_API.get_all_gen().__anext__())


@bp_router.post('songs')
async def post_songs():
    form = await request.form
    yt_id = form.get('yt-id', None)

    if not yt_id:
        await flash('Empty ID :(')
        return redirect(url_for('routers.songs'))
    elif len(yt_id) > 11:
        await flash('Invalid ID :(')
        return redirect(url_for('routers.songs'))

    song, code = await Server_API.submit_song(settings.API_SECRET, yt_id)

    if code == 409:
        await flash(f'Song already added :(')
        return redirect(url_for('routers.songs'))
    elif code == 429:
        await flash(f'Too many requests :(')
        return redirect(url_for('routers.songs'))
    elif code == 422:
        await flash('Invalid ID :(')
        return redirect(url_for('routers.songs'))
    elif code == 500:
        await flash('Download error :(')
        return redirect(url_for('routers.songs'))

    await flash('Song added :)')
    return redirect(url_for('routers.songs'))


@copy_current_app_context
@bp_router.get('songs/search')
async def search_songs():
    title = request.args.get('title', None)

    if not title:
        return redirect(url_for('routers.songs'))

    song, code = await Server_API.search_song(title)

    if not song:
        await flash('Song not found :/')
        return redirect(url_for('routers.songs'))

    return await render_template('songs.html', listeners=await Server_API.get_listeners_gen().__anext__(),
                                 song_title=await Server_API.get_song_gen().__anext__(), songs=song)
