# voicetools
## 简介
以百度语音 API 为基础的语音识别和语音合成的基础包，附带树莓派语音助手示例代码。

## 用法
```
from voicetools import BaiduVoice
# api key 及 secret key 请在百度语音官方网站注册获取
token = BaiduVoice.get_baidu_token('YOUR_VOICE_API_KEY', 'YOUR_VOICE_SECRET')
bv = BaiduVoice(token)
# 语音识别
results = bv.asr('path/to/your/audio/file')  # 返回识别结果列表
# 语音合成
audio = bv.tts('你好')  # 返回 MP3 格式二进制数据
```

## 依赖
- requests
- wolframalpha
