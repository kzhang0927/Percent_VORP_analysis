from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from time import sleep

#create empty dataframe to use as "master dataframe" as we add df2 from loops
df = pd.DataFrame()



list_teams = ['CLE','GSW']
beg_year = 2017
end_year = 2018

#Get table data for teams and years
for year in range(beg_year, end_year + 1):
    for teams in list_teams:
        try:
            r = get(f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fteams%2F{teams}%2F{year}.html&div=div_playoffs_advanced")
            if r.status_code==200:
                soup = BeautifulSoup(r.content, 'html.parser')
                table = soup.find('table')
            #translate scraped table into dataframe
            df2= pd.read_html(str(table))[0]
            #add flag and calculation columns
            df2 = df2.assign(Year = year,Team = teams, Percent_VORP = df2["VORP"] / df2["VORP"].sum())
            #obey robots.txt
            sleep(3)
            #append df and df2
            df = pd.concat([df,df2], axis=0, join='outer', ignore_index=False, keys=None,levels=None, names=None, verify_integrity=False, copy=True)
        except:
            pass
df = df.sort_values(by=["Percent_VORP"], ascending = False).query("G>9")
df.to_csv("Percent_VORP_Sorted.csv", index=False)


print(df)




