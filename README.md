# tuisec用于抓取tuisec的更新数据并写入数据库 #

- [x] 获取及时更新的内容
- [x] 写入数据库
- [x] 采用多进程+协程
- [x] 指定间隔时间执行

## 使用方法 ##
```
创建你的数据库，表名请命名为urls
create table urls(
url varchar(100) not null,
title varchar(100) not null,
id int not null auto_increment,
primary key(id))ENGINE=InnoDB DEFAULT CHARSET=utf8;

在config填写以下信息:
USERNAME='root' #mysql user
PASSWORD='root' #mysql passwd
HOST='localhost' #mysql host
DATABASE='xiao' #mysql database
PORT=3306 #mysql port
TIME=300 #selpp time start
```


## 结果 ##
![](https://s2.ax1x.com/2019/05/07/EyA2m4.md.png)

![](https://s2.ax1x.com/2019/05/07/EyEFBQ.png)

