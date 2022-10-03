# Python调用实现MSF漏洞搜索模块

<div class="has-toc have-toc">
</div>

## 0x00 需求

漏洞搜索模块：  
功能：搜索msf内置的攻击模块，返回模块的路径  
输入：service  
返回：  
{  
"service":"path"  
}  
难点：搜索服务的路径，优先返回远程代码执行等高危害，容易展示的漏洞

## 0x01 Metasploit API

Metasploit官方提供有RPC方式调用，即标准API调用。

<a rel="noreferrer noopener" href="https://docs.rapid7.com/metasploit/standard-api-methods-reference/" data-type="URL" data-id="https://docs.rapid7.com/metasploit/standard-api-methods-reference/" target="_blank" rel="nofollow" >RPC API 调用官方文档</a>

开启服务端API服务有两种方式：

  1. 通过msfconsole加载msfrpc插件来开启RPC
      * 打开msfconsole，输入`load msgrpc ServerHost=IP地址 ServerPort=端口 User=用户名 Pass=密码`<img loading="lazy" width="713" height="91" class="wp-image-1847" style="width: 600px;" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-114.png" alt="" />
  2. 通过msfrpcd服务来开启RPC
      * `msfrpcd -U 用户名 -P 密码 -S -f`<img loading="lazy" width="472" height="97" class="wp-image-1851" style="width: 600px;" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-115.png" alt="" /> 

<div class="wp-container-3 wp-block-group">
  <div class="wp-block-group__inner-container">
    <div class="wp-container-2 wp-block-columns">
      <div class="wp-container-1 wp-block-column">
        <p id="block-9ad91b23-1c22-4b83-b917-768135a0076b">
          msfrpcd的详细参数如下：
        </p>
      </div>
    </div>
  </div>
</div>

<pre class="wp-block-preformatted">Usage: msfrpcd &lt;options&gt;
OPTIONS:
       -P &lt;opt&gt;  设置RPC登录密码
       -S        在RPC socket上禁止使用SSL
       -U &lt;opt&gt;  设置RPC登录用户名
       -a &lt;opt&gt;  绑定一个IP地址（本机IP地址）
       -f        在后台以精灵进程（守护进程）的方式运行、启动
       -h        帮助菜单
       -n        禁止使用数据库
       -p &lt;opt&gt;  绑定某个端口，默认为55553
       -u &lt;opt&gt;  设置Web服务器的URI</pre>

与msf rpc api通信需要对通信的内容使用`msgpack`进行序列化，简单来说就是将要发送的数据包转换为二进制形式，以便于传输和格式统一。msgpack序列化之后的数据包支持多种语言，可以在msf服务端由ruby正常解析。

## 0x02 登录认证

## auth.login {#auth.login}

The auth.login method allows a username and password to be supplied which in turn grants the caller with a temporary authentication token. This authentication token expires five minutes after the last request made with it.

### Syntax {#syntax}

auth.login(String: Username, String: Password)

### Successful Request Example {#successful-request-example}

Client:

`[ "auth.login", "MyUserName", "MyPassword"]`

Server:

<pre class="wp-block-preformatted"><code>{ </code>
  <code>"result" =&gt; "success",</code>
 <code> "token" =&gt; "a1a1a1a1a1a…"</code>
<code>}</code>
<code>Token</code>是令牌码，一个随机字符串，是登录认证后的标识。</pre>

### Unsuccessful Request Example {#unsuccessful-request-example}

Client:

<pre class="wp-block-preformatted"><code>[ "auth.login", "MyUserName", "BadPassword"]</code></pre>

Server:

<pre class="wp-block-preformatted"><code>{</code>
  <code>"error" =&gt; true,</code>
  <code>"error_class" =&gt; "Msf::RPC::Exception",</code>
  <code>"error_message" =&gt; "Invalid User ID or Password"</code>
<code>}</code></pre>

<pre class="wp-block-code"><code>import msgpack
import http.client

HOST="127.0.0.1"
PORT="55553"
headers = {"Content-type" : "binary/message-pack"}

# 连接MSF RPC Socket
req = http.client.HTTPConnection(HOST, PORT)
options = &#91;"auth.login","msf","msf"]
# 对参数进行序列化（编码）
options = msgpack.packb(options)
# 发送请求，序列化之后的数据包
req.request("POST","/api/1.0",body=options,headers=headers)
# 获取返回
res = req.getresponse().read()
# 对返回进行反序列户（解码）
res = msgpack.unpackb(res)
res = res&#91;b'token'].decode()
print(res)</code></pre>

## 0x03 操作控制台

## Console {#Console}

The Console API provides the ability to allocate and work with the Metasploit Framework Console. In addition to being able to send commands and read output, these methods expose the tab completion backend as well being able to detach from and kill interactive sessions. Note that consoles provide the ability to do anything a local Metasploit Framework Console user may do, including running system commands.

