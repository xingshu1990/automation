# automation 工作用WEB自动化脚本
www.yun-caigou.com [云端采购网](https://raw.githubusercontent.com/xingshu1990/automation/main/yun-caigou.py)
-- 刚开始发布这个脚本的时候，没考虑python环境问题，
后来删除了自己电脑上的python，装了Anaconda后，
Windows 11中的【任务计划程序】未能找到这个.py文件，
于是把问题丢给chatgpt3.5.

chatgpt3.5推荐我【创建一个批处理文件（.bat文件）来自动切换到该环境并执行你的代码。】
于是以下是修改后的.bat文件：
不负责适配，只负责提供代码，
自行理解或者自行让chatgpt理解代码。

@echo off
chcp 65001
% 这块用于激活anaconda %
call "D:\anaconda3\Scripts\activate.bat" 
% 这块用于在cmd窗口打印：正在执行平台提示工具 %
echo 正在执行平台提示工具
% 理解成Windows的cmd下的目录切换 %
D:
% 同上 %
cd D:\py_demo
% 使用python执行D盘py_demo目录下的22.py文件 %
python D:\py_demo\22.py
% 退出anaconda %
call conda deactivate
pause

将其保存为.bat文件以后，
Windows下只是装了anaconda，anaconda 装了python，
并且确保anaconda 中的python装了相应的库，
那么就可以正常的让Windows自定执行代码了。
