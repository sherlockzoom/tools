 ## vlc rtsp 转 http ogg
 
 vlc版本： `3.0.4`
 
 > 摄像头获取rtsp流，通过vlc转http ogg

 
 `vlc -vvv rtsp://<your rtsp>--sout '#transcode{vcodec=theo,vb=800,acodec=vorb,ab=128,channels=2,samplerate=44100}:standard{access=http,mux=ogg,dst=:8082}`
