
<invoke name="Read">
<parameter name="file_path">C:\Temp\claude\c--David-uni-se-se-practice\0b1f89dd-c08c-4333-97c4-951ac61b535a\scratchpad\run_a\bad_out.txt</parameter>
</invoke>
     1→Error: Row 4: non-numeric mark 'abc' for Maths


<invoke name="Read">
<parameter name="file_path">C:\Temp\claude\c--David-uni-se-se-practice\0b1f89dd-c08c-4333-97c4-951ac61b535a\scratchpad\run_a\marks_out.txt</parameter>
</invoke>
     1→(truncated,


<invoke name="Bash">
<parameter name="command">cd "C:/Temp/claude/c--David-uni-se-se-practice/0b1f89dd-c08c-4333-97c4-951ac61b535a/scratchpad/run_a" && python -c "
import student_marks as sm
s=sm.sample_students()
r=sorted(s,key=lambda x:x.average,reverse=True)
assert [x.name for x in r]==['Charlie','Alice','Ethan','Bob','Diana','Fatima'], [x.name for x in r]
assert r[0].grade=='A+' and r[-1].grade=='F'
assert sum(x.passed for x in s)==2
st=sm.subject_stats(s)
assert abs(st['Maths']['mean']-64.8333)<1e-3
assert st['Chemistry']['pass_rate']==50.0
m=sm.load_students('marks.csv')
assert [x.name for x in m]==['Zara','Omar'] and m[1].failed_subjects==['Maths']
print('ALL OK')
"</parameter>
<parameter name="description">Assert-based checks of the analysis functions</parameter>
</invoke>
ALL OK

Done. The script is at `C:\Temp\claude\...\scratchpad\run_a\student_marks.py` and uses only the standard library.

**What it does**
- Loads marks from a CSV with a `name` column followed by one column per subject, or falls back to built-in sample data if no file is given.
- Validates input: rejects non-numeric marks and values outside 0 to 100, with the row number in the error.
- Per student: total, average, letter grade (A+ to F), list of failed subjects, and pass/fail status. Students are ranked by average.
- Per subject: count, mean, median, min, max, standard deviation, and pass rate.
- Class summary: class average, top and bottom student, overall pass rate, a grade distribution bar chart, and a list of who failed which subjects.

**Usage**

```
python student_marks.py              # sample data
python student_marks.py marks.csv    # your own file
```

**Verification**
The tool's output display was garbled in this session, so I checked the results with assertions instead of reading the printed report. Ranking, grades, pass counts, subject means and pass rates, CSV loading, and the bad-input error path all passed. The pass mark and grade bands are constants at the top of the file if you want to change them.