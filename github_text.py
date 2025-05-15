import os
import subprocess
from datetime import datetime, timedelta

TEXT = "TEXT"
START_DATE = "2025-07-06"  # niedziela; przesunięte, by całe TEXT mieściło się w oknie ostatniego roku
COMMITS_PER_CELL = 3

FONT = {
    "T": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
    ],
    "E": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "11111",
    ],
    "X": [
        "10001",
        "01010",
        "00100",
        "00100",
        "01010",
        "10001",
        "10001",
    ],
}

def run(cmd, env=None):
    subprocess.run(cmd, shell=True, check=True, env=env)

def commit_on(date, index):
    with open("contribution-text.txt", "a") as f:
        f.write(f"{date.isoformat()} #{index}\n")

    run("git add contribution-text.txt")

    env = os.environ.copy()
    git_date = date.strftime("%Y-%m-%dT12:00:00")
    env["GIT_AUTHOR_DATE"] = git_date
    env["GIT_COMMITTER_DATE"] = git_date

    run(f'git commit -m "draw TEXT {git_date}"', env=env)

def build_columns(text):
    columns = []
    for char in text:
        glyph = FONT[char]
        for col in range(len(glyph[0])):
            column = [glyph[row][col] for row in range(7)]
            columns.append(column)
        columns.append(["0"] * 7)
    return columns

def main():
    start = datetime.strptime(START_DATE, "%Y-%m-%d")
    columns = build_columns(TEXT)

    for col_index, column in enumerate(columns):
        for row_index, value in enumerate(column):
            if value == "1":
                date = start + timedelta(days=col_index * 7 + row_index)
                for i in range(COMMITS_PER_CELL):
                    commit_on(date, i)

    print("Gotowe ✅ Teraz zrób: git push")

if __name__ == "__main__":
    main()
