from quart import Quart, jsonify, request, send_from_directory, Response
from utils.source.gogoanime.gogoanime import GogoAnimeClient
from utils.source.dramacool.dramacool import DramaCoolClient
from utils.source.moviesdrive.moviedrive import MoviesDrive
from utils.source.torrent.torrent import TorrentClient
from utils.source.vidsrc.vidsrc import VidSrcClient
from utils.source.manga.manga import MangaClient    
from utils.source.tmdb.tmdb import TMDbFetcher
import aiofiles 
import asyncio

app = Quart(__name__, static_folder='docs')

gogo_anime = GogoAnimeClient()
drama_cool = DramaCoolClient() 
movies_drive = MoviesDrive()
manga_client = MangaClient()
torrent = TorrentClient()
vidsrc = VidSrcClient()
tmdb = TMDbFetcher()

#-------------------
# API STATUS
#-------------------
@app.route('/')
async def spycliapi_home():
    return jsonify({"spycli": "online"})

@app.route('/spycliapi/log')
async def spycliapi_log():
    log_path = '/content/spycli-api.log'
    try:
        async with aiofiles.open(log_path, mode='r') as log_file:
            content = await log_file.read()
        return Response(content, mimetype='text/plain')
    except Exception as e:
        return Response(f"Error reading log file: {e}", status=500)
    
#-------------------
# MOVIES DRIVE ROUTES
#-------------------
@app.route('/moviesdrive')
async def moviesdrive_documentation():
    return await send_from_directory('docs', 'moviesdrive_doc.html')

@app.route('/moviesdrive/trending', methods=['GET'])
async def moviesdrive_get_movies():
    page = request.args.get('page', default=1, type=int)
    # Offload synchronous call to a separate thread
    movies = await asyncio.to_thread(movies_drive.get_movies, page=page)
    return jsonify(movies)

@app.route('/moviesdrive/search', methods=['GET'])
async def moviesdrive_search():
    query = request.args.get('query', default='', type=str)
    # Offload synchronous call to a separate thread
    results = await asyncio.to_thread(movies_drive.search, query)
    return jsonify(results)

@app.route('/moviesdrive/detail', methods=['GET'])
async def moviesdrive_quality_info():
    movie_id = request.args.get('id', default='', type=str)
    # Offload synchronous call to a separate thread
    info = await asyncio.to_thread(movies_drive.checker, movie_id)
    return jsonify(info)

@app.route('/moviesdrive/quality', methods=['GET'])
async def moviesdrive_get_stream():
    movie_id = request.args.get('id', default='', type=str)
    # Offload synchronous call to a separate thread
    info = await asyncio.to_thread(movies_drive.fetch_content_links, movie_id)
    return jsonify(info)

@app.route('/moviesdrive/play', methods=['GET'])
async def moviesdrive_stream_link():
    url = request.args.get('id', default='', type=str)
    result = await movies_drive.scrape(url)
    return jsonify(result)

#-------------------
# GOGOANIME ROUTES
#-------------------
@app.route('/gogoanime')
async def gogoanime_documentation():
    return await send_from_directory('docs', 'gogoanime_doc.html')

@app.route('/gogoanime/trending', methods=['GET'])
async def gogoanime_get_anime():
    # Offload the synchronous function to a separate thread
    trending_anime = await asyncio.to_thread(gogo_anime.get_home)
    return jsonify(trending_anime)

@app.route('/gogoanime/search', methods=['GET'])
async def gogoanime_search():
    query = request.args.get('query', default='', type=str)
    # Offload the synchronous function to a separate thread
    results = await asyncio.to_thread(gogo_anime.search_anime, query)
    return jsonify(results)

@app.route('/gogoanime/detail', methods=['GET'])
async def gogoanime_detail():
    anime_id = request.args.get('id', default='', type=str)
    # Offload the synchronous function to a separate thread
    info = await asyncio.to_thread(gogo_anime.get_anime_details, anime_id)
    return jsonify(info)

@app.route('/gogoanime/episode', methods=['GET'])
async def gogoanime_episode():
    episode_id = request.args.get('id', default='', type=str)
    # Offload the synchronous function to a separate thread
    info = await asyncio.to_thread(gogo_anime.get_episode_stream_urls, episode_id)
    return jsonify(info)

