import requests
import re
import json
import win32api
import win32con

import subprocess
import importlib.util
import winsound
# 检查所需库是否已安装
def check_library(library_name):
    spec = importlib.util.find_spec(library_name)
    if spec is None:
        return False
    return True

# 安装缺失的库
def install_library(library_name):
    subprocess.call(['pip', 'install', library_name])

# 检查并安装缺失的库
def check_and_install_library(library_name):
    if not check_library(library_name):
        print(f'{library_name} 库未安装，正在尝试安装...')
        install_library(library_name)
        if check_library(library_name):
            print(f'{library_name} 库安装成功！')
        else:
            print(f'无法安装 {library_name} 库，请手动安装。')
            exit()

# 执行检查和安装所需的库
def main():
    libraries = ['requests', 're', 'json', 'win32api', 'win32con','winsound']
    for lib in libraries:
        check_and_install_library(lib)

class YunCaiGouAssistant:
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36',
        }
# 先获取formhash  nchash 两个字段 用于账号密码登录POST的时候，一起提交。
    def get_formhash_nchash(self):
        params = {
            'app': 'login',
            'wwi': 'index',
            'ref_url': '/mall/index.php?app=member&wwi=home',
        }
        response = self.session.get('http://yun-caigou.com/member/index.php', params=params, headers=self.headers, verify=False)
        html_data = response.text
        formhash_data = re.findall('<input type=\'hidden\' name=\'formhash\' value=\'(.*?)\' />', html_data)[0]
        nchash_data = re.findall('<input name="nchash" type="hidden" value="(.*?)" />', html_data)[0]
        return formhash_data, nchash_data
# 这部分是登录部分代码
    def login(self, formhash_data, nchash_data, username, password):
        params = {
            'app': 'login',
            'wwi': 'index',
        }
        data = {
            'formhash': formhash_data,
            'form_submit': 'ok',
            'nchash': nchash_data,
            'user_name': username,
            'password': password,
            'ref_url': '',
        }
        response = self.session.post('http://yun-caigou.com/member/index.php', params=params, headers=self.headers, data=data, verify=False)
# 这部分是获取【消息提醒】的json
    def fetch_messages(self):
        url = "http://yun-caigou.com/mall/index.php?app=member&wwi=ajax_store_msg"
        html = self.session.post(url).text
        return json.loads(html)['list']
# 这部分是解析【消息提醒】json数据，为了不让电脑以及网站承受过多压力，只抓取第一页5条内容。
    def display_messages(self):
        messages = self.fetch_messages()
        for msg in messages[:5]:
            addtime = msg['sm_addtime']
            content = msg['sm_content']
            data = '订单时间', addtime + "     " +  "标题", content
            
            win32api.MessageBox(0, str(data), "中化弘润平台信息提醒小助手", win32con.MB_ICONWARNING)
    
def main():
    #下方第一条为音频提示。
    winsound.Beep(1000, 2000)  # Beep(频率, 持续时间)
    assistant = YunCaiGouAssistant()
    formhash_data, nchash_data = assistant.get_formhash_nchash()
    #下方输入账号密码
    #参考格式 assistant.login(formhash_data, nchash_data, '137******', '12******')
    assistant.login(formhash_data, nchash_data, '账号', '密码')
    assistant.display_messages()
    

if __name__ == "__main__":
    main()
