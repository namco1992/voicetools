## 树莓派语音助手

### 简介
你的树莓派还在吃灰吗？来试试把它改造成语音助手吧！该示例程序基于 voicetools，遵循最简单的 one-in-one-out，只需要在该示例程序的基础上添加关键词和对应执行的动作，就可以扩展成为个性化的专属助手。
目前示例程序实现的功能有**语音提醒**及**今明两天天气预报查询**。

### 特性
- 使用 redis 作缓存，提升语音助手的反应速度。同样的问题，第二遍不再发生网络请求。
- 使用图灵机器人 API，除了预设功能外，所有问题都会有答案。
- 非常简单的“receive-process-execute-feedback”逻辑，易于扩展。
- 有一个心情阈值，目前是预设在配置文件中的。不一定会对你的命令言听计从。（只是为了好玩）

### 需要准备什么？
- 一块树莓派
- 一个麦克风
- 一个扬声器
- 一个传感器（用于唤醒语音助手，我使用的是声音传感器，当然任何传感器都可以）

### 使用方法
首先，安装 voicetools，可通过 pip 安装或直接通过源码安装。

```shell
pip install voicetools
// or
git clone git@github.com:namco1992/voicetools.git
```

安装依赖库：

```shell
jieba==0.38
PyAudio==0.2.9
redis==2.10.5
requests==2.11.0
RPi.GPIO==0.6.2
wolframalpha==2.4
```

如果你的树莓派的开发环境未经配置，可参考如下步骤：

```
// python 编译环境
sudo apt-get install python-dev

// 用于音频转换的 ffmpeg，该方法适用于取消了 ffmpeg 源的 RASPBIAN JESSIE
sudo sh -c 'echo "deb http://www.deb-multimedia.org jessie main" >> /etc/apt/sources.list'
sudo apt-get update
sudo apt-get install deb-multimedia-keyring
sudo apt-get install ffmpeg

// 音频相关
sudo apt-get install libjack-jackd2-dev portaudio19-dev
sudo apt-get install alsa-utils

// 系统声音设置
sudo modprobe snd_bcm2835

// 安装并启动 redis
...
```

硬件安装。将你的传感器接在 GPIO 上，我的信号输入是4,你可以自由修改，但是要记得修改配置文件中的信号输入端口。

参考`settings.py.example`设置你自己的配置文件`settings.py`，主要需要设置的参数如下：

```python
# BasicConfig 类中
LOCATION = '你的地址'  # 天气预报的地区
TURING_KEY = 'YOUR_TURING_KEY'  # 图灵机器人 key
VOICE_API_KEY = 'YOUR_API_KEY'  # 百度语音 api key
VOICE_SECRET = 'YOUR_API_SECRET'  # 百度语音 secret key

# BaiduAPIConfig 类中
API_KEY = 'YOUR_BAIDU_API_KEY'  # 天气预报使用了百度 APIStore 中的服务，需要百度 APIStore 的 key，你也可以选择任何你喜欢的服务提供商

# GPIOConfig 类中
VOICE_SENSOR = 4  # 修改成你的传感器信号输入口
```

Enjoy!

```shell
// cd 到示例程序目录
cd to/your/project/path
//建立 log 文件夹
mkdir log
// 运行
python assistant.py
```

## 如何扩展
1.在配置文件的`BasicConfig`类中的关键词列表`KEYWORDS`中加入你的关键词；
```python
KEYWORDS = {'提醒', '备忘录', '播放', '今天', '明天', '天气', '删除', '最后', '第一条'}
```
2.在`handler.py`的`FUNCTION_MAP`映射中加入你的关键词与执行方法名称的映射。比如你想在识别出关键词“明天”和“天气”后，对应执行天气查询的方法，方法名称是“weather_today”:
```python
FUNC_MAP = {
    Keyword(['今天', '天气']).value: 'weather_today'
}
```
3.在`handler.py`的`ActionHandler`中加入你需要执行的方法。
```python
class ActionHandler(object):

    @staticmethod
    def your_method(base_handler, result):
        """
        该类中的方法均是 staticmethod。
        args:
            base_handler: `BaseHandler`实例
            result: 语音识别内容
        returns:
            需要语音播放的内容或回答。
        """
        pass
```
4.大功告成。

## LICENCE
Apache 2.0
