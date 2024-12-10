
from duckduckgo_search import DDGS

ans = DDGS().text(keywords='AI科技', max_results=30)
for ans_id, tmp_ans in enumerate(ans):
    print(f'{ans_id} tmp_ans:{tmp_ans}')
print(f'ans:{ans}')