@app.route('/gogoanime/episode/download', methods=['GET'])
async def gogoanime_episode_download():
    episode_id = request.args.get('id', default='', type=str)
    # Offload the synchronous function to a separate thread
    info = await asyncio.to_thread(gogo_anime.get_episode_download_urls, episode_id)
    return jsonify(info)

@app.route('/gogoanime/log')
async def gogoanime_log():
    log_path = '/content/anime_api.log'
    try:
        async with aiofiles.open(log_path, mode='r') as log_file:
            content = await log_file.read()
        return Response(content, mimetype='text/plain')
    except Exception as e:
        return Response(f"Error reading log file: {e}", status=500)
    
#-------------------
# TORRENT ROUTES
#-------------------
@app.route('/torrent')
async def torrent_documentation():
    return await send_from_directory('docs', 'torrent_doc.html')

@app.route('/torrent/search/all', methods=['GET'])
async def torrent_search_all():
    search_query = request.args.get('query', default='', type=str)
    limit = request.args.get('limit', default=2, type=int)
    # Offload the synchronous function to a separate thread
    info = await asyncio.to_thread(torrent.search_all_sites, search_query, limit=limit)
    return jsonify(info)

@app.route('/torrent/search/site', methods=['GET'])
async def torrent_search_site():
    search_query = request.args.get('query', default='', type=str)
    limit = request.args.get('limit', default=2, type=int)
    site = request.args.get('site', default=None, type=str)
    if not site:
        return jsonify({"error": "The 'site' parameter is required."}), 400
    # Offload the synchronous function to a separate thread
    info = await asyncio.to_thread(torrent.search_on_site, site, search_query, limit=limit)
    return jsonify(info)

@app.route('/torrent/log')
async def torrent_log():
    log_path = '/content/torrent_api.log'
    try:
        async with aiofiles.open(log_path, mode='r') as log_file:
            content = await log_file.read()
        return Response(content, mimetype='text/plain')
    except Exception as e:
        return Response(f"Error reading log file: {e}", status=500)
    
#-------------------
#  DRAMACOOL ROUTES
#-------------------
@app.route('/dramacool')
async def dramacool_documentation():
    return await send_from_directory('docs', 'dramacool_doc.html')

@app.route('/dramacool/search')
async def dramacool_search():
    query = request.args.get('query')
    page_no = request.args.get('page', default=1, type=int)
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    
    results = await asyncio.to_thread(drama_cool.search, query, page_no)
    if results is None:
        return jsonify({"error": "An error occurred during the search"}), 500
    return jsonify(results)

@app.route('/dramacool/info')
async def dramacool_info():
    drama_id = request.args.get('id')
    if not drama_id:
        return jsonify({"error": "Missing id parameter"}), 400
    
    info = await asyncio.to_thread(drama_cool.get_info, drama_id)
    if info is None:
        return jsonify({"error": "An error occurred while fetching info"}), 500
    return jsonify(info)

@app.route('/dramacool/streaming')
async def dramacool_streaming():
    episode_id = request.args.get('episodeId')
    media_id = request.args.get('mediaId')
    server = request.args.get('server', default="asianload")
    if not episode_id or not media_id:
        return jsonify({"error": "Missing episodeId or mediaId parameter"}), 400
    links = await asyncio.to_thread(drama_cool.get_streaming_links, episode_id, media_id, server)
    if links is None:
        return jsonify({"error": "An error occurred while fetching streaming links"}), 500
    return jsonify(links)

@app.route('/consumet/log')
async def consumet_log():
    log_path = '/content/consumet_api.log'  # Adjust the path as needed
    try:
        async with aiofiles.open(log_path, mode='r') as log_file:
            content = await log_file.read()
        return Response(content, mimetype='text/plain')
    except Exception as e:
        return Response(f"Error reading log file: {e}", status=500)

#-------------------
#  MANGA ROUTES
#-------------------

@app.route('/manga')
async def manga_documentation():
    return await send_from_directory('docs', 'manga_doc.html')

@app.route('/manga/search')
async def manga_search():
    source = request.args.get('source')
    query = request.args.get('query')
    if not source or not query:
        return jsonify({"error": "Missing source or query parameter"}), 400
    results = await asyncio.to_thread(manga_client.search, source, query)
    if results is None:
        return jsonify({"error": "An error occurred during the search"}), 500
    return jsonify(results)

