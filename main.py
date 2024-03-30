from quart import Quart, jsonify, request, send_from_directory, Response
from utils.source.moviesdrive.moviedrive import MoviesDrive
from utils.source.gogoanime.gogoanime import GogoAnimeClient
from utils.source.torrent.torrent import TorrentClient
from utils.source.vidsrc.vidsrc import VidSrcClient
from utils.source.tmdb.tmdb import TMDbFetcher
import aiofiles 

app = Quart(__name__, static_folder='docs')

movies_drive = MoviesDrive()
gogo_anime = GogoAnimeClient()
torrent = TorrentClient()
vidsrc = VidSrcClient()
tmdb = TMDbFetcher()

#-------------------
# API STATUS
#-------------------

@app.route('/')
async def spycliapi_home():
    return jsonify({"spycli": "online"})

@app.route('/log')
async def log():
    log_path = '/content/installation.log'
    try:
        async with aiofiles.open(log_path, mode='r') as log_file:
            content = await log_file.read()
        return Response(content, mimetype='text/plain')
    except Exception as e:
        return Response(f"Error reading log file: {e}", status=500)

@app.route('/spycliapi/log')
async def spycliapi_log():
    log_path = '/content/spycli-api.log'
    try:
        async with aiofiles.open(log_path, mode='r') as log_file:
            content = await log_file.read()
        return Response(content, mimetype='text/plain')
    except Exception as e:
        return Response(f"Error reading log file: {e}", status=500)

@app.route('/cloudflare/log')
async def cloudflare_log():
    log_path = '/content/cloudflared.log'
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
    movies = movies_drive.get_movies(page=page)
    return jsonify(movies)

@app.route('/moviesdrive/search', methods=['GET'])
async def moviesdrive_search():
    query = request.args.get('query', default='', type=str)
    results = movies_drive.search(query)
    return jsonify(results)

@app.route('/moviesdrive/detail', methods=['GET'])
async def moviesdrive_quality_info():
    movie_id = request.args.get('id', default='', type=str)
    info = movies_drive.checker(movie_id)
    return jsonify(info)

@app.route('/moviesdrive/quality', methods=['GET'])
async def moviesdrive_get_stream():
    movie_id = request.args.get('id', default='', type=str)
    info = movies_drive.fetch_content_links(movie_id)
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
    trending_anime = gogo_anime.get_home()
    return jsonify(trending_anime)

@app.route('/gogoanime/search', methods=['GET'])
async def gogoanime_search():
    query = request.args.get('query', default='', type=str)
    results = gogo_anime.search_anime(query)
    return jsonify(results)

@app.route('/gogoanime/detail', methods=['GET'])
async def gogoanime_detail():
    anime_id = request.args.get('id', default='', type=str)
    info = gogo_anime.get_anime_details(anime_id)
    return jsonify(info)

@app.route('/gogoanime/episode', methods=['GET'])
async def gogoanime_episode():
    episode_id = request.args.get('id', default='', type=str)
    info = gogo_anime.get_episode_stream_urls(episode_id)
    return jsonify(info)

@app.route('/gogoanime/episode/download', methods=['GET'])
async def gogoanime_episode_download():
    episode_id = request.args.get('id', default='', type=str)
    info = gogo_anime.get_episode_download_urls(episode_id)
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
    info = torrent.search_all_sites(search_query, limit=limit)
    return jsonify(info)

@app.route('/torrent/search/site', methods=['GET'])
async def torrent_search_site():
    search_query = request.args.get('query', default='', type=str)
    limit = request.args.get('limit', default=2, type=int)
    site = request.args.get('site', default=None, type=str)
    if not site:
        return jsonify({"error": "The 'site' parameter is required."}), 400

    info = torrent.search_on_site(site, search_query, limit=limit)
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
#  TMDB ROUTES
#-------------------

@app.route('/tmdb')
async def tmdb_documentation():
    return await send_from_directory('docs', 'moviesdrive_doc.html')

@app.route('/tmdb/search', methods=['GET'])
async def tmdb_search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    try:
        results = tmdb.search_multi(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tmdb/fetch', methods=['GET'])
async def tmdb_get_seasons():
    media_id = request.args.get('id')
    if not media_id:
        return jsonify({"error": "Missing id parameter"}), 400
    try:
        structure = tmdb.get_seasons_episode_structure('tv', media_id)
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
    id = request.args.get('id', default=None, type=str)
    if not id:
        return jsonify({"error": "Movie ID is required"}), 400
    info = vidsrc.get_vidsrc_source(id)
    return jsonify(info)

@app.route('/vsc/vsrcme/movie', methods=['GET'])
async def get_vsrcme_movie():
    id = request.args.get('id', default=None, type=str)
    if not id:
        return jsonify({"error": "Movie ID is required"}), 400
    info = vidsrc.get_vsrcme_source(id)
    return jsonify(info)

@app.route('/vsc/vidsrc/tv', methods=['GET'])
async def get_vidsrc_tv():
    id = request.args.get('id', default=None, type=str)
    season = request.args.get('season', default=None, type=str)
    episode = request.args.get('episode', default=None, type=str)
    if not id or not season or not episode:
        return jsonify({"error": "TV show ID, season, and episode are required"}), 400
    info = vidsrc.get_vidsrc_source(id, season=season, episode=episode)
    return jsonify(info)

@app.route('/vsc/vsrcme/tv', methods=['GET'])
async def get_vsrcme_tv():
    id = request.args.get('id', default=None, type=str)
    season = request.args.get('season', default=None, type=str)
    episode = request.args.get('episode', default=None, type=str)
    if not id or not season or not episode:
        return jsonify({"error": "TV show ID, season, and episode are required"}), 400
    info = vidsrc.get_vsrcme_source(id, season=season, episode=episode)
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