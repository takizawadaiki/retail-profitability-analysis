"""Recompute aggregate diagnostics; this does not validate transaction-level data."""
import json
from pathlib import Path

def analyze(data):
    regions=['West','East','South','Central']
    names=[r['name'] for r in data['All']['subcat']]
    cells={r:{x['name']:x for x in data[r]['subcat']} for r in regions}
    assert all(set(cells[r])==set(names) for r in regions)
    totals={r:sum(x['sales'] for x in cells[r].values()) for r in regions}
    global_sales={n:sum(cells[r][n]['sales'] for r in regions) for n in names}
    weights={n:v/sum(global_sales.values()) for n,v in global_sales.items()}
    mix=[]
    for r in regions:
        observed=sum(x['profit'] for x in cells[r].values())/totals[r]
        standardized=sum(weights[n]*cells[r][n]['profit']/cells[r][n]['sales'] for n in names)
        mix.append(dict(region=r,observed=observed,standardized=standardized))
    # Reference-weight decomposition of Central minus all other regions.
    c=cells['Central']; other={n:{k:sum(cells[r][n][k] for r in regions if r!='Central') for k in ['sales','profit']} for n in names}
    cs=sum(x['sales'] for x in c.values()); os=sum(x['sales'] for x in other.values())
    contributions=[]
    for n in names:
        wc=c[n]['sales']/cs; wo=other[n]['sales']/os
        mc=c[n]['profit']/c[n]['sales']; mo=other[n]['profit']/other[n]['sales']
        contributions.append(dict(name=n,central_margin=mc,other_margin=mo,mix_effect=(wc-wo)*mo,within_effect=wc*(mc-mo),benchmark_gap_dollars=c[n]['sales']*(mo-mc)))
    gap=sum(x['profit'] for x in c.values())/cs-sum(x['profit'] for x in other.values())/os
    assert abs(gap-sum(x['mix_effect']+x['within_effect'] for x in contributions))<1e-12
    negative=[dict(region=r,**x) for r in regions for x in cells[r].values() if x['profit']<0]
    negative.sort(key=lambda x:x['profit'])
    all_negative=sum(-x['profit'] for x in data['All']['subcat'] if x['profit']<0)
    region_negative=sum(-x['profit'] for x in negative)
    discounted=data['All']['discount']; loss=sum(-x['profit'] for x in discounted if x['profit']<0)
    positive=sum(x['profit'] for x in discounted if x['profit']>0)
    reconciliation={r:{view:{k:sum(x[k] for x in data[r][view])-data[r]['kpis']['total_'+k] for k in ['sales','profit']} for view in ['subcat','category','segment']} for r in data}
    return dict(standardized_regions=mix,decomposition=dict(gap=gap,mix=sum(x['mix_effect'] for x in contributions),within=sum(x['within_effect'] for x in contributions),contributions=sorted(contributions,key=lambda x:x['within_effect'])),loss_cells=negative,loss_pool=dict(regional=region_negative,national=all_negative,masked=region_negative-all_negative),discount=dict(loss=loss,positive=positive,erosion=loss/positive,loss_record_share=sum(x['orders'] for x in discounted if x['profit']<0)/data['All']['kpis']['total_orders']),reconciliation=reconciliation)

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    result=analyze(json.loads((root/'aggregate-data.json').read_text()))
    (root/'analysis-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['reconciliation','loss_cells']},indent=2))
