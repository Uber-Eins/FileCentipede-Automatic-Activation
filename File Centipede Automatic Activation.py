import datetime
import os
from json import load,dump
from pyautogui import moveTo,click,hotkey,press
from pygetwindow import getWindowsWithTitle
from pyperclip import copy
from re import compile
from requests import get
from time import sleep

def GetActivationCodes():
    ActivationCodes = os.path.join(os.environ['APPDATA'], 'File Centipede', 'ActivationCodes.json')
    # 首先尝试从本地文件中读取激活码，如果文件存在并且包含当天日期的激活码，就直接返回它
    try:
        with open(ActivationCodes, 'r') as f:
            codes = load(f)
            today = datetime.date.today().strftime('%Y-%m-%d')
            for code in codes:
                if code["Validity Period"].startswith(today):
                    return code["ActivationCode"]
    except:
        codes = []
    
    try:
        url = 'https://filecxx.com/zh_CN/activation_code.html'
        response = get(url)
        html_content = response.text

        pattern = compile(r'(\d{4}-\d{2}-\d{2} 00:00:00 - \d{4}-\d{2}-\d{2} 00:00:00).*?\n(.+?)\n')

        results = pattern.findall(html_content)

        if results:
            for result in results:
                date = result[0]
                code = result[1]
                codes.append({"Validity Period": date, "ActivationCode": code})
            today_date = datetime.date.today()
            codes = [code for code in codes if datetime.datetime.strptime(code["Validity Period"][:10], '%Y-%m-%d').date() >= today_date]
            ActivationCodesDir = os.path.dirname(ActivationCodes)
            if not os.path.exists(ActivationCodesDir):
                os.makedirs(ActivationCodesDir)
            with open(ActivationCodes, 'w') as f:
                dump(codes, f, indent=2)
            for code in codes:
                if code["Validity Period"].startswith(today):
                    return code["ActivationCode"]
        else:
            print("没有找到符合条件的激活码")
            return None
        
    except Exception as e:
        print(e)
        return None
    
def InputActivationCode(WindowTitle,ActivationCode):
    try:
        # 查找指定标题的窗口
        target_window = getWindowsWithTitle(WindowTitle)[0]
        target_window.restore()  # 还原窗口
        target_window.activate()  # 激活窗口

        # 延时确保窗口激活
        sleep(0.15)

        # 计算输入框的中心位置
        input_box_x = (target_window.left + target_window.right) // 2
        input_box_y = (target_window.top + target_window.bottom) // 2 - 15

        # 移动鼠标到输入框中心并点击
        moveTo(input_box_x, input_box_y)
        click()

        # 清空输入框中的数据
        hotkey('ctrl', 'a')
        press('delete')

        # 将激活码复制到剪贴板
        copy(ActivationCode)

        # 粘贴激活码到输入框
        hotkey('ctrl', 'v')
        
        # 延时确保激活码输入完成
        sleep(0.15)

        # 计算确认按钮位置
        confirm_button_x = target_window.right - 60
        confirm_button_y = target_window.bottom - 30

        # 移动鼠标到确认按钮位置并点击
        moveTo(confirm_button_x, confirm_button_y)
        click()
        
        sleep(0.15)
        
        hotkey('enter')
    except IndexError:
        print(f"未找到标题为 '{WindowTitle}' 的窗口。")
    except Exception as e:
        print("发生错误:", e)

# 主进程
InputActivationCode("文件蜈蚣 - 激活码",GetActivationCodes())