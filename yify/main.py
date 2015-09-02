import traceback

from couchpotato.core.helpers.variable import tryInt, getIdentifier
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider


log = CPLog(__name__)


class Yify(TorrentProvider, MovieProvider):

    urls = {
        'test': '%s/api/v2',
        'search': '%s/api/v2/list_movies.json?limit=50&query_term=%s',
        'api_docs': 'https://yts.to/api'
    }

    http_time_between_calls = 1  # seconds

    proxy_list = [
        'https://yts.im',
        'https://yts.to',
        'https://yify.ml',
        'https://yify.link',
        'https://yifytorrent.link',
        'https://yts.ch',
        'https://yts.click',
        'https://yify.me',
    ]

    def search(self, movie, quality):

        if not quality.get('hd', False):
            return []

        return super(Yify, self).search(movie, quality)

    def _search(self, movie, quality, results):

        domain = self.getDomain()
        if not domain:
            return

        search_url = self.urls['search'] % (domain, getIdentifier(movie))

        data = self.getJsonData(search_url) or {}
        data = data.get('data')

        if isinstance(data, dict) and data.get('movies'):
            try:
                for result in data.get('movies'):

                    for release in result.get('torrents', []):

                        if release['quality'] and release['quality'] not in result['title_long']:
                            title = result['title_long'] + ' ' + release['quality'] + '-YIFY'
                        else:
                            title = result['title_long'] + ' BRRip' + '-YIFY'

                        results.append({
                            'id': release['hash'],
                            'name': title,
                            'url': release['url'],
                            'detail_url': result['url'],
                            #'size': self.parseSize(release['size']),
                            'seeders': tryInt(release['seeds']),
                            'leechers': tryInt(release['peers']),
                        })

            except:
                log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))

    def correctProxy(self, data):
        data = data.lower()
        return 'yify' in data and 'yts' in data