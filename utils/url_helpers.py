import urllib.parse


def url_with_get_params(url, params):
    return f"{url}?{urllib.parse.urlencode(params)}"
