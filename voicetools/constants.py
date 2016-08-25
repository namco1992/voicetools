# coding: utf-8
from .exceptions import RecognitionError, VerifyError, QuotaError, APIError


class BaiduUrl(object):
    token_url = 'https://openapi.baidu.com/oauth/2.0/token'
    tts_url = 'http://tsn.baidu.com/text2audio'
    asr_url = 'http://vop.baidu.com/server_api'
    baike_url = 'http://baike.baidu.com/search/word'


# turing robot config
class TuringUrl(object):
    turing_url = 'http://www.tuling123.com/openapi/api'


# error no
class ErrNo(object):
    tts_err_no = {
        500: ValueError,
        501: ValueError,
        502: VerifyError,
        503: APIError
    }
    asr_err_no = {
        3300: ValueError,
        3301: RecognitionError,
        3302: VerifyError,
        3303: APIError,
        3304: QuotaError,
        3305: QuotaError
    }
