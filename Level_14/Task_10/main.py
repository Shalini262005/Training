from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

class match(BaseModel):
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
    

Match_details = pd.read_csv("C:/Users/shali/OneDrive/Desktop/Training/Level_14/Task_2/IPL 2021 Matches.csv",index_col='match_no')

@app.get("/Match_details/{match_no}",response_model=match)
def get_match(match_no: int):
    if match_no in Match_details.index:
        row = Match_details.loc[match_no]
        return match(match_no=match_no, **row.to_dict())
    else:
        raise HTTPException(status_code=404, detail=f'Match {match_no} not found')
    