下面简要介绍几种常用的函数

### console.create {#console.create}

The console.create method is used to allocate a new console instance. The server will return a Console ID ("id") that is required to read, write, and otherwise interact with the new console. The "prompt" element in the return value indicates the current prompt for the console, which may include terminal sequences. Finally, the "busy" element of the return value determines whether the console is still processing the last command (in this case, it always be false). Note that while Console IDs are currently integers stored as strings, these may change to become alphanumeric strings in the future. Callers should treat Console IDs as unique strings, not integers, wherever possible.

简单理解就是创建一个控制台实例。

Client:

<pre class="wp-block-preformatted"><code>[ "console.create", "&lt;token&gt;"]</code></pre>

Server:

<pre class="wp-block-preformatted"><code>{
 "id" =&gt; "0",
 "prompt" =&gt; "msf &gt; ",
 "busy" =&gt; false
 }</code></pre>

### console.destroy {#console.destroy}

The console.destroy method deletes a running console instance by Console ID. Consoles should always be destroyed after the caller is finished to prevent resource leaks on the server side. If an invalid Console ID is specified, the "result" element will be set to the string "failure" as opposed to "success".

销毁掉控制台实例。

Client:

<pre class="wp-block-preformatted"><code>[ "console.destroy", "&lt;token&gt;", "ConsoleID"]</code></pre>

Server:

<pre class="wp-block-preformatted"><code>{ "result" =&gt; "success" }</code></pre>

### console.list {#console.list}

The console.list method will return a hash of all existing Console IDs, their status, and their prompts.

Client:

<pre class="wp-block-preformatted"><code>[ "console.list", "&lt;token&gt;"]</code></pre>

Server:

<pre class="wp-block-preformatted"><code>{
 "0" =&gt; {
   "id" =&gt; "0",
   "prompt" =&gt; "msf exploit(\x01\x02\x01\x02handler\x01\x02) &gt; ",
   "busy" =&gt; false
   },
 "1" =&gt; {
   "id" =&gt; "1",
   "prompt" =&gt; "msf &gt; ",
   "busy" =&gt; true
   }
 }</code></pre>

### console.write {#console.write}

The console.write method will send data to a specific console, just as if it had been typed by a normal user. This means that most commands will need a newline included at the end for the console to process them properly.

在控制台写入命令。

Client:

<pre class="wp-block-preformatted"><code>[ "console.write", "&lt;token&gt;", "0", "version\n"]</code></pre>

Server:

<pre class="wp-block-preformatted"><code>{ "wrote" =&gt; 8 }</code></pre>

### console.read {#console.read}

The console.read method will return any output currently buffered by the console that has not already been read. The data is returned in the raw form printed by the actual console. Note that a newly allocated console will have the initial banner available to read.

读取控制台的输出

Client:

<pre class="wp-block-preformatted"><code>[ "console.read", "&lt;token&gt;", "0"]</code></pre>

Server:

<pre class="wp-block-preformatted">{
 "data" =&gt; "Framework: 4.0.0-release.14644[..]\n",
 "prompt" =&gt; "msf &gt; ",
 "busy" =&gt; false
 }</pre>

<p id="block-fb83e500-1208-4676-9f3b-1807dd369a3d">
  下面提供一个demo，调用MSF RPC登录获取<code>Token</code>之后创建实例，用户输入所需要查找的服务名称，拼接后发送命令到控制台，由msf服务端去执行。执行成功之后会将结果以序列化后的形式返回。反序列化之后成为一个dict，包含了返回后的结果。
</p>

<pre class="wp-block-code"><code>import msgpack
import http.client
import re
import json

HOST="127.0.0.1"
PORT="55553"
headers = {"Content-type" : "binary/message-pack"}

# 连接MSF RPC Socket
req = http.client.HTTPConnection(HOST, PORT)
options1= &#91;"auth.login","msf","msf"]
# 对参数进行序列化（编码）
options1= msgpack.packb(options1)
# 发送请求，序列化之后的数据包
req.request("POST","/api/1.0",body=options1,headers=headers)
# 获取返回
res1= req.getresponse().read()
# 对返回进行反序列户（解码）
res1= msgpack.unpackb(res1)
token= res1&#91;b'token'].decode('utf8')
options2= &#91;"console.create",token]
options2= msgpack.packb(options2)
req.request("POST","/api/1.0",body=options2,headers=headers)
# 获取返回
res2= req.getresponse().read()
# 对返回进行反序列户（解码）
res2= msgpack.unpackb(res2, strict_map_key=False)
id= res2&#91;b'id']
print("Please input thr service name:")
service= input()
options3= &#91;"console.write",token,id, "search "+service+"\n"]
options3= msgpack.packb(options3)
req.request("POST","/api/1.0",body=options3,headers=headers)
# 获取返回
res4= req.getresponse().read()
# 对返回进行反序列户（解码）
res4= msgpack.unpackb(res4, strict_map_key=False)
options4= &#91;"console.read",token,id]
options4= msgpack.packb(options4)
req.request("POST","/api/1.0",body=options4,headers=headers)
# 获取返回
res4= req.getresponse().read()
# 对返回进行反序列户（解码）
res4= msgpack.unpackb(res4, strict_map_key=False)
data=res4&#91;b'data'].decode('utf8')
print(data)</code></pre><figure class="wp-block-image size-large">

