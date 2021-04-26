#!/usr/bin/env
# coding: utf-8

from common import *

class IndexHandler(tornado.web.RequestHandler):


    fu = FileUtil()
    async def prepare(self):

        self.set_status(404)
        error_page_raw = open('./lib/http_error/404.html', 'r')
        error_page = error_page_raw.read()
        error_page_raw.close()
        self.write(
            error_page.format(self.fu.serverUrl)
        )
        self.finish()
        return

class SleepHandler(tornado.web.RequestHandler):
    async def get(self):
        # await asyncio.sleep(100)
        for i in range(0, 100000):
            await asyncio.sleep(1)
            Log.i(i)
        self.write('It works!')


class AsyncHttpHandler(tornado.web.RequestHandler):
    async def get(self):

        rs = MongoMixin.userDb.state.find()
        stateList = []
        async for i in rs:
            i['_id'] = str(i['_id'])
            stateList.append(i)

        resp =  {
                    'status': True,
                    'code': 2000,
                    'message': '',
                    'result': stateList
                }
        self.write(resp)

        #url = 'http://127.0.0.1:5000/'
        #client = httpclient.AsyncHTTPClient()
        #resp = await client.fetch(url)
        #self.finish(resp.body)


class GenHttpHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        url = 'http://127.0.0.1:5000/'
        client = httpclient.AsyncHTTPClient()
        resp = yield client.fetch(url)
        self.finish(resp.body)


class SyncHttpHandler(tornado.web.RequestHandler):
    async def get(self):
        url = 'http://127.0.0.1:5000/'
        resp = requests.get(url)
        self.finish(resp.text)


class App(tornado.web.Application):
    def __init__(self):
        settings = {
            'debug': True
        }
        super(App, self).__init__(
            handlers=[
                #(r'/', IndexHandler),
                #(r'/v2/async', AsyncHttpHandler),
                #(r'/gen', GenHttpHandler),
                #(r'/sync', SyncHttpHandler),
                #(r'/sleep', SleepHandler),
                (r'/web/api/bigbase/country', CountryHandler),
                (r'/web/api/sign/in', SignInHandler),
                (r'/web/api/sign/up', SignUpV2Handler),
                (r'/web/api/forms', FormsHandler),
                (r'/web/api/forms_data', FormsDataHandler),
            ],
            **settings,
            default_handler_class=IndexHandler
        )
        Log.i('APP', 'Running Tornado Application Port - [ {} ]'.format(WEB_SERVER_PORT))


if __name__ == '__main__':
    # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    # tornado_asyncio.AsyncIOMainLoop().install()

    # app = App()
    # server = httpserver.HTTPServer(app, xheaders=True)
    # server.listen(WEB_SERVER_PORT)
    # asyncio.get_event_loop().run_forever()

    app = App()
    app.listen(WEB_SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()


