"""Execute every Python block in WALKTHROUGH.zh-CN.md in one fresh namespace."""
from pathlib import Path
import re


def main():
    text=(Path(__file__).resolve().parent/'WALKTHROUGH.zh-CN.md').read_text(encoding='utf-8')
    blocks=re.findall(r'^```python\n(.*?)^```\s*$',text,re.MULTILINE|re.DOTALL)
    if not blocks:
        raise RuntimeError('no executable walkthrough blocks found')
    namespace={'__name__':'__walkthrough__'}
    for index,block in enumerate(blocks,1):
        print(f'=== block {index} ===')
        exec(compile(block,f'WALKTHROUGH.zh-CN.md:block-{index}','exec'),namespace)
    print(f'PASS: {len(blocks)} Python blocks executed')


if __name__=='__main__': main()
