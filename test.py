al/lib/python3.5/site-packages/urllib3/response.py", line 547, in _update_chunk_length
    raise httplib.IncompleteRead(line)
http.client.IncompleteRead: IncompleteRead(0 bytes read)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/requests/models.py", line 745, in generate
    for chunk in self.raw.stream(chunk_size, decode_content=True):
  File "/home/hung/.local/lib/python3.5/site-packages/urllib3/response.py", line 432, in stream
    for line in self.read_chunked(amt, decode_content=decode_content):
  File "/home/hung/.local/lib/python3.5/site-packages/urllib3/response.py", line 626, in read_chunked
    self._original_response.close()
  File "/usr/lib/python3.5/contextlib.py", line 77, in __exit__
    self.gen.throw(type, value, traceback)
  File "/home/hung/.local/lib/python3.5/site-packages/urllib3/response.py", line 320, in _error_catcher
    raise ProtocolError('Connection broken: %r' % e, e)
urllib3.exceptions.ProtocolError: ('Connection broken: IncompleteRead(0 bytes read)', IncompleteRead(0 bytes read))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "send_sms.py", line 139, in <module>
    coin.refresh()
  File "/home/hung/github/py_coin_watch/crypto/coin.py", line 62, in refresh
    self.exchange_conn.get_coin_data_json(self))  # except Exception as e:  #   print("Error Filling Data:", e)
  File "/home/hung/github/py_coin_watch/crypto/exchange.py", line 170, in get_coin_data_json
    json ,error = self.conn.get_markets()
  File "/home/hung/github/py_coin_watch/crypto/cryptopia_api.py", line 78, in get_markets
    return self.api_query(feature_requested='GetMarkets')
  File "/home/hung/github/py_coin_watch/crypto/cryptopia_api.py", line 51, in api_query
    req = requests.get(url, params=get_parameters)
  File "/usr/local/lib/python3.5/dist-packages/requests/api.py", line 72, in get
    return request('get', url, params=params, **kwargs)
  File "/usr/local/lib/python3.5/dist-packages/requests/api.py", line 58, in request
    return session.request(method=method, url=url, **kwargs)
  File "/usr/local/lib/python3.5/dist-packages/requests/sessions.py", line 508, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/local/lib/python3.5/dist-packages/requests/sessions.py", line 658, in send
    r.content
  File "/usr/local/lib/python3.5/dist-packages/requests/models.py", line 823, in content
    self._content = bytes().join(self.iter_content(CONTENT_CHUNK_SIZE)) or bytes()
  File "/usr/local/lib/python3.5/dist-packages/requests/models.py", line 748, in generate
    raise ChunkedEncodingError(e)
requests.exceptions.ChunkedEncodingError: ('Connection broken: IncompleteRead(0 bytes read)', IncompleteRead(0 bytes read))