@app.route('/manga/info')
async def manga_info():
    source = request.args.get('source')
    manga_id = request.args.get('id')
    if not source or not manga_id:
        return jsonify({"error": "Missing source or id parameter"}), 400
    info = await asyncio.to_thread(manga_client.get_manga_info, source, manga_id)
    if info is None:
        return jsonify({"error": "An error occurred while fetching info"}), 500
    return jsonify(info)

@app.route('/manga/chapters')
async def manga_chapters():
    source = request.args.get('source')
    chapter_id = request.args.get('chapterId')
    if not source or not chapter_id:
        return jsonify({"error": "Missing source or chapterId parameter"}), 400
    pages = await asyncio.to_thread(manga_client.get_chapter_pages, source, chapter_id)
    if pages is None:
        return jsonify({"error": "An error occurred while fetching chapter pages"}), 500
    return jsonify(pages)

#-------------------
#  TMDB ROUTES
#-------------------
@app.route('/tmdb')
async def tmdb_documentation():
    return await send_from_directory('docs', 'tmdb_doc.html')

@app.route('/tmdb/search', methods=['GET'])
async def tmdb_search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    try:
        # Offload the synchronous search operation to a separate thread
        results = await asyncio.to_thread(tmdb.search_multi, query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tmdb/fetch', methods=['GET'])
async def tmdb_get_seasons():
    media_id = request.args.get('id')
    if not media_id:
        return jsonify({"error": "Missing id parameter"}), 400
    try:
        # Offload the synchronous get seasons operation to a separate thread
        structure = await asyncio.to_thread(tmdb.get_seasons_episode_structure, 'tv', media_id)
        return jsonify(structure)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#-------------------
# VIDSRC ROUTES
#-------------------
@app.route('/vidsrc')
async def vidsrc_documentation():
    return await send_from_directory('docs', 'vidsrc_doc.html')

@app.route('/vsc/vidsrc/movie', methods=['GET'])
async def get_vidsrc_movie():
    movie_id = request.args.get('id', default=None, type=str)
    if not movie_id:
        return jsonify({"error": "Movie ID is required"}), 400
    # Offload the synchronous function to a separate thread
    info = await asyncio.to_thread(vidsrc.get_vidsrc_source, movie_id)
    return jsonify(info)

@app.route('/vsc/vsrcme/movie', methods=['GET'])
async def get_vsrcme_movie():
    movie_id = request.args.get('id', default=None, type=str)
    if not movie_id:
        return jsonify({"error": "Movie ID is required"}), 400
    # Offload the synchronous function to a separate thread
    info = await asyncio.to_thread(vidsrc.get_vsrcme_source, movie_id)
    return jsonify(info)

@app.route('/vsc/vidsrc/tv', methods=['GET'])
async def get_vidsrc_tv():
    tv_id = request.args.get('id', default=None, type=str)
    season = request.args.get('season', default=None, type=str)
    episode = request.args.get('episode', default=None, type=str)
    if not tv_id or not season or not episode:
        return jsonify({"error": "TV show ID, season, and episode are required"}), 400
    # Offload the synchronous function to a separate thread
    info = await asyncio.to_thread(vidsrc.get_vidsrc_source, tv_id, season=season, episode=episode)
    return jsonify(info)

@app.route('/vsc/vsrcme/tv', methods=['GET'])
async def get_vsrcme_tv():
    tv_id = request.args.get('id', default=None, type=str)
    season = request.args.get('season', default=None, type=str)
    episode = request.args.get('episode', default=None, type=str)
    if not tv_id or not season or not episode:
        return jsonify({"error": "TV show ID, season, and episode are required"}), 400
    # Offload the synchronous function to a separate thread
    info = await asyncio.to_thread(vidsrc.get_vsrcme_source, tv_id, season=season, episode=episode)
    return jsonify(info)

@app.route('/vsc/log')
async def vsc_log():
    log_path = '/content/vidsrc_api.log'
    try:
        async with aiofiles.open(log_path, mode='r') as log_file:
            content = await log_file.read()
        return Response(content, mimetype='text/plain')
    except Exception as e:
        return Response(f"Error reading log file: {e}", status=500)

if __name__ == '__main__':
    app.run(port=5000)