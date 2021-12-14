#!/usr/bin/env python3
import os
import pickle
import sys
from glob import glob
from os import path
from time import sleep
from typing import List, Dict

import pandas as pd
import regex as re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

os.chdir(sys.path[0])


class Scraper:

    def __init__(self, filename):
        self.difficulties_storage = path.join("cache", path.basename(filename).replace(".txt", ".pkl"))
        self.difficulties = self._load_existing_difficulties()
        self.driver = self._init_chromedriver()

    @staticmethod
    def _init_chromedriver(debug: bool = False) -> webdriver:
        options = webdriver.ChromeOptions()
        if not debug:
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-setuid-sandbox")
        return webdriver.Chrome(options=options)

    def _extract_difficulty(self) -> str:
        for difficulty in ["easy", "medium", "hard"]:
            try:
                return self.driver.find_element_by_xpath(f"//div[@diff='{difficulty}']").get_attribute("diff")
            except NoSuchElementException:
                pass
        raise NoSuchElementException("couldn't find it")

    def _load_existing_difficulties(self) -> Dict:
        if path.exists(self.difficulties_storage):
            with open(self.difficulties_storage, "rb") as infile:
                return pickle.load(infile)
        else:
            return dict()

    def scrape(self, links: List[str]) -> pd.DataFrame:
        for link in links:
            if link not in self.difficulties:
                self.difficulties[link] = self._scrape_difficulty(link)
            print(f"{link} {self.difficulties[link]}")
        self.store_difficulties()
        return pd.DataFrame({"link": k, "difficulty": v} for k, v in self.difficulties.items()).set_index("link")

    def store_difficulties(self):
        with open(self.difficulties_storage, "wb") as infile:
            pickle.dump(self.difficulties, infile)

    def _scrape_difficulty(self, link: str) -> str:
        self.driver.get(link)
        submit_button_clickable = EC.element_to_be_clickable((By.XPATH, "//button[@data-cy='submit-code-btn']"))
        try:
            WebDriverWait(self.driver, timeout=5).until(submit_button_clickable)
            difficulty = self._extract_difficulty()
            sleep(2.5)
        except TimeoutException:
            difficulty = "premium"
        finally:
            self.store_difficulties()
        return difficulty


def parse_problems(file: str) -> pd.DataFrame:
    def get_freq(string):
        return int(re.sub(r"^.+ \(", "", string))

    def get_title(string):
        return re.sub(r" \([0-9]+$", "", string)

    with open(file) as infile:
        problems_str = infile.readlines()
    problems = [line.strip().split(" times): ") for line in problems_str]
    dicts = [{"title": get_title(s), "times": get_freq(s), "link": link} for s, link in problems]
    base_df = pd.DataFrame(dicts).set_index("link", drop=False)
    return base_df


def prepare_output_file(filename):
    print(filename)
    base_df = parse_problems(filename)
    difficulties_df = Scraper(filename).scrape(base_df.link.to_list())
    df = base_df.join(difficulties_df)
    df.to_csv(path.join("outputs", path.basename(filename).replace(".txt", ".csv")), index=False)
    print()


for file in glob("inputs/*.txt"):
    prepare_output_file(file)
