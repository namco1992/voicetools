# coding: utf-8
import uuid
import wave
import urllib


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


if __name__ == '__main__':
    pass
