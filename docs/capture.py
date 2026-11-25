"""Render actual dashboard HTML with synthetic API fixtures; browser network access is restricted."""
import sys, json, os
from pathlib import Path
from playwright.sync_api import sync_playwright
base=Path(__file__).resolve().parents[1];sys.path.insert(0,str(base/'shared'))
from app import MODULES
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for i,(key,cfg) in enumerate(MODULES.items(),1):
  context=browser.new_context(viewport={'width':1440,'height':950},device_scale_factor=1)
  page=context.new_page()
  records=[{'id':j+1,**dict(zip(cfg['fields'],sample))} for j,sample in enumerate(cfg['sample'])]
  if key=='risk':
   for r in records:r['risk_score']=round(sum(int(r[x]) for x in cfg['fields'][2:])/4*20);r['risk_band']='High' if r['risk_score']>=70 else 'Medium'
  summary={'labels':cfg['metrics'],'values':[len(records),1,1]}
  page.route('**/api/summary',lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps(summary)))
  page.route('**/api/records',lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps(records)))
  html=(base/'shared/dashboard.html').read_text()
  for k,v in [('__TITLE__',cfg['name']),('__SHORT__',cfg['short']),('__DESC__',cfg['desc']),('__COLOR__',cfg['color']),('__MODULE__',key),('__FIELDS__',json.dumps(cfg['fields'])),('__LABELS__',json.dumps(cfg['metrics']))]:html=html.replace(k,v)
  page.goto('about:blank');page.set_content(html,wait_until='load')
  # Provide a local-page fetch shim because the browser disallows even loopback network requests.
  page.evaluate('''(fixtures) => { window.fetch = async (url) => ({ok:true, json:async()=>url.includes('summary')?fixtures.summary:fixtures.records}); }''',{'summary':summary,'records':records})
  page.evaluate('load()');page.wait_for_timeout(300)
  page.screenshot(path=str(base/'screenshots'/f'{i:02}-{key}-dashboard.png'),full_page=True)
  print(key,'preview captured')
  context.close()
 browser.close()
