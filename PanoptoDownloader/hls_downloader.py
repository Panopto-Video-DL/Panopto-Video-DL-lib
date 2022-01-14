# Credits: https://github.com/justfoolingaround/hls-downloader

import re
import requests
import yarl
from Cryptodome.Cipher import AES
from pathlib import Path

ENCRYPTION_DETECTION_REGEX = re.compile(r"#EXT-X-KEY:METHOD=([^,]+),")
ENCRYPTION_URL_IV_REGEX = re.compile(
    r"#EXT-X-KEY:METHOD=(?P<method>[^,]+),URI=\"(?P<key_uri>[^\"]+)\"(?:,IV=(?P<iv>.*))?")

QUALITY_REGEX = re.compile(
    r'#EXT-X-STREAM-INF:.*RESOLUTION=\d+x(?P<quality>\d+).*\s+(?P<content_uri>.+)')
TS_EXTENSION_REGEX = re.compile(r"(?P<ts_url>.*\.ts.*)")


def get_extension(url):
    initial, _, extension = yarl.URL(url).name.partition('.')
    return extension


def def_iv(initial=1):
    while True:
        yield initial.to_bytes(16, 'big')
        initial += 1


default_iv_generator = def_iv()


def get_decrypter(key, *, iv=b''):
    if not iv:
        iv = next(default_iv_generator)
    return AES.new(key, AES.MODE_CBC, iv).decrypt


def unencrypted(m3u8_content):
    st = ENCRYPTION_DETECTION_REGEX.search(m3u8_content)
    return (not bool(st)) or st.group(1) == 'NONE'


def extract_encryption(m3u8_content):
    return ENCRYPTION_URL_IV_REGEX.search(m3u8_content).group('key_uri', 'iv')


def m3u8_generation(session_init, m3u8_uri):
    m3u8_uri_parent = yarl.URL(m3u8_uri).parent
    response = session_init(m3u8_uri)
    for quality, content_uri in QUALITY_REGEX.findall(response.text):
        url = yarl.URL(content_uri)
        if get_extension(url) == 'm3u8':
            if not url.is_absolute():
                content_uri = str(m3u8_uri_parent / content_uri)
            yield from m3u8_generation(session_init, content_uri)
        yield {'quality': quality, 'stream_url': content_uri}


def select_best(q_dicts, preferred_quality):
    return (
        sorted([
                q for q in q_dicts if get_extension(
                    q.get('stream_url')) in [
                    'm3u', 'm3u8'] and q.get(
                        'quality', '0').isdigit() and int(
                            q.get(
                                'quality', 0)) <= preferred_quality], key=lambda q: int(
                                    q.get(
                                        'quality', 0)), reverse=True) or q_dicts)


def hls_yield(session, m3u8_uri, preferred_quality):
    """
    hls_yield(session, 'https://example.com/hls_stream.m3u8', 1080) # Generator[dict]
    Returns
    ------
    A dictionary with 3 keys, `bytes`, `total` and `current`. 
    """
    streams = [
        *
        m3u8_generation(
            lambda s: session.get(s),
            m3u8_uri)]

    genexp = iter((_.get('stream_url') for _ in select_best(streams, preferred_quality)) or [m3u8_uri])

    ok = False
    while not ok:
        second_selection = next(genexp)
        content_response = session.get(second_selection)
        ok = content_response.status_code < 400

    m3u8_data = content_response.text

    relative_url = yarl.URL(second_selection.rstrip('/') + "/").parent

    encryption_uri, encryption_iv, encryption_data = None, None, b''
    encryption_state = not unencrypted(m3u8_data)

    if encryption_state:
        encryption_uri, encryption_iv = extract_encryption(m3u8_data)
        parsed_uri = yarl.URL(encryption_uri)
        if not parsed_uri.is_absolute():
            parsed_uri = relative_url.join(parsed_uri)
        encryption_key_response = session.get(str(parsed_uri))
        encryption_data = encryption_key_response.content

    all_ts = TS_EXTENSION_REGEX.findall(m3u8_data)
    last_yield = 0

    for c, ts_uris in enumerate(all_ts, 1):
        ts_uris = yarl.URL(ts_uris)
        if not ts_uris.is_absolute():
            ts_uris = relative_url.join(ts_uris)

        while last_yield != c:
            try:
                ts_response = session.get(str(ts_uris))
                ts_data = ts_response.content
                if encryption_state:
                    ts_data = get_decrypter(
                        encryption_data, iv=encryption_iv or b'')(ts_data)
                yield {'bytes': ts_data, 'total': len(all_ts), 'current': c}
                last_yield = c
            except requests.exceptions.HTTPError as e:
                print('ERROR: HLS downloading error due to {!r}, retrying.'.format(e))


def hls_downloader(m3u8_uri: str,
                   output: str,
                   headers: dict = None,
                   preferred_quality: int = 1080,
                   callback: callable = None):
    """
    Parameters
    ----------
    m3u8_uri: Input url for the stream
    output: Output file to which the stream is to be downloaded
    headers: Access headers for the stream
    preferred_quality: Preferred quality for downloading (if available)
    callback
    """
    if isinstance(output, str):
        output = Path(output)
    if headers is None:
        headers = {}
    session = requests.Session()
    session.headers.update(headers)

    with open(output, 'ab') as sw:
        for content in hls_yield(session, m3u8_uri, preferred_quality):
            sw.write(content.get('bytes'))
            if callable(callback):
                callback(int(content.get('current', 0) / content.get('total', 1) * 100))
