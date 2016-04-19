import falcon
import linebot
import hello

application = falcon.API()
application.add_route('/callback', linebot.Resource())
application.add_route('/hello', hello.Resource())
