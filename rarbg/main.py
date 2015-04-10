import traceback

from couchpotato.core.logger import CPLog
from couchpotato.core.helpers.encoding import tryUrlencode
from couchpotato.core.helpers.variable import getIdentifier
from couchpotato.core.media._base.providers.torrent.base import TorrentMagnetProvider
from couchpotato.core.media.movie.providers.base import MovieProvider

log = CPLog(__name__)


class Rarbg(TorrentMagnetProvider, MovieProvider):

    urls = {'base': 'https://rarbg.com/pubapi/pubapi.php?%s',
            'docs': 'https://rarbg.com/pubapi/apidocs.txt'}

    cat_ids = [
        (['45', '48'], ['720p']),
        (['44'], ['1080p']),
        (['42', '46'], ['bd50']),
        (['14', '17'], ['brrip', 'dvdrip']),
        (['47'], ['3d']),
    ]

    http_time_between_calls = 11

    def _search(self, media, quality, results):

        token = self.get_token()
        if not token:
            log.error('No token set. Exiting %s: %s', (self.getName(), traceback.format_exc()))

        cat_ids = self.getCatId(quality)

        params = {'mode': 'search',
                  'token': token,
                  'search_imdb': getIdentifier(media),  # search_imdb=tt2800038
                  'category': ';'.join(cat_ids),  # category=18;41
                  'min_seeders': self.conf('minimum_seeders', section='torrent'),
                  # 'min_leechers': config['min_leechers'],
                  'format': 'json'}

        data = self.getJsonData(self.urls['base'] % tryUrlencode(params), show_error=False)

        if isinstance(data, list):
            try:
                for release in data:

                    results.append({
                        'id': release['d'].replace('magnet:?xt=urn:btih:', '').split('&')[0],
                        'name': release['f'],
                        'url': release['d'],
                    })

            except KeyError:
                log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))
        else:
            log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))

    def get_token(self):
        # using rarbg.com to avoid the domain delay as tokens can be requested always
        params = {'get_token': 'get_token',
                  'format': 'json'}
        r = self.getJsonData(self.urls['base'] % tryUrlencode(params))
        token = None
        try:
            token = r.get('token')
        except ValueError:
            log.error('Could not retrieve RARBG token.')
        log.debug('RARBG token: %s' % token)
        return token
