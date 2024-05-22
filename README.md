# 演唱会回流票监控程序

集齐大麦、猫眼、纷玩岛，票星球，4个平台的回流票监控

## 使用

### 一、源代码
```bash
# 克隆本项目
git clone https://github.com/ThinkerWen/TicketMonitoring.git
cd TicketMonitoring
# 安装python运行需要的包
python3 -m pip install -r requirements.txt
# 执行程序
python3 start.py
```
**程序默认没有用代理，若要添加代理请修改`Monitor.py`文件中的`_proxy`** (自建隧道代理查看GitHub：[https://github.com/ThinkerWen/ProxyServer](https://github.com/ThinkerWen/ProxyServer))

### 二、编译后的可执行文件

前往 [release](https://github.com/ThinkerWen/TicketMonitoring/releases) 下载最新的文件，下载后解压在`TicketMonitoring`目录下有 **回流票监控.exe** 文件，双击运行即可

**可执行程序没有用代理，若要添加代理请使用源代码方式**

<br>

## 添加监控演出

添加新的演出监控请在`TicketMonitoring`文件夹下的`config.json`中配置，

| 字段名       | 含义      | 备注                                                                |
|-----------|---------|-------------------------------------------------------------------|
| show_id   | 演出id    | 通过抓包获取，找到类似于`perfromId` `projectId` `showId` 等的关键字即可              |
| show_name | 演出名称    | 可以任意填写，自己好记即可                                                     |
| platform  | 演出的监控平台 | 和`show_id`的平台对应，`platform`参照：(`大麦: 0` `猫眼: 1` ` 纷玩岛: 2` `票星球: 3`) |
| deadline  | 监控的截止时间 | 截止时间内进行监控，超过截止时间则停止监控,许按照`2000-01-01 00:00:00`格式填写                |

<br>

# 赞助
**如若对您有用，望能给予我一点支持！**

| 微信                                                                                                                        | 支付宝                                                                                                                      |
|---------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| <img src="https://images.hive-net.cn/img/2024/05/22/664d92bf3e044.png" width="200" alt="wechat.png" title="wechat.png" /> | <img src="https://images.hive-net.cn/img/2024/05/22/664d932849164.png" width="200" alt="alipay.png" title="alipay.png" /> |


<br>

# 注意

程序仅供学习，请勿用于违法活动中，如作他用所承受的法律责任一概与作者无关

编程能力蒟蒻，代码仅供参考^_^

----

原文链接：<a href="https://bbs.kanxue.com/thread-279165.htm">[看雪] 某麦网回流票监控，sing参数分析</a>

原文链接：<a href="https://www.52pojie.cn/forum.php?mod=viewthread&tid=1845064&extra=page%3D1%26filter%3Dtypeid%26typeid%3D378">[吾爱破解] 某麦网回流票监控，sing参数分析</a>