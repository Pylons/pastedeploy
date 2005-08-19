def make_wsgiutils(host, port):
    from wsgiutils import wsgiServer
    def server(app):
        server = wsgiServer.WSGIServer(
            (host, int(port)), {'': app})
        server.serve_forever()
    return server
