"""Run real tests in three modes and save deterministic teaching evidence."""
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys
import third_figure as m

ROOT=Path(__file__).resolve().parent
LOG=ROOT/'logs'
LOG.mkdir(exist_ok=True)

def save_json(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    results=[]
    for name, flags in [('normal',[]),('optimized',['-O']),('double-optimized',['-OO'])]:
        cmd=[sys.executable,*flags,'-m','unittest','-v','test_third_figure']
        p=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        # Invocation uses a local executable; public evidence records a portable command only.
        text='COMMAND: python '+ ' '.join(flags+['-m','unittest','-v','test_third_figure'])+'\n'+p.stdout
        (LOG/f'tests-{name}.log').write_text(text,encoding='utf-8')
        if p.returncode: raise SystemExit(p.returncode)
        r=subprocess.run([sys.executable,*flags,'third_figure.py'],cwd=ROOT,text=True,capture_output=True,check=True)
        parsed=json.loads(r.stdout)
        if parsed!=json.loads(json.dumps(m.report())): raise RuntimeError('report differs across interpreter modes')
        (LOG/f'report-{name}.json').write_text(r.stdout,encoding='utf-8')
        results.append({'mode':name,'exit_code':p.returncode,'test_methods':30,'report_sha256':hashlib.sha256(r.stdout.encode()).hexdigest()})
    report=m.report(); save_json(ROOT/'report.json',report)
    routes={}
    for name,(q,r,c) in m.MOODS.items():
        cases=[s for s in m.supports('middle-nonempty') if m.premises(q,r,s)]
        for s in cases: m.proof_witness(name,s)
        routes[name]={'premises':[q,r],'conclusion':c,'witness_routes_checked':len(cases)}
    invalid_pairs=[row for row in report['policies']['all-nonempty']['premise_pairs'] if not row['valid_conclusions']]
    proof_summary={'route_checks':routes,'total_witness_routes':sum(x['witness_routes_checked'] for x in routes.values()),
                   'inference_queries':3*16*4,'nonentailments':sum(len(row['minimal_countermodels']) for p in report['policies'].values() for row in p['premise_pairs']),
                   'invalid_premise_pairs_all_nonempty':len(invalid_pairs),
                   'invalid_pairs':invalid_pairs}
    save_json(ROOT/'witnesses.json',proof_summary)
    save_json(LOG/'environment.json',{'python_version':platform.python_version(),'implementation':platform.python_implementation(),
        'system':platform.system(),'machine':platform.machine(),'dependencies':'Python standard library only',
        'excludes':'No user names, private paths, environment variables or host identifiers recorded.'})
    save_json(LOG/'verification.json',{'runs':results,'report_identical_across_modes':True,**{k:v for k,v in proof_summary.items() if k!='invalid_pairs'}})
    rows=['# 第三格完整分类（程序生成）','',
          '主前提 Q(M,P)，次前提 R(M,S)，结论 C(S,P)。所有策略均要求论域非空。',
          '反模型的最小性按对象数衡量，每个实际类型使用一个对象；等基数时取类型元组字典序首项。',
          '', '| 主/次 | 允许空项 | M 非空 | 所有项非空 |','|---|---|---|---|']
    for i,row in enumerate(report['policies']['allow-empty']['premise_pairs']):
        cells=['、'.join(report['policies'][p]['premise_pairs'][i]['valid_conclusions']) or '无' for p in m.POLICIES]
        rows.append('| '+row['major']+row['minor']+' | '+' | '.join(cells)+' |')
    rows+=['','## 十组无有效结论的前提对（全项非空）','',
           '每行四个反模型分别否定 A、E、I、O；它们不必是同一个模型。','',
           '| 前提对 | 否 A | 否 E | 否 I | 否 O |','|---|---|---|---|---|']
    for row in invalid_pairs:
        cells=[str(row['minimal_countermodels'][c]) for c in m.QUANTIFIERS]
        rows.append('| '+row['major']+row['minor']+' | '+' | '.join(cells)+' |')
    rows+=['','## 六条见证路线','', '| 名称 | 满足前提且 M 非空的支持数 |','|---|---|']
    rows += ['| '+k+' | '+str(v['witness_routes_checked'])+' |' for k,v in routes.items()]
    rows+=['','有限检查仅核验这段代码；一般的类型压缩与见证保持证明见 README 和正文。','']
    (ROOT/'REPORT.md').write_text('\n'.join(rows),encoding='utf-8')
    print(json.dumps({'runs':3,'tests_per_run':30,'inference_queries':192,'nonentailments':proof_summary['nonentailments'],'witness_routes':proof_summary['total_witness_routes']},ensure_ascii=False))

if __name__=='__main__': main()
