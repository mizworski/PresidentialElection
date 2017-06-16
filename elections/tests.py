# coding=utf-8
from django.test import TestCase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium import webdriver


class TestCountry(TestCase):
    def testRegisterLogin(self):
        driver = webdriver.Chrome()
        self.register(driver)
        self.login(driver)
        self.openCommunitySubpage(driver)
        self.validateVotesNumber(driver)
        self.resetVotes(driver)
        self.changeVotesNumber(driver)
        driver.close()

    def register(self, driver):
        driver.get('http://localhost:8000')
        logout_button = driver.find_element_by_id('logout_button')
        logout_button.click()
        register_link = driver.find_element_by_name('register')
        register_link.click()

        username_box = driver.find_element_by_name('username')
        password_box = driver.find_element_by_name('password')
        username_box.send_keys('testowy_uzytkownik_123')
        password_box.send_keys('dupa123')

        submit_button = driver.find_element_by_tag_name('button')
        submit_button.click()

    def login(self, driver):
        driver.get('http://localhost:8000')
        login_link = driver.find_element_by_name('login')
        login_link.click()

        username_box = driver.find_element_by_name('username')
        password_box = driver.find_element_by_name('password')
        username_box.send_keys('testowy_uzytkownik_123')
        password_box.send_keys('dupa123')
        submit_button = driver.find_element_by_tag_name('button')
        submit_button.click()

    def openCommunitySubpage(self, driver):
        province_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'MAŁOPOLSKIE')))
        province_link.click()
        circuit_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Obwód25')))
        circuit_link.click()
        community_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Piwniczna')))
        community_link.click()

    def validateVotesNumber(self, driver):
        jkm_score = WebDriverWait(driver, 10). \
            until(EC.presence_of_element_located((By.NAME, 'Janusz KORWIN-MIKKE')))

        votes = jkm_score.get_attribute("value")
        assert int(votes) >= 0

    def resetVotes(self, driver):
        jkm_score = WebDriverWait(driver, 10). \
            until(EC.presence_of_element_located((By.NAME, 'Janusz KORWIN-MIKKE')))

        jkm_score.clear()
        jkm_score.send_keys('1488')
        submit_button = driver.find_element_by_class_name('submit_button')
        submit_button.click()

        jkm_score = WebDriverWait(driver, 10). \
            until(EC.presence_of_element_located((By.NAME, 'Janusz KORWIN-MIKKE')))
        votes = jkm_score.get_attribute("value")
        assert int(votes) == 1488

    def changeVotesNumber(self, driver):
        jkm_score = WebDriverWait(driver, 10). \
            until(EC.presence_of_element_located((By.NAME, 'Janusz KORWIN-MIKKE')))

        jkm_score.clear()
        jkm_score.send_keys('476')
        submit_button = driver.find_element_by_class_name('submit_button')
        submit_button.click()

        jkm_score = WebDriverWait(driver, 10). \
            until(EC.presence_of_element_located((By.NAME, 'Janusz KORWIN-MIKKE')))
        votes = jkm_score.get_attribute("value")
        assert int(votes) == 476
