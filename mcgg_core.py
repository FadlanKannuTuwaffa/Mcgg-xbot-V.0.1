import os, sqlite3, random
from typing import List, Tuple, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), 'mcgg_pairing.db')

def connect_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.execute('CREATE TABLE IF NOT EXISTS players (name TEXT PRIMARY KEY, hp INTEGER DEFAULT 30, alive INTEGER DEFAULT 1)')
    conn.execute('CREATE TABLE IF NOT EXISTS matches (round INTEGER, p1 TEXT, p2 TEXT)')
    conn.commit()
    return conn

def add_or_update_player(name: str, hp: int = 30, alive: int = 1):
    conn = connect_db()
    conn.execute('INSERT OR REPLACE INTO players (name,hp,alive) VALUES (?,?,?)', (name, hp, alive))
    conn.commit()
    conn.close()

def all_alive_players(conn):
    return conn.execute('SELECT name,hp FROM players WHERE alive=1').fetchall()

def recent_opponent(conn, player_name: str):
    row = conn.execute('SELECT round,p1,p2 FROM matches WHERE p1=? OR p2=? ORDER BY round DESC LIMIT 1', (player_name, player_name)).fetchone()
    if not row:
        return None
    _, p1, p2 = row
    return p2 if p1 == player_name else p1

def log_actual_match(round_no: int, player: str, opponent: str):
    conn = connect_db()
    conn.execute('INSERT INTO matches (round,p1,p2) VALUES (?,?,?)', (round_no, player, opponent))
    conn.commit()
    conn.close()

def history_counts_for(target: str, window_round: int = None) -> Dict[str,int]:
    conn = connect_db()
    if window_round is None:
        rows = conn.execute('SELECT p1,p2 FROM matches WHERE p1=? OR p2=?', (target, target)).fetchall()
    else:
        rows = conn.execute('SELECT p1,p2 FROM matches WHERE (p1=? OR p2=?) AND round >= ?', (target, target, window_round)).fetchall()
    conn.close()
    counts = {}
    for p1,p2 in rows:
        opp = p2 if p1 == target else p1
        counts[opp] = counts.get(opp,0) + 1
    return counts

def generate_one_pairing(players: List[Tuple[str,int]], avoid_recent: Dict[str,str]) -> Dict[str,str]:
    names = list(players)
    names.sort(key=lambda x: x[1], reverse=True)
    # slight shuffle for stochasticity
    if random.random() < 0.15:
        i = random.randrange(len(names))
        j = random.randrange(len(names))
        names[i], names[j] = names[j], names[i]

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

def montecarlo_predict(target: str, sims: int = 300, history_weight: float = 2.0, history_window_round: int = None) -> List[Tuple[str,float]]:
    """Predict opponent distribution for target player.
    Combines Monte Carlo pairing simulation with historical counts (adaptive learning).
    - history_weight: how strongly history counts bias final probabilities
    - history_window_round: if provided, only use matches with round >= that value
    """
    conn = connect_db()
    players = all_alive_players(conn)
    if not any(p[0] == target for p in players):
        return []
    # build avoid_recent map
    avoid = {}
    for n,_ in players:
        opp = recent_opponent(conn, n)
        if opp:
            avoid[n] = opp
    counts = {}
    for _ in range(max(1, sims)):
        pairing = generate_one_pairing(players, avoid)
        opp = pairing.get(target, 'CLONE')
        counts[opp] = counts.get(opp, 0) + 1
    # incorporate history
    hist = history_counts_for(target, window_round=history_window_round)
    # Boost counts by history (weighted)
    for opp, cnt in hist.items():
        counts[opp] = counts.get(opp, 0) + cnt * history_weight
    total = sum(counts.values())
    if total == 0:
        return []
    scored = sorted([(name, cnt/total) for name,cnt in counts.items()], key=lambda x: x[1], reverse=True)
    return scored
