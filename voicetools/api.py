# coding: utf-8
import wolframalpha
from .exceptions import APIError
from .clients import turingclient, baiduclient
from .utils import get_mac_address, get_audio_info


class Wolfram(object):
    """A client for request Wolfram.

    Attributes:
        key: The key string got from https://www.wolframalpha.com.
    """
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
            texts = texts.encode('ascii', 'ignore')
            return texts
        else:
            raise APIError('Wolfram API failed.')


class TuringRobot(object):
    """A client for request Turing Robot.

    Attributes:
        key: The key string got from http://www.tuling123.com.
    """
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
    """A client for request Turing Robot.

    Attributes:
        token: The token string got from https://openapi.baidu.com/oauth/2.0/token.
        cuid: Unique identification of user, default is MAC address.
    """
    def __init__(self, token):
        self.token = token
        self.cuid = get_mac_address()

    def asr(self, file_, format_='wav',
            cuid=None, ptc=1, lan='zh'):
        """Constructs and sends an Automatic Speech Recognition request.

        Args:
            file_: the open file with methods write(), close(), tell(), seek()
                   set through the __init__() method.
            format_:(optional) the audio format, default is 'wav'
            cuid:(optional) Unique identification of user, default is MAC address.
            ptc:(optional) nbest results, the number of results.
            lan:(optional) language, default is 'zh'.
        Returns:
            A list of recognition results.
        Raises:
            ValueError
            RecognitionError
            VerifyError
            APIError
            QuotaError
        """
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
        """Constructs and sends an Text To Speech request.

        Args:
            tex: The text for conversion.
            lan:(optional) language, default is 'zh'.
            ctp:(optional) Client type, default is 1.
            cuid:(optional) Unique identification of user, default is MAC address.
            spd:(optional) speed, range 0-9, default is 5.
            pit:(optional) pitch, range 0-9, default is 5.
            vol:(optional) volume, range 0-9, default is 5.
            per:(optional) voice of male or female, default is 0 for female voice.
        Returns:
            A binary string of MP3 format audio.
        Raises:
            ValueError
            VerifyError
            APIError
        """
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
        """Get Baidu Voice Service token by api key and secret.

        Functions of other args of response are not confirmed, so the whole
        response dict will be returned, you can access the token by ret['access_token'].
        """
        params = {
            'grant_type': 'client_credentials',
            'client_id': api_key,
            'client_secret': secret_key
        }
        return baiduclient.get_token(params)
