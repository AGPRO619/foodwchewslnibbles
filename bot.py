import os, json, sys, re, urllib.request, urllib.error
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

BASE=Path(__file__).parent
MENU=json.loads((BASE/'menu.json').read_text())
RATINGS=json.loads((BASE/'ratings.json').read_text())
TOKEN=os.environ['DISCORD_BOT_TOKEN']
CHANNEL=os.environ['DISCORD_CHANNEL_ID']

def rating(food):
    f=food.lower()
    # Match the most specific recognizable entrée; prevent generic "chicken" matches.
    aliases={
      'hamburger / cheeseburger':['hamburger','cheeseburger'],
      'carne guisada with tortillas':['carne guisada'],
      'turkey & cheese sandwich':['turkey & cheese','turkey and cheese'],
      'club sandwich':['club sandwich'],
      'loaded baked potato with chicken fajitas':['loaded baked potato'],
      'corn dog with sun chips':['corn dog'],
      'hot dog with baked chips':['hot dog'],
      'chicken alfredo pasta':['chicken alfredo'],
      'ham & cheese deli sandwich':['ham & cheese'],
      'chef salad with breadsticks':['chef salad'],
      'shaker salad with breadsticks':['shaker salad'],
      'bean & cheese burrito':['bean & cheese burrito'],
      'sunbutter & jelly sandwich':['sunbutter'],
      'turkey & gravy':['turkey & gravy'],
      'artisan chicken tenders':['artisan chicken tenders'],
      'spicy chicken tenders':['spicy chicken tenders'],
      'hot & spicy boneless wings':['boneless wings'],
      'chicken poppers':['chicken poppers'],
      'chicken smackers':['chicken smackers'],
      'pizza & wings':['pizza & wings'],
      'pizza crunchers':['pizza crunchers'],
      'stuffed crust pizza':['stuffed crust pizza'],
      'pizzaboli bites':['pizzaboli'],
      'cheesy pull-aparts':['cheesy pull-aparts'],
      'chicken & cheese crisp-ups':['chicken & cheese crisp-ups'],
      'artisan chicken sandwich':['artisan chicken sandwich'],
      'walking taco':['walking taco'],
      'frito pie':['frito pie'],
      'pulled pork sandwich':['pulled pork sandwich'],
      'cheeseburger sliders':['cheeseburger sliders'],
    }
    matches=[]
    for name,terms in aliases.items():
        if any(term in f for term in terms):
            matches.append((max(len(t) for t in terms if t in f), RATINGS.get(name, RATINGS.get(name.title(), 'unrated'))))
    if not matches:
        for name,value in RATINGS.items():
            if name.lower() in f: matches.append((len(name),value))
    return max(matches)[1] if matches else 'unrated'

def verdict(mains):
    votes=[rating(x) for x in mains]
    if 'good' in votes: return '🔥 GOOD EATS'
    if 'mid' in votes: return '😐 MID EATS'
    if votes and all(x=='bad' for x in votes): return '💀 BAD EATS'
    return '❓ NOT RATED'


def request(method, path, payload=None):
    import os
    import json
    import urllib.request

    token = os.environ["DISCORD_BOT_TOKEN"]

    url = "https://discord.com/api/v10" + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": "PSJA-Good-Eats/1.0"
        },
        method=method.upper()
    )

    with urllib.request.urlopen(req, timeout=25) as response:
        return json.load(response)


def main():
    now=datetime.now(ZoneInfo('America/Chicago'))
    date=os.getenv('LUNCH_DATE') or now.date().isoformat()
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',date): raise ValueError('Date must be YYYY-MM-DD')
    action=os.getenv('ACTION','post')
    if action=='post' and datetime.fromisoformat(date).weekday()>=5:
        print('Weekend; skipped'); return
    parts=[]; mentions=[]
    for campus,title in [('bears','🐻 BEARS'),('tstem','🔬 T-STEM')]:
        entry=MENU.get(campus,{}).get(date)
        ids=[v.strip() for v in os.getenv('PING_'+campus.upper(),'').split(',') if v.strip().isdigit()]
        mentions+=ids
        if not entry:
            parts.append('**'+title+'**\nMenu not available / not confirmed.')
            continue
        override=os.getenv('OVERRIDE_'+campus.upper(),'').strip().lower()
        result={'good':'🔥 GOOD EATS','bad':'💀 BAD EATS','mid':'😐 MID EATS','unrated':'❓ NOT RATED'}.get(override,verdict(entry['mains']))
        lines=['**'+title+'**','**Lunch choices:**']+['• '+x for x in entry['mains']]
        if entry.get('sides'):lines+=['**Sides:** '+', '.join(entry['sides'])]
        if entry.get('fruit'):lines+=['**Fruit:** '+', '.join(entry['fruit'])]
        lines+=['**Verdict: '+result+'**']
        parts.append('\n'.join(lines))
    content='🍔 **PSJA GOOD EATS — '+date+'**\n\n'+'\n\n'.join(parts)
    if mentions:content+='\n\n'+' '.join('<@'+x+'>' for x in dict.fromkeys(mentions))
    payload={'content':content[:2000],'allowed_mentions':{'parse':[],'users':list(dict.fromkeys(mentions))}}
    if action=='preview':print(payload['content']);return
    message_id=os.getenv('EDIT_MESSAGE_ID','').strip()
    if message_id:
        request('PATCH',f'/channels/{CHANNEL}/messages/{message_id}',payload)
        print('Edited existing message',message_id)
    else:
        response=request('POST',f'/channels/{CHANNEL}/messages',payload)
        print('Posted message ID:',response['id'])

if __name__=='__main__': main()
