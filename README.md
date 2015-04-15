##CouchPotatoServer Python builtins

###Get json data:

 * If fetched data not json exactly, use `show_error=False` param.
 
 ```python
 self.getJsonData(self.urls['search'], show_error=False)
 ```
 
```python
self.getJsonData(self.urls['search'])
```

###Get cache:

```python
from couchpotato.core.helpers.variable import md5

cache_key = md5(self.urls['search'])
url = self.urls['search'])
self.getCache(cache_key, url, show_error=False)
```

###Get provider settings:
 
 * If you want to get from couchpotatoserver.ini file use section param.
 
 ```python
 self.conf('minimum_seeders', section='torrent')
 ```
 
 it gets from:
 
 ```ini
 [torrent]
 minimum_seeders = 1
 ```

```python
self.conf('username')  # user_name_string
```

###Get IMDb id:

```python
from couchpotato.core.helpers.variable import getIdentifier

getIdentifier(media)  # tt2800038
```

###Get category ids:

```python
cat_ids = [
    (['45', '48'], ['720p']),
    (['44'], ['1080p']),
    (['42', '46'], ['bd50']),
    (['14', '17'], ['brrip', 'dvdrip']),
    (['47'], ['3d']),
]
self.getCatId(quality)  # you can get list: [45, 48]

';'.join(self.getCatId(quality))  # you can get ids: 45;48
```

###Get failed request count:
 
 * You can change failed requests.
 
 ```python
 self.http_failed_request[self.urls['hostname']] = 0
 ```

```python
self.http_failed_request
```