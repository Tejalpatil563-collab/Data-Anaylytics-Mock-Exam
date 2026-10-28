import pandas as pd
def calculate_average(marks):
    return sum(marks)/ len(marks)

n=int(input("enter number of students:"))
names=[]
marks=[]
for i in range(n):
    name=input("enter student name:")
    mark=float(input("enter marks:"))

    names.append(name)
    marks.append(mark)
df=pd.DataFrame({
    "name":names,
    "marks":marks
})

def result(marks):
    if mark>=75:
        return "distinction"
    elif mark>=50:
        return "pass"
    else:
        return "fail"
df["result"]=df["marks"].apply(result)

print("\nDataset:")
print(df)

print("\nstudent analysis:")
for mark in marks:
    if mark>=75:
        print(mark,"distiction")
    elif mark>=50:
        print(mark,"pass")
    else:
        print(mark,"fail")

print("\naverage marks:",calculate_average(marks))
print("\nhighest marks:",max(marks))
print("\nlowest marks:",min(marks))

