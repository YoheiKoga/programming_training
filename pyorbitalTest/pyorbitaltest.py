from pyorbital.orbital import Orbital
from datetime import datetime

# 国際宇宙ステーション
orb = Orbital("ISS (ZARYA)") 

# 福岡市役所
(lat, lon, alt) =  (33.590198, 130.401719, 4.0) 

# 現在時刻(UTC): 2019-07-07 11:24:46
now = datetime.utcnow() 

# 福岡市役所からみて24時間以内の観測可能な時間
passTimes = orb.get_next_passes(now, 24, lon, lat, alt, tol=0.001, horizon=0)

print("福岡市役所の次のPassの時間は(UTC): ", passTimes[0][0].strftime('%Y-%m-%d %H:%M:%S'))
#=> 福岡市役所の次のPassの時間は(UTC):  2019-07-07 14:16:35



