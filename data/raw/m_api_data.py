import pandas as pd 
import requests
schemes = {
    "sbi_bluechip": 119551,
    "icici_bluechip": 120503,
    "nippon_largecap": 118632,
    "axis_bluechip": 119092,
    "kotak_bluechip": 120841
}
for v, n in schemes.items():
    url=f'https://api.mfapi.in/mf/{n}'
    r=requests.get(url)
    data=r.json()
    df = pd.DataFrame(data=data['data'])
    df.to_csv(f'{v}.csv', index=False)
    