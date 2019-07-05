def app(environ, start_response):
    # bisness logic
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    body = environ['QUERY_STRING'].split('&')
    body = '\n'.join(body)
    body = bytes(body, encoding='utf-8')
    #1# "\n".join(environ.get('QUERY_STRING').split("&"))
    #2# m = [bytes(i + '\n', 'ascii') for i in data.split('&')]
    start_response(status, headers)
    return [body]