## docker images

https://hub.docker.com/r/zylhub

## detectron docker image build

相关文件：

1. dockerfile: https://github.com/zylhub/misc/blob/master/docker/dockerfile-tectron-cn
2. pip.conf: https://github.com/zylhub/misc/blob/master/docker/pip.conf
3. ubuntu16.04-aliyun-sources-list: https://github.com/zylhub/misc/blob/master/docker/ubuntu16.04-aliyun-sources-list

`docker build -t zylhub/detectron-cn:cuda9-cudnn7 .`

+ 添加中文支持
+ 添加ubuntu16.04阿里源
+ 添加pip 阿里源
+ 使用gitee替换git库


## Ubuntu 16.04+、Debian 8+、CentOS 7

对于使用 systemd 的系统，请在 `/etc/docker/daemon.json` 中写入如下内容（如果文件不存在请新建该文件）
```
{
  "registry-mirrors": [
    "https://registry.docker-cn.com"
  ]
}

```

注意，一定要保证该文件符合 json 规范，否则 Docker 将不能启动。

之后重新启动服务。
```
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```

## 参考
https://yeasy.gitbooks.io/docker_practice/install/mirror.html
