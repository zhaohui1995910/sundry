**1、使用openssl制作 "auth.key" 文件**
- openssl rand -base64 756 > auth.key; 
- chmod 400 auth.key; 

**2、通过Dockerfile制作镜像：mongo-replset**

**3、启动docker-compose up -d**