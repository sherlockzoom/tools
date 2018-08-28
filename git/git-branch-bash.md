#  在Mac、Linux 终端显示 Git 当前所在分支

1. 进入你的`home`目录


 ```
 cd ~
 ```

1. 编辑`.bashrc`文件

 ```
 vi .bashrc
 ```

1. 将下面的代码加入到文件的最后处

 ```
 function git_branch {
    branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"
    if [ "${branch}" != "" ];then
        if [ "${branch}" = "(no branch)" ];then
            branch="(`git rev-parse --short HEAD`...)"
        fi
        echo " ($branch)"
    fi
 }
 
 export PS1='\u@\h \[\033[01;36m\]\W\[\033[01;32m\]$(git_branch)\[\033[00m\] \$ '
 ```
1. 保存退出
1. 执行加载命令

 ```
 source ./.bashrc
 ```

1. 完成


 >Mac 下面启动的 shell 是 login shell，所以加载的配置文件是`.bash_profile`，不会加载`.bashrc`。如果你是 Mac 用户的话，需要再执行下面的命令，这样每次开机后才会自动生效：

 ```
 echo "[ -r ~/.bashrc ] && source ~/.bashrc" >> .bash_profile
 ```
