# coding: utf-8
import wolframalpha
# from bs4 import BeautifulSoup, SoupStrainer
from .exceptions import APIError
from .clients import turingclient, baiduclient
from .utils import get_mac_address, get_audio_info


class Wolfram(object):
    """docstring for Wolfram"""
    def __init__(self, key):
        self.key = key

    def ask_wolfram(self, question):
        client = wolframalpha.Client(self.key)
        res = client.query(question)
        if len(res.pods) > 0:
            pod = res.pods[1]
            if pod.text:
                texts = pod.text
            else:
                raise APIError('Wolfram API failed.')
            # to skip ascii character in case of error
            # TODO: 取消换行，替换特殊字符
            texts = texts.encode('ascii', 'ignore')
            return texts
        else:
            raise APIError('Wolfram API failed.')


class TuringRobot(object):
    """docstring for TuringRobot"""
    def __init__(self, key):
        self.key = key

    def ask_turing(self, question):
        params = {
            'key': self.key,
            'info': question
        }
        ret = turingclient.query_turing(params)
        code = ret.get('code')
        if code == 100000:
            return ret['text'].encode('utf-8')
        else:
            raise APIError('Cannot handle this ret code: %s' % code)


class BaiduVoice(object):
    """docstring for BaiduVoice"""
    def __init__(self, token):
        self.token = token
        self.cuid = get_mac_address()

    def asr(self, file_, format_='wav',
            cuid=None, ptc=1, lan='zh'):
        if format_ != 'wav':
            raise ValueError('Unsupported audio format')
        params = {
            'format': format_,
            'token': self.token,
            'cuid': cuid or self.cuid,
            'ptc': ptc,
            'lan': lan
        }
        try:
            audio_info = get_audio_info(file_)
        except Exception, e:
            raise e
        params['len'], params['rate'] = audio_info['nframes'], audio_info['framerate']
        return baiduclient.asr(audio_info['content'], params)

    def tts(self, tex, lan='zh', ctp=1,
            cuid=None, spd=5, pit=5, vol=5, per=0):
        params = {
            'tex': tex,
            'lan': lan,
            'tok': self.token,
            'ctp': ctp,
            'cuid': cuid or self.cuid,
            'spd': spd,
            'pit': pit,
            'vol': vol,
            'per': per
        }
        return baiduclient.tts(params)

    @staticmethod
    def get_baidu_token(api_key, secret_key):
        params = {
            'grant_type': 'client_credentials',
            'client_id': api_key,
            'client_secret': secret_key
        }
        return baiduclient.get_token(params)


# def ask_baidupedia(question):
#     params = {
#         'word': question
#     }
#     ret = baiduclient.baidu_pedia(params)
#     if 'none' in ret.url:
#         raise APIError('Cannot find the answer')
#     else:
#         return content_filter(ret.content)


# def content_filter(content):
#     if 'lemma-summary' in content:
#         return _generate_answer(content)
#     elif 'list-dot list-dot-paddingleft' in content:
#         filter = SoupStrainer('li', class_='list-dot list-dot-paddingleft')
#         dom = BeautifulSoup(content, 'lxml', parse_only=filter)
#         try:
#             url = dom.find('a')['href']
#         except Exception, e:
#             raise RuntimeError('Cannot find the result')
#         ret, resp = _query(url)
#         if ret != RetCode.SUCCESS:
#             return resp
#         return _generate_answer(resp.content)
#     else:
#         logger.debug(content)
#         return u'内容不匹配'


# def _generate_answer(content):
#     filter = SoupStrainer('div', class_='lemma-summary')
#     try:
#         dom = BeautifulSoup(content, 'lxml', parse_only=filter)
#         answer = dom.find('div', class_='para').get_text()
#     except Exception, e:
#         raise RuntimeError('Cannot find the result')
#     return answer
