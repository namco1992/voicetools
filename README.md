# voicetools
voicetools: 语音识别和语音合成的基础包。
## 简介
以百度语音 API 为基础的语音识别和语音合成的基础包，同时集成了 wolfram API 和图灵机器人 API。附带树莓派语音助手示例代码。

## 用法
### 安装
```shell
pip install voicetools
```

### 语音识别及语音合成
```python
from voicetools import BaiduVoice
# api key 及 secret key 请在百度语音官方网站注册获取
token = BaiduVoice.get_baidu_token('YOUR_VOICE_API_KEY', 'YOUR_VOICE_SECRET')  # 该方法返回百度 API 返回的完整 json
bv = BaiduVoice(token['access_token'])  # 在上述方法获取的 json 中得到 access_token
# 语音识别
results = bv.asr('path/to/your/audio/file')  # 返回识别结果列表，可选参数见百度语音文档
# 语音合成
audio = bv.tts('你好')  # 返回 MP3 格式二进制数据，可选参数见百度语音文档
```

### wolfram API
wolfram 是一个功能强大的搜索引擎，可以直接返回问题的答案，而不是返回页面。
由于国内网络原因，接口稳定性差，且只支持英文搜索。
```python
from voicetools import Wolfram
# api key 请在 wolfram 网站注册获取
robot = Wolfram('YOUR_WOLFRAM_KEY')
result = robot.ask_wolfram('Who is Bill Gates?')  # 返回文字信息
```

### 图灵机器人 API
国产 AI 的 API。
```python
from voicetools import TuringRobot
# api key 请在图灵机器人网站注册获取
robot = TuringRobot('YOUR_TURING_KEY')
result = robot.ask_turing('给我讲个笑话')  # 返回文字信息
```

## 依赖
- requests
- wolframalpha

## 树莓派语音助手示例程序
请点击[这里](https://github.com/namco1992/voicetools/tree/master/examples/raspi_assistant)
