import falcon
import json

class Resource:
    def on_get(self, req, resp):
        msg = {
            "messages": "hello, world"
        }
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(msg)
