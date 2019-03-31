FROM zylhub/ubuntu16.04:cuda9-cudnn7-py3
MAINTAINER zylhub

ADD vim/vimrc_plug /root/.vimrc

# replace sources.list
ADD ./sources.list/ubuntu16.04-tsinghua /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y vim ctags python3 python3-pip curl git && apt-get clean all

# add vimrc
RUN curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
RUN cd ~/.vim/bundle/YouCompleteMe && git submodule update --init --recursive && ./install.py --clang-completer
RUN vim +PlugInstall +qall
RUN echo "vim done!"