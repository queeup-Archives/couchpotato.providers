import traceback

from couchpotato.core.logger import CPLog
from couchpotato.core.helpers.encoding import tryUrlencode
from couchpotato.core.media._base.providers.torrent.base import TorrentMagnetProvider
from couchpotato.core.media.movie.providers.base import MovieProvider

log = CPLog(__name__)


class Strike(TorrentMagnetProvider, MovieProvider):

    urls = {'search': 'https://getstrike.net/api/v2/torrents/search/?category=Movies&phrase=%s'}

    cat_ids = [
        (['720p'], ['720p']),
        (['1080p'], ['1080p']),
        (['brrip'], ['brrip']),
        (['dvdrip'], ['dvdrip']),
    ]

    http_time_between_calls = 5

    def _searchOnTitle(self, title, media, quality, results):

        cat_ids = self.getCatId(quality)

        query = '%s %s %s' % (title.replace(':', '')
                              .replace(' s ', 's ')
                              .replace("'s ", "s "),
                              media['info']['year'],
                              cat_ids)
        search_url = self.urls['search'] % tryUrlencode(query)
        data = self.getJsonData(search_url) or {}

        if isinstance(data, dict) and data.get('torrents'):
            try:
                for release in data.get('torrents', []):

                    results.append({
                        'id': release['torrent_hash'],
                        'name': release['torrent_title'],
                        'url': release['magnet_uri'],
                        'detail_url': release['page'],
                        'size': int(release['size']) / 1024 / 1024,
                        'seeders': release['seeds'],
                        'leechers': release['leeches'],
                    })

            except KeyError:
                log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))
        else:
            log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))
