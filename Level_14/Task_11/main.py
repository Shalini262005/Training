from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

app = FastAPI()

class Match(BaseModel):
    match_no: int
    match_name: str
    match_type: str
    match_date: str
    match_time: str
    match_venue: str
    match_href: str
    match_team1: str
    match_team2: str
    winning_team: str

base_url = "https://www.cricbuzz.com"
series_url = "https://www.cricbuzz.com/cricket-series/3472/indian-premier-league-2021/matches"

def scrape_match_data():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    driver.get(series_url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    match_data = []
    matches = soup.select("div.cb-col-100.cb-col.cb-series-matches")
    year = "2021"

    for idx, match in enumerate(matches, start=1):
        try:
            date = match.select_one('span.ng-binding').text.strip()
            match_date = date.split(",")[0].strip()

            match_item = match.select_one("a.text-hvr-underline")
            if not match_item:
                continue
            match_detail = match_item.select_one("span").text.strip().split(',')
            match_name = match_detail[0]
            match_href = base_url + match_item['href']

            playoffs = ["Qualifier 1", "Qualifier 2", "Eliminator", "Final"]
            match_type = "Playoff" if match_detail[1].strip() in playoffs else "League"

            match_time = match.select_one('span.schedule-date').text.strip()
            match_venue = match.select_one("div.text-gray").text.strip()

            match_teams = match_name.split(" vs ")
            match_team1 = match_teams[0].strip()
            match_team2 = match_teams[1].strip()

            result_tag = match.select_one("a.cb-text-complete")
            winning_team = result_tag.text.strip().split(" won")[0].strip() if result_tag else "TBD"

            match_data.append({
                "match_no": idx,
                "match_name": match_name,
                "match_type": match_type,
                "match_date": match_date + ", " + year,
                "match_time": match_time,
                "match_venue": match_venue,
                "match_href": match_href,
                "match_team1": match_team1,
                "match_team2": match_team2,
                "winning_team": winning_team.upper()
            })
        except Exception:
            continue

    return pd.DataFrame(match_data).set_index("match_no")

@app.get("/get_live/Match_details/{match_no}", response_model=Match)
def get_match_details(match_no: int):
    df = scrape_match_data()
    if match_no in df.index:
        row = df.loc[match_no]
        return Match(match_no=match_no, **row.to_dict())
    else:
        raise HTTPException(status_code=404, detail=f"Match {match_no} not found")
