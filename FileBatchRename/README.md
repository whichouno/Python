文件批量重命名

说明：
  适用于文件名中有阿拉伯数字的顺序编号，如多个视频文件。

使用：
  python3 BatchRename.py 'path' pattern' 'newfilename' 或者
  python3 BatchRename.py --path='path' --pattern='pattern' --newfilename='newfilename'

  path：待重命名文件的所在路径。
  pattern：待重命名文件名中顺序编号的正则表达式。正则中顺序编号需要使用第一个分组。
  newfilename：新文件名，不含扩展名。其中使用 * 或者 多个* 来标识新文件名中顺序编号的位置。

  单个*：使用原顺序编号
  多个*：在原顺序编号的基础上，右对齐左补'0'，长度为*的个数。若*个数小于原顺序编号长度，则使用原顺序编号。

示例：
  重命名前：
    /User/test/example/movie_dd-EP1.mp4
    /User/test/example/season4.EP2.hd.mp4
    /User/test/example/hd720_EP03[new].mp4

  执行：
    python3 BatchRename.py '/User/test/example' 'EP(\d{1,2})' 'movie_**' 或者
    python3 BatchRename.py --original_path='/User/test/example' --id_pattern='EP(\d{1,2})' --newfilename_format='movie_**'

  重命名后：
    /User/test/example/movie_01.mp4
    /User/test/example/movie_02.mp4
    /User/test/example/movie_03.mp4
