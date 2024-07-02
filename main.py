from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import re


class Web:
    def __init__(self, url):
        self.url = url
        self.scores = []
        options = webdriver.ChromeOptions()
        self.web = webdriver.Chrome(service=Service(r"D:\Desktop\绩点自动计算\chromedriver.exe"), options=options)
        # 修改浏览器指纹防止检测
        self.web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
            """
        })
        self.web.implicitly_wait(10)

    def login(self, username, password):
        self.web.get(self.url)
        sleep(0.2)

        login_button1 = self.web.find_element(By.XPATH, '//*[@id="ampHasNoLogin"]')
        login_button1.click()
        sleep(0.2)

        username_input = self.web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/span[1]/input')
        password_input = self.web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/span[2]/input')
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button2 = self.web.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/button')
        login_button2.click()
        sleep(5)

    def get_score(self):
        self.web.get('https://ehall.seu.edu.cn/appShow?appId=4768574631264620')
        pages = self.web.find_element(By.XPATH, '//*[@id="pagerdqxq-index-table"]/div/div/div[1]/span[2]').text
        pages = int(pages.split()[-1])
        total = self.web.find_element(By.XPATH, '//*[@id="pagerdqxq-index-table"]/div/div/div[1]/span[1]').text
        total = int(total.split()[-1])
        for i in range(pages):
            n = 10 if i != pages - 1 else total % 10
            for j in range(n):
                self.scores.append(ScoreLine(self.web.find_element(By.XPATH, f'//*[@id="row{j}dqxq-index-table"]')))
                sleep(0.05)
            if n != 10:
                break
            next_button = self.web.find_element(By.XPATH, '//*[@id="pagerdqxq-index-table"]/div/div/div[1]/a[3]')
            next_button.click()
            sleep(0.5)
        sleep(1)

    def count_GPA(self):
        total_credits = 0.0
        credit_score = 0.0
        total_score = 0.0
        for score in self.scores:
            #  跳过通选课
            if score.info['课程代码'][:3] == 'B00':
                continue
            print(score.info, self.trans_score(score.info['打分方式'], score.info['成绩']), self.trans_GPA(score.info['打分方式'], score.info['成绩']))
            total_credits += float(score.info['学分'])
            total_score += self.trans_score(score.info['打分方式'], score.info['成绩']) * float(score.info['学分'])
            credit_score += self.trans_GPA(score.info['打分方式'], score.info['成绩']) * float(score.info['学分'])
        print(f'计入绩点课程中已修学分{total_credits}, 平均学分绩：{credit_score / total_credits}, 加权平均分：{total_score / total_credits}')

    def trans_score(self, mode, score):
        #  成绩换算分数
        a = {'优': 95.0, '良': 85.0, '中': 75.0, '及格': 65.0}
        if mode == "五级制":
            return a[score]
        else:
            return float(score)

    def trans_GPA(self, mode, score):
        #  分数换算绩点
        score = self.trans_score(mode, score)
        if score >= 96:
            return 4.8
        elif score >= 93:
            return 4.5
        elif score >= 90:
            return 4.0
        elif score >= 86:
            return 3.8
        elif score >= 83:
            return 3.5
        elif score >= 80:
            return 3.0
        elif score >= 76:
            return 2.8
        elif score >= 73:
            return 2.5
        elif score >= 70:
            return 2.0
        elif score >= 66:
            return 1.8
        elif score >= 63:
            return 1.5
        elif score >= 60:
            return 1.0
        else:
            return 0.0


class ScoreLine:
    def __init__(self, line):
        self.line = line
        self.html = line.get_attribute('innerHTML')
        self.pattern = re.compile("<span.*?title=.*?>(.*?)</span>", re.S)
        self.grade_pattern = re.compile('<td role="gridcell" style="pointer-events: none; visibility: hidden; border-color: transparent; max-width:100px; width:100px;" class="jqx-cell jqx-grid-cell jqx-item jqx-center-align">(.*?)</td>', re.S)
        self.grade = self.grade_pattern.search(self.html).group(1)
        if len(self.grade) > 3:
            self.grade_pattern = re.compile('<div class="zcjsfjg"><span>(.*?)</span></div>', re.S)
            self.grade = self.grade_pattern.search(self.grade).group(1)
        self.score = self.pattern.findall(self.html)
        self.info = {
            '学期': self.score[0],
            '课程名称': self.score[1],
            '课程代码': self.score[2],
            '学分': self.score[6],
            '打分方式': self.score[27],
            '成绩': self.grade
        }


if __name__ == '__main__':
    web = Web("https://ehall.seu.edu.cn/new/index.html")
    web.login(" 一卡通号", "密码")
    web.get_score()
    web.count_GPA()
