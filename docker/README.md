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
