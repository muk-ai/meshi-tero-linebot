import os
import json
import random
from pprint import pprint
import requests
import falcon

FLICKR_ENDPOINT_URI = 'https://api.flickr.com/services/rest/'
NUM_OF_PHOTOS = 20
MESHI_TERO_WORDS = [
  'カレー',
  '焼きおにぎり',
  'ラーメン',
  'チャーハン',
  '焼肉',
  'フォンダンショコラ',
  'ブリュレ',
  'パンケーキ',
  'ハンバーグ',
  'ハンバーガー',
  'お茶漬け',
  '卵かけごはん',
  '寿司',
  'pizza',
  '焼鳥',
  '豚汁',
  '麻婆豆腐',
  'からあげ',
]
LINEBOT_ENDPOINT_URI = 'https://trialbot-api.line.me/v1/events'

def get_image_and_thumbnail():
    params = {
        'method': 'flickr.photos.search',
        'api_key': os.environ['FLICKR_API_KEY'],
        'text': random.choice(MESHI_TERO_WORDS),
        'license': '1,2,3,4,5,6', # Creative Commons Lisense
        'per_page': NUM_OF_PHOTOS,
        'format': 'json',
        'nojsoncallback': '1',
        'privacy_filter': '1', # 1 public photos
        'content_type': '1', # 1 for photos only
        'sort': 'relevance'
    }

    resp = requests.get(FLICKR_ENDPOINT_URI, params=params)
    resp_json = resp.json()

    photo_info = random.choice(resp_json['photos']['photo'])
    tmp_url = 'https://farm%s.staticflickr.com/%s/%s_%s' % (photo_info['farm'], photo_info['server'], photo_info['id'], photo_info['secret'])
    image_url = tmp_url + '.jpg'
    thumbnail_url = tmp_url + '_m.jpg'
    return image_url, thumbnail_url

class Resource():
    def on_post(self, req, resp):
        body = req.stream.read()
        params = json.loads(body.decode('utf-8'))
        print(json.dumps(body.decode('utf-8'), indent=2))
        for msg in params['result']:
            image_url, thumbnail_url = get_image_and_thumbnail()
            data = {
                'to': [msg['content']['from']],
                'toChannel': 1383378250,  # Fixed value
                'eventType': '138311608800106203',  # Fixed value
                'content': {
                    'contentType': 2, # image
                    'toType': 1,
                    'originalContentUrl': image_url,
                    'previewImageUrl': thumbnail_url
                },
            }
            headers = {
                'Content-Type': 'application/json; charset=UTF-8',
                'X-Line-ChannelID': os.environ['LINE_CHANNEL_ID'],
                'X-Line-ChannelSecret': os.environ['LINE_CHANNEL_SECRET'],
                'X-Line-Trusted-User-With-ACL': os.environ['LINE_CHANNEL_MID']
            }
            r = requests.post(LINEBOT_ENDPOINT_URI, data=json.dumps(data), headers=headers)
            print(data)
            print(r.text)

        resp.status = falcon.HTTP_200

    def on_get(self, req, resp):
        image_url, thumbnail_url = get_image_and_thumbnail()

        resp.set_header('Content-Type', 'text/html')
        resp.status = falcon.HTTP_200
        resp.body = '<img src="%s"><br><img src="%s">' % (thumbnail_url, image_url)
