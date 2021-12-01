# Hambloger
 A blog in Computer Science Introduction course.

2021/10/25<br>
Adding the basic web pages, including 404 page and 500 page.<br>
Not advanced yet...

2021/11/9

可以通过邮箱Leo@233.com与密码cat登录了

## 如何使用

1. 安装python=3.9并配置pip国内源

   配置pip国内源具体方法：

   1. Win+R 输入 %HOMEPATH% 回车
   2. 在该文件夹下创建pip文件夹，并在该文件夹中创建pip.ini文件，输入以下内容：

   ``` ini
   [global]
   index-url = https://pypi.tuna.tsinghua.edu.cn/simple
   [install]
   trusted-host = https://pypi.tuna.tsinghua.edu.cn
   ```

   

1. 安装flask

   ``` cmd
   pip install flask
   ```

   

2. 安装依赖

   ``` cmd
   pip install -r requirements.txt
   ```

   

3. 切换默认启动文件

   ``` cmd
   set FLASK_APP=hambloger.py
   ```

4. 运行

   ``` cmd
   flask run
   ```

   

