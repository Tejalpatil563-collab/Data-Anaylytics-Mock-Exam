import pandas as pd 
df=pd.DataFrame(
    {
        "stu_id":[101,102,103,104,105],
        "name":["tejal","yugal","yamini","trupti","rutuja"],
        "age":[24,35,36,26,25],
        "marks":[40,70,80,90,99]
    })

print("original data:\n",df)
print("\nsubset(marks)>30):\n",df[df["marks"]>30])

print("\nsorted by marks(ascending):\n",
df.sort_values("marks"))

print("\nsorted by marks (desecnding):\n",
df.sort_values("marks",ascending=False))

print("\ngrouped (average mark by name):\n",
df.groupby("name")["marks"].mean())

print("\nmean=",df["marks"].mean())
print("\nmedian=",df["marks"].median())
print("\nmode=")
print(df["marks"].mode())