python
import os, sqlite3, random
from typing import List, Tuple, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), 'mcgg_pairing.db')

def connect_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.execute('''CREATE TABLE IF NOT EXISTS players (name TEXT PRIMARY KEY, hp INTEGER DEFAULT 30, alive INTEGER DEFAULT 1)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS matches (round INTEGER, p1 TEXT, p2 TEXT)''')
    conn.commit()
    return conn

def all_alive_players(conn):
    return conn.execute('SELECT name,hp FROM players WHERE alive=1').fetchall()

def recent_opponent(conn, player_name: str):
    row = conn.execute('SELECT round,p1,p2 FROM matches WHERE p1=? OR p2=? ORDER BY round DESC LIMIT 1', (player_name, player_name)).fetchone()
    if not row:
        return None
    _, p1, p2 = row
    return p2 if p1 == player_name else p1

def generate_one_pairing(players: List[Tuple[str,int]], avoid_recent: Dict[str,str]) -> Dict[str,str]:
    names = list(players)
    names.sort(key=lambda x: x[1], reverse=True)
    paired, used = {}, set()

    def find_partner(idx):
        name, hp = names[idx]
        best, best_score = None, None
        for cand, chp in names:
            if cand == name or cand in used: continue
            pen = 1000.0 if avoid_recent.get(name) == cand else 0.0
            score = abs(hp - chp) + random.random()*0.0001 + pen
            if best is None or score < best_score:
                best, best_score = cand, score
        return best

    for i in range(len(names)):
        name, hp = names[i]
        if name in used: continue
        partner = find_partner(i)
        if not partner:
            for cand,_ in names:
                if cand != name and cand not in used:
                    partner = cand; break
        if not partner:
            paired[name] = 'CLONE'; used.add(name); continue
        paired[name], paired[partner] = partner, name
        used.add(name); used.add(partner)
    return paired

def montecarlo_predict(target: str, sims: int = 300):
    conn = connect_db()
    players = all_alive_players(conn)
    if not any(p[0] == target for p in players): return []
    avoid = {n: recent_opponent(conn, n) for n,_ in players if recent_opponent(conn, n)}
    counts = {}
    for _ in range(max(1, sims)):
        opp = generate_one_pairing(players, avoid).get(target, 'CLONE')
        counts[opp] = counts.get(opp, 0) + 1
    total = sum(counts.values())
    return sorted([(n, c/total) for n,c in counts.items()], key=lambda x: x[1], reverse=True)
