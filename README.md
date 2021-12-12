# Hambloger
 A blog in Computer Science Introduction course.


## 更新日志

* 2021/10/18 **踌躇满志地创建了项目**
* 2021/11/10 **完成登录,注册功能**
* 2021/11/28 **完成登录,注册,首页的界面优化**
* 2021/11/30 **完成编辑个人资料功能**
* 2021/12/1  **完成发表文章功能**
* 2021/12/2  **完成关注功能**
* 2021/12/7  **完成个人主页的优化**
* 2021/12/9  **完成编写文章界面优化**
* 2021/12/12 **完成关注界面** 
* 2021/12/10--2021/12/12 **疯狂的修补bug以及完善界面**

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

   