<img loading="lazy" width="1514" height="934" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-116.png" alt="" class="wp-image-1869" /> </figure> 

## 0x04 优化

创建类，引入正则匹配和json格式化输出。优先返回远程代码执行等高危害，容易展示的漏洞。

<pre class="wp-block-code"><code>import requests
import msgpack
import sys
import time
import re
import json

class Msfrpc:

  class MsfError(Exception):
    def __init__(self,msg):
      self.msg = msg
    def __str__(self):
      return repr(self.msg)

  class MsfAuthError(MsfError):
    def __init__(self,msg):
      self.msg = msg

  def __init__(self,opts=&#91;]):
    self.host = "127.0.0.1"# MSF的IP地址
    self.port = "55553"# 端口号
    self.uri = "/api/"# api默认使用/api/或/api/1.0
    self.ssl = False
    self.token = None
    self.headers = {"Content-type" : "binary/message-pack"}

  def encode(self, data):
    return msgpack.packb(data)

  def decode(self, data):
    return msgpack.unpackb(data)

  def call(self, method, opts=&#91;]):
    if method != 'auth.login':
      if self.token == None:
        raise self.MsfAuthError("MsfRPC: Not Authenticated")

    if method != "auth.login":
      opts.insert(0, self.token)
    
    if self.ssl == True:
      url = "https://%s:%s%s" % (self.host, self.port, self.uri)
    else:
      url = "http://%s:%s%s" % (self.host, self.port, self.uri)


    opts.insert(0, method)
    payload = self.encode(opts)
    
    r = requests.post(url, data=payload, headers=self.headers)
    opts&#91;:] = &#91;] # 清空opts列表
    
    return self.decode(r.content)

  def login(self, user, password):
    auth = self.call("auth.login", &#91;user, password])
    try:
      if auth&#91;b'result'] == b'success':
        self.token = auth&#91;b'token'].decode('utf8')
        return True
    except:
      raise self.MsfAuthError("MsfRPC: Authentication failed")

if __name__ == '__main__':
    client = Msfrpc({})# 创建一个新的默认配置的客户端实例
    
    client.login('msf','msf')# 使用密码msf登录msf
    try:
        res = client.call('console.create')
        console_id = res&#91;b'id']
    except:
        print ("Console create failed\r\n")
        sys.exit()
    service=&#91;'redis','mysql']# 定义服务列表
    service_path={}
    for i in range(0,len(service)):
      cmd="search "+service&#91;i]+"\n"# 构造命令
      client.call('console.write',&#91;console_id,cmd])
      # 使用msfrpc的api将命令写入控制台
      time.sleep(1)
      while True:
        res = client.call('console.read',&#91;console_id])
        # 使用msfrpc的api读取控制台的输出
        if len(res&#91;b'data']) &gt; 1:
                data=res&#91;b'data'].decode('UTF-8')
                filter_data=re.compile('exploit/\S*').findall(data)
                # 通过正则表达式过滤出exploit的漏洞
                service_path&#91;service&#91;i]]=&#91;]
                # 构造字典，将服务与漏洞的路径组成键值对
                for j in range(0,len(filter_data)):
                # 将list的data结果循环插入
                  service_path&#91;service&#91;i]].append(filter_data&#91;j])
        if res&#91;b'busy'] == True:
                time.sleep(1)
                continue
        break
    
    json_service_path=json.dumps(service_path ,indent=2)# 转换成json格式输出
    print(json_service_path)
    client.call('console.destroy',&#91;console_id])# 关闭控制台</code></pre><figure class="wp-block-image size-large">

<img loading="lazy" width="573" height="411" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-117.png" alt="" class="wp-image-1875" /> </figure> 

## 0x05 参考文献

<a href="https://github.com/dr0op/MsfRpcApi" target="_blank"  rel="nofollow" >https://github.com/dr0op/MsfRpcApi</a>

<a href="https://github.com/DanMcInerney/msfrpc/blob/master/msfrpc.py" target="_blank"  rel="nofollow" >https://github.com/DanMcInerney/msfrpc/blob/master/msfrpc.py</a>

<a href="https://docs.rapid7.com/metasploit/standard-api-methods-reference/" target="_blank"  rel="nofollow" >https://docs.rapid7.com/metasploit/standard-api-methods-reference/</a>
