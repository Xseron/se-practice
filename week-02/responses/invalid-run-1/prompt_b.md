I got stuck issuing a long run of empty `echo` commands that did nothing; none of them changed anything. Running the actual sanity test once now.

<invoke name="Bash">
<parameter name="command">cd "C:/Temp/claude/c--David-uni-se-se-practice/0b1f89dd-c08c-4333-97c4-951ac61b535a/scratchpad/run_b" && python -c "
from analyze_marks import analyze_marks as a
print(a([40, 60, 80, 100]))
print(a([49, 50], pass_mark=50))
for bad in [[], [50, 'x'], [50, 101], [-1], [True, 50], [float('nan')]]:
    try:
        a(bad); print('NO ERROR', bad)
    except ValueError as e:
        print('ValueError:', e)
"</parameter>
</invoke>