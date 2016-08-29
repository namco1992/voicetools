# coding: utf-8
import json
import requests
from .constants import BaiduUrl, TuringUrl, ErrNo
from .exceptions import RespError, APIError, VerifyError
from .utils import concat_url


class BaseClient(object):
    """BaseClient for requesting APIs."""

    def __init__(self, **kwargs):
        self.connect_timeout = kwargs.get('connect_timeout', 5)
        self.request_timeout = kwargs.get('request_timeout', 30)

    def post_request(self, url, params, headers=None, connect_timeout=None, request_timeout=None):
        connect_timeout = connect_timeout or self.connect_timeout
        request_timeout = request_timeout or self.request_timeout
        try:
            resp = requests.post(
                url=url,
                data=params,
                headers=headers,
                timeout=(connect_timeout, request_timeout)
                )
        except Exception, e:
            raise e
        else:
            if resp.status_code != 200:
                raise RespError('The resp status code is %s' % resp.status_code)
            else:
                return resp

    def get_request(self, url, params, headers=None, connect_timeout=None, request_timeout=None):
        connect_timeout = connect_timeout or self.connect_timeout
        request_timeout = request_timeout or self.request_timeout
        try:
            resp = requests.get(
                url=url,
                params=params,
                headers=headers,
                timeout=(connect_timeout, request_timeout)
                )
            return resp
        except Exception, e:
            raise e
        else:
            if resp.status_code != 200:
                raise RespError('The resp status code is %s' % resp.status_code)
            else:
                return resp


class BaiduClient(BaseClient):
    """Client for handling the process of Baidu Voice requests."""
    def __init__(self, **kwargs):
        super(BaiduClient, self).__init__(**kwargs)

    def get_token(self, params):
        try:
            resp = self.get_request(BaiduUrl.token_url, params)
        except Exception, e:
            raise e
        else:
            r = resp.json()
            if 'error' in r:
                raise VerifyError(r.get('error_description', 'unknown error'))
            return r

    def tts(self, params):
        try:
            resp = self.get_request(BaiduUrl.tts_url, params)
        except Exception, e:
            raise e
        content_type = resp.headers.get('Content-type')
        if content_type == 'application/json':
            response = resp.json()
            err_msg = 'err_msg: %s' % response.get('err_msg', 'baidu tts service error')
            raise ErrNo.tts_err_no.get(response['err_no'], APIError)(err_msg)
        elif content_type == 'audio/mp3':
            return resp.content
        else:
            raise APIError('baidu tts service unknown error')

    def asr(self, speech, params):
        headers = {
            'Content-Type': 'audio/%s;rate=%s' % (params.pop('format'), params.pop('rate')),
            'Content-length': str(params.pop('len'))
        }
        url = concat_url(BaiduUrl.asr_url, params)
        try:
            resp = self.post_request(url, speech, headers=headers)
            print params, resp.json()
        except Exception, e:
            raise e
        response = resp.json()
        if response.get('err_no') != 0:
            err_msg = 'err_msg: %s' % response.get('err_msg', 'baidu asr service error')
            raise ErrNo.asr_err_no.get(response['err_no'], APIError)(err_msg)
        else:
            return response.get('result')

    def baidu_pedia(self, params):
        try:
            resp = self.get_request(url=BaiduUrl.baike_url, params=params)
        except Exception, e:
            raise e
        return resp

baiduclient = BaiduClient()


class TuringClient(BaseClient):
    """Client for handling the process of Turing requests."""
    def __init__(self, **kwargs):
        super(TuringClient, self).__init__(**kwargs)

    def query_turing(self, params):
        try:
            resp = self.get_request(url=TuringUrl.turing_url, params=params)
        except Exception, e:
            raise e
        return resp.json()

turingclient = TuringClient()
