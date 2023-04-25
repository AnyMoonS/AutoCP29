from selenium.webdriver.common.by import By
from selenium import webdriver
import pyttsx3
import json
import random
import time

# 加载配置文件
with open('./config.json', 'r') as f:
    config = json.load(f)

# 检查cookie
if len(config["cpp_cookies"]) == 0:
    print("\n输入L开始获取cookies,cookies将被用于账号登录")  # 不支持快捷登录（QQ登录等等）
    getcookies = input()
    if getcookies == "L":
        WebDriver = webdriver.Firefox()
        WebDriver.get("https://cp.allcpp.cn/#/ticket/detail?event=1074")
        print('\n=============================================')
        input("\n登录完成后请按任意键继续\n")
        config["cpp_cookies"] = WebDriver.get_cookies()
        with open('./config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("\ncookies 已保存,再运行一次脚本吧")
        exit(0)
    else:
        print("\n你不扣 L, 程序结束")
        exit(1)
engine = pyttsx3.init()


def voice():
    engine.setProperty('volume', 1.0)
    engine.say('抢到票了，速归！')
    engine.runAndWait()
    engine.stop()
    voice()


WebDriver = webdriver.Firefox()
WebDriver.get("https://cp.allcpp.cn/#/ticket/detail?event=1074")
WebDriver.maximize_window()
print("\n成功打开官网\n")
for cookie in config["cpp_cookies"]:  # 利用cookies登录账号
    WebDriver.add_cookie(
        {
            'domain': cookie['domain'],
            'name': cookie['name'],
            'value': cookie['value'],
            'path': cookie['path']
        }
    )
WebDriver.get("https://cp.allcpp.cn/#/ticket/detail?event=1074")
print("\n成功进入购票页\n")
while True:
    time.sleep(random.uniform(0.1, 1))
    currurl = WebDriver.current_url
    if "cp.allcpp.cn/#/ticket/detail" in currurl:
        try:
            ticket = WebDriver.find_element(
                By.XPATH,
                "//*[@id='root']/div/div[2]/div/div/div[1]/div/div[2]/div[1]/div/div[text()='DAY1 普通票']")  # 最后一项对应票的类型
            ticket.click()
            if ticket.get_attribute('class') == 'ticket-box disabled':
                print("无票")
                WebDriver.refresh()
                continue
            WebDriver.find_element(
                By.XPATH, "//*[@id='root']/div/div[2]/div/div/div[1]/div/div[2]/div[2]/button").click()
        except:
            print("无法购买")
            WebDriver.refresh()
    elif "cp.allcpp.cn/#/ticket/confirmOrder" in currurl:
        try:
            WebDriver.find_element(By.CLASS_NAME, "purchaser-info").click()
            WebDriver.find_element(
                By.XPATH, "//*[@id='root']/div/div[2]/div/div/button").click()
            print("下单中")
            voice()
        except:
            print("无法点击创建订单")
