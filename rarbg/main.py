import traceback
from datetime import datetime

from couchpotato import fireEvent
from couchpotato.core.logger import CPLog
from couchpotato.core.helpers.encoding import tryUrlencode
from couchpotato.core.helpers.variable import tryInt, getIdentifier
from couchpotato.core.media._base.providers.torrent.base import TorrentMagnetProvider
from couchpotato.core.media.movie.providers.base import MovieProvider

log = CPLog(__name__)


class Rarbg(TorrentMagnetProvider, MovieProvider):

    urls = {'base': 'http://torrentapi.org/pubapi_v2.php?%s',
            'docs': 'https://torrentapi.org/apidocs_v2.txt'}

    cat_ids = [
        (['45', '48'], ['720p']),
        (['44'], ['1080p']),
        (['42', '46'], ['bd50']),
        (['14', '17'], ['brrip', 'dvdrip']),
        (['47'], ['3d']),
    ]

    http_time_between_calls = 3
    _token = 0

    def _search(self, media, quality, results):
        hasresults = False
        self.get_token()

        cat_ids = self.getCatId(quality)

        params = {'mode': 'search',
                  'token': self._token,
                  'search_imdb': getIdentifier(media),  # search_imdb=tt2800038
                  'category': ';'.join(cat_ids),  # category=18;41
                  'min_seeders': self.conf('minimum_seeders', section='torrent'),
                  # 'min_leechers': config['min_leechers'],
                  'format': 'json_extended',
                  'app_id': 'couchpotato'}

        if self._token != 0:
            data = self.getJsonData(self.urls['base'] % tryUrlencode(params),
                                    headers=self.get_request_headers())
            if data:
                if 'error_code' in data:
                    if data['error'] == 'No results found':
                        log.debug('RARBG: No results returned from Rarbg')
                    elif data['error_code'] == 2:
                        log.error(data['error'])
                    else:
                        if data['error_code'] == 10:
                            log.error(data['error'], getIdentifier(media))
                        else:
                            log.error('RARBG: There is an error in the returned JSON: %s', data['error'])
                else:
                    hasresults = True
                try:
                    if hasresults:
                        for release in data['torrent_results']:
                            pubdate = release['pubdate']  # .strip(' +0000')
                            try:
                                pubdate = datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S +0000')
                                now = datetime.utcnow()
                                age = (now - pubdate).days
                            except ValueError:
                                log.debug('RARBG: Bad pubdate')
                                age = 0

                            results.append({
                                'id': release['download'].replace('magnet:?xt=urn:btih:', '').split('&')[0],
                                'name': release['title'],
                                'url': release['download'],
                                'detail_url': release['info_page'],
                                'size': tryInt(release['size']/1048576),  # rarbg sends in bytes
                                'seeders': tryInt(release['seeders']),
                                'leechers': tryInt(release['leechers']),
                                'age': tryInt(age),
                            })
                except RuntimeError:
                    log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))
            else:
                log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))

    def get_token(self):
        params = {'get_token': 'get_token',
                  'format': 'json',
                  'app_id': 'couchpotato'}
        tokendata = self.getJsonData(self.urls['base'] % tryUrlencode(params),
                                     headers=self.get_request_headers())
        if tokendata:
            try:
                token = tokendata['token']
                if self._token != token:
                    log.debug('RARBG: GOT TOKEN: %s', token)
                self._token = token
            except KeyError:
                log.error('RARBG: Failed getting token from Rarbg: %s', traceback.format_exc())
                self._token = 0

    def get_request_headers(self):
        return {'User-Agent': fireEvent('app.version', single=True)}
