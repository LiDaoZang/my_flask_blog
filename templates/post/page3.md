# docker配置kail容器# docker配置kail容器
- 配置docker的方法就不再在本文记录 
- 下面直接进入docker下kail的安装配置 
- 输入命令：
`docker pull kalilinux/kali-linux-docker`
- 从docker存储库 获取kail镜像后
- 启动镜像生产容器 
`Docker run -d -it 23f3rrwsfhgfnd2fd -p 2202:22 /bin/bash`
- 然后得到正在运行的kail容器
`Docker exec -it fdsf32f34f12e23r /bin/bash`
- 进入容器 
`apt-get update && apt-get install metasploit-framework`
- 安装msf 成功
- 接下来退出容器 
- 把配置好容器封装成镜像 
- 然后上传到自己的docker hub 存储库里
- 这样下次使用 就方便了 
- 当然要登陆自己的docker hub 账号 
`docker login Docker cmmint df3243r4fregre（ID号）kail(image-name)` 
- 接下来就是给镜像打标签了 
- 标签决定着 镜像存储在那个docker库项目里 
`Docker tag kail lisensen545123/mygame`
- 这次上传的项目名为lisensen545123/mygame
- 接下来就是上传了 
`docker push lisensen545123/mygame `2020/2/24
