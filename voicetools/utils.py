# coding: utf-8
import uuid
import wave
import urllib
from cStringIO import StringIO


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 11, 2)])


def get_audio_info(file_):
    try:
        f = wave.open(file_, 'rb')
        params = f.getparams()
        audio_info = {}
        audio_info['nchannels'], audio_info['sampwidth'], audio_info['framerate'], audio_info['nframes']\
            = params[:4]
        audio_info['content'] = f.readframes(audio_info['nframes'])
        f.close()
    except Exception, e:
        raise e
    return audio_info


def concat_url(url, params):
    return url + '?' + urllib.urlencode(params)

# def text_to_audio(text):  # tts
#     # get audio from redis
#     # if can't find in redis.
#     logger.debug('-----text to audio: ', text)
#     params = {
#         'tex': text,
#         'lan': 'zh',
#         'cuid': cuid,
#         'ctp': 1,
#         'tok': access_token,
#         'spd': 4,
#         'per': 0
#     }
#     rclient = get_rclient(text2audio_url)
#     ret, content = rclient.handle_text2audio(params)
#     if ret != RetCode.SUCCESS:
#         return ret
#     # TODO: save into redis
#     with open(os.path.join(Path.VOICE_DIR, receive_audio_file), 'w') as f:
#         f.write(content)
#     return RetCode.SUCCESS


# def audio_to_text():  # asr
#     url = audio2text_url % (cuid, access_token)
#     try:
#         f = wave.open(os.path.join(Path.VOICE_DIR, send_audio_file), 'rb')
#         params = f.getparams()
#         logger.debug('wave file params: %s', params)
#         nchannels, sampwidth, framerate, nframes = params[:4]
#         wave_data = f.readframes(nframes)
#         f.close()
#     except Exception, e:
#         logger.debug(traceback.format_exc())
#         return RetCode.SERVER_ERR, 'Sorry,something wrong,please try again.'
#     params = {
#         'voice_content': wave_data,
#         'length': nframes
#     }
#     rclient = get_rclient(url)
#     ret, content = rclient.handle_audio2text(params)
#     if ret != RetCode.SUCCESS:
#         return ret, 'Sorry,something wrong,please try again.'
#     return ret, content[0]


if __name__ == '__main__':
    pass
