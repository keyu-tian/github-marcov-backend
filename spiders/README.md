# 怎么爬

### 对于所有的 *_spider.py 注意：
1.  不能 import 任何 django model
2.  将爬到的数据存在 `SPIDER_DATA_DIRNAME` 这个路径下的某个文件夹中。（这个全局变量在 meta_config.py 中）
3.  最下方记得写 `if __name__ == '__main__': main()`
4.  如果想运行 *_spider.py，直接在 `spiders` 文件夹中 `python` 运行它就可以了。

### 对于所有的 *_importer.py 注意：
1.  可以 import django model 来插入或者更新数据库
2.  从 `IMPORTER_DATA_DIRNAME` 读取爬到的数据，注意不同于 `SPIDER_DATA_DIRNAME`（这个全局变量在 meta_config.py 中）
3.  使用 `.bulk_create` 函数可以批量插入，插入数据库的速度更快
4.  最下方记得**不要写** `if __name__ == '__main__': main()`
5.  记得**不要写全局的函数调用或者计算、读文件等**，而是把他们写在函数中。
6.  把整个 main() 函数命名为 `xxxx_import()`
6.  如果想运行 xxxx_importer.py，需要先在项目根文件夹 `python manage.py shell`，然后 `from spiders.xxxx_importer import xxxx_import`，然后调用 `xxxx_import()` 即可。

