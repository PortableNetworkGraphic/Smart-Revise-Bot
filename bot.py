import time
import json

import selenium.common
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc



class SMBot:

    def __init__(self, version: int, fullscreen: bool=False):

        self.driver = uc.Chrome(version_main=version)

        if fullscreen:
            self.driver.maximize_window()

    def wait(self):
        while True:
            time.sleep(1)

    def login(self, username, password):

        self.driver.get("https://smartrevise.online/Account/Login")

        self.driver.find_element(By.XPATH, '/html/body/div[1]/div/a').click()

        self.driver.find_element(By.XPATH, '//*[@id="Email"]').send_keys(username)

        self.driver.find_element(By.XPATH, '//*[@id="Password"]').send_keys(password)

        time.sleep(1)

        self.driver.find_element(By.XPATH, '//*[@id="btnLogin"]').click()

        self.driver.find_element(By.XPATH, '//*[@id="tile-117807"]').click()

        self.driver.find_element(By.XPATH, '//*[@id="modeSelQuiz"]/div/i').click()

        self.driver.find_element(By.XPATH, '//*[@id="lnkQuiz"]/a').click()

    def comp_questions(self):

        while True:

            time.sleep(1)

            a1 = self.driver.find_element(By.XPATH, '//*[@id="answercontainer"]/div[1]/a/div/div[2]')
            a2 = self.driver.find_element(By.XPATH, '//*[@id="answercontainer"]/div[2]/a/div/div[2]')
            a3 = self.driver.find_element(By.XPATH, '//*[@id="answercontainer"]/div[3]/a/div/div[2]')
            a4 = self.driver.find_element(By.XPATH, '//*[@id="answercontainer"]/div[4]/a/div/div[2]')

            given_answers = [a1, a2, a3, a4]

            question = self.driver.find_element(By.XPATH, '//*[@id="questiontext"]').text

            #Get database
            with open("answers.json", 'r') as file:
                answers = json.load(file)

            not_in_db = True

            try:

                not_next = True

                time.sleep(0.5)

                if a1.text in answers[question]:
                    a1.click()
                    not_in_db = False
                elif a2.text in answers[question]:
                    a2.click()
                    not_in_db = False
                elif a3.text in answers[question]:
                    a3.click()
                    not_in_db = False
                elif a4.text in answers[question]:
                    a4.click()
                    not_in_db = False
                else:
                    not_next = False

                while not_next:
                    try:
                        self.driver.find_element(By.XPATH, '//*[@id="lnkNext"]').click()
                        not_next = False
                    except: pass
                    try:
                        self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div[3]/button[1]').click()
                    except: pass


            except KeyError:
                pass


            if not_in_db:


                given_answerst = []
                for a in given_answers:
                    given_answerst.append(a.text)

                if question not in answers.keys() or answers[question] not in given_answerst:

                    time.sleep(1)

                    a1.click()

                    corr_answer = None

                    while corr_answer == None:

                        for count, answer in enumerate(given_answers):

                            if 'btn-success' in self.driver.find_element(By.XPATH,
                                                                         f'//*[@id="answercontainer"]/div[{count + 1}]/a').get_attribute(
                                'class'):
                                corr_answer = answer

                                break

                            try:
                                self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div[3]/button[1]').click()
                            except selenium.common.NoSuchElementException:
                                pass

                            try:
                                time.sleep(1)
                                a1.click()

                            except selenium.common.StaleElementReferenceException:
                                pass

                    if question not in answers.keys():
                        answers[question] = [corr_answer.text]
                    elif question in answers.keys() and corr_answer.text not in answers[question]:
                        answers[question].append(corr_answer.text)

                    with open("answers.json", 'w') as file:

                        json.dump(answers, file, indent=2)

            time.sleep(1)

            try:

                self.driver.find_element(By.XPATH, '//*[@id="lnkNext"]').click()

            except selenium.common.ElementClickInterceptedException: pass