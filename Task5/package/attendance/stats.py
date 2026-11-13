import datetime
def percentage(present, total):
    return 100 * present / total if total else 0.0

def compute(grouped):
    summary=[]; streaks=[]
    for register,rows in sorted(grouped.items()):
        present=sum(status=="P" for _,status in rows)
        summary.append((register,present,len(rows)-present,percentage(present,len(rows))))
        run=0; previous=None
        for date_text,status in sorted(rows):
            current=datetime.date.fromisoformat(date_text)
            consecutive=previous is not None and (current-previous).days==1
            run=(run+1 if consecutive else 1) if status=="A" else 0
            if run>=3: streaks.append(register); break
            previous=current
    return summary,streaks
