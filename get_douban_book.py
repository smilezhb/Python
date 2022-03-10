# -*- coding:utf-8 -*-

from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options


if __name__ == '__main__':
    with open("douban_tag.txt", 'r', encoding='utf-8') as tag_file:
        tags = tag_file.readlines()
    # 创建 option 对象
    # 创建一个参数对象，用来控制chrome以无界面模式打开
    options = Options()
    options.add_argument('--headless')  # # 浏览器不提供可视化页面
    options.add_argument('--disable-gpu')  # 禁用GPU加速,GPU加速可能会导致Chrome出现黑屏，且CPU占用率高达80%以上
    # 规避检测
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    bro = webdriver.Chrome(options=options)
    bro.implicitly_wait(3)

    bro.get("https://accounts.douban.com/passport/login")
    bro.maximize_window()
    bro.find_element_by_class_name("account-tab-account").click()
    # 设置用户名
    bro.find_element_by_id('username').send_keys("15770793039")
    # 设置密码
    bro.find_element_by_id('password').send_keys("zhb150706032")
    # 点击登录
    bro.find_element_by_link_text("登录豆瓣").click()
    # 停留两秒
    time.sleep(2)
    print(1)
    # 定位iframe
    iframe = bro.find_element_by_id("tcaptcha_iframe")
    # 切换iframe
    bro.switch_to.frame(iframe)
    # 定位滑块
    yanzheng = bro.find_element_by_id("tcaptcha_drag_thumb")

    print(2)
    # 创建动作链对象
    action = ActionChains(bro)
    # 点击然后移动
    action.click(yanzheng).move_by_offset(xoffset=200, yoffset=0).perform()
    # 释放
    action.release().perform()
    # 停留三秒
    time.sleep(3)
    print(3)
    # 访问豆瓣图书
    bro.get("https://book.douban.com/")
    time.sleep(1)
    # 遍历图书标签
    for tag in tags:
        # https://book.douban.com/tag/推理?start=40
        # 遍历标签下的每一页
        tag = tag.strip()
        # 创建相应csv文件
        f = open(tag + ".csv", 'w', encoding='utf-8')
        # 当前页为0
        page_num = 0
        while True:
            bro.get('https://book.douban.com/tag/{}?start={}&type=T'.format(tag,page_num))
            print(bro.find_elements_by_class_name('pl2'))
            text = bro.find_elements_by_class_name('pl2')[0].text
            if "没有找到符合条件的图书" in text:
                break
            info_list = bro.find_elements_by_class_name('info')
            for info in info_list:
                infos = info.text.split('\n')
                f.write(",".join(infos) + '\n')
            page_num += 20
        f.close()
        print(tag,"图书全部爬取成功！")
    print("all over!")
    bro.quit()