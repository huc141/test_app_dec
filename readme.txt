操作步骤：

1、下载S3中的tar文件包，存放在本项目中的A1_S3_tar目录，或者你自定义的目录路径；

2、打开app_decry.js脚本，执行；

3、打开extract_json_dir.py脚本，先修改你的客户端类型（Android或iOS）、以及测试手机型号，然后执行脚本；

4、打开对应的Android或iOS目录，查看根据客户端类型和测试手机型号所拆分出来的埋点事件；



安卓查看terminalModel：
    adb shell getprop ro.product.model
