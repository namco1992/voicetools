# voicetools
voicetools

500 不支持输入
501 输入参数不正确
502 token验证失败
503 合成后端错误


3300    输入参数不正确
3301    识别错误
3302    验证失败
3303    语音服务器后端问题
3304    请求 GPS 过大，超过限额
3305    产品线当前日请求数超过限额

format  sting   语音压缩的格式，请填写上述格式之一，不区分大小写
rate    int 采样率，支持 8000 或者 16000
channel int 声道数，仅支持单声道，请填写 1
cuid    string  用户唯一标识，用来区分用户，填写机器 MAC 地址或 IMEI 码，长度为60以内
token   string  开放平台获取到的开发者 access_token
ptc int 协议号，下行识别结果选择，默认 nbest 结果
lan string  语种选择，中文=zh、粤语=ct、英文=en，不区分大小写，默认中文
url string  语音下载地址
callback    string  识别结果回调地址
speech  string  真实的语音数据 ，需要进行base64 编码
len int 原始语音长度，单位字节


tex 合成的文本，使用UTF-8编码，请注意文本长度必须小于1024字节
lan 语言选择,填写zh
tok 开放平台获取到的开发者 access_token
ctp 客户端类型选择，web端填写1
cuid    用户唯一标识，用来区分用户，填写机器 MAC 地址或 IMEI 码，长度为60以内
spd 语速，取值0-9，默认为5中语速
pit 音调，取值0-9，默认为5中语调
vol 音量，取值0-9，默认为5中音量
per 发音人选择，取值0-1, 0为女声，1为男声，默认为女声