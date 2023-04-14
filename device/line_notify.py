import requests


class LineNotify:
    def __init__(self, token):
        self._session = requests.Session()
        self.auth = 'Bearer {}'.format(token)
        self.header = {'Authorization': self.auth}

    def send_msg(self, msg):
        _data = {'message': msg}
        response = self._session.post('https://notify-api.line.me/api/notify', data=_data, headers=self.header)
        print('[send_msg] status_code: {}  X-RateLimit-Remaining: {}'
              .format(response.status_code, response.headers['X-RateLimit-Remaining']))

    def send_pic(self, msg, pic):
        _data = {'message': msg}
        response = self._session.post('https://notify-api.line.me/api/notify', data=_data,
                                      files={'imageFile': pic}, headers=self.header)
        print('[send_pic] status_code: {}  X-RateLimit-ImageRemaining: {}'
              .format(response.status_code, response.headers['X-RateLimit-ImageRemaining']))


if __name__ == "__main__":
    # Change to your Line Notify Token
    notify = LineNotify('your-token')
    notify.send_msg('Hello World')
    pic = requests.get(
        'https://line.me/static/b83de682148ca1092750bd59456ca0d9/5b953/329473e988bb3cab682a5b5bd46b47dc.png')
    notify.send_pic('LINE', pic.content)
