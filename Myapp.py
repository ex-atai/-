import random
import math
import re
import os
ans=[]  ##记录已经保存的表达式
ecode=[]    ##记录已保存的表达式的编码
k1=['+','-','*','/']
k2=['(',')']

def encoded(formula):   ##对表达式进行编码
    f=[]
    for i in range(0,len(formula)):     #将formula中的数字放入f中
        if (not (formula[i] in k1 or formula[i] in k2)):
            f.append(formula[i])
    for i in range(0,len(f)):     #对f中的数字降序排序
        for j in range(0,i):
            fz1,fm1=change(f[i])
            fz2,fm2=change(f[j])
            if (fz1*fm2>fz2*fm1):
                f[i],f[j]=f[j],f[i]
    for i in range(0,len(k1)):
        for j in range(0,len(formula)):
            if (formula[j]==k1[i]): f.append(k1[i]) #按+-*/的顺序放入f中
    f.append(cal(formula))  #将运算结果加入f中
    return f

def checkrepeat(formula):   #判断表达式是否重复
    f=encoded(formula)
    if (f in ecode):        #如果当前表达式的编码在之前出现过则返回False
        return False
    else:
        ecode.append(f)
        return True

def change(x):  ##将真分数字符串转化为假分数并返回分子和分母
    x=re.split('’|/',x)     ##将x按’和/分开
    m=len(x)
    if (len(x)==1):     ##x是一个整数
        return int(x[0]),1
    elif (len(x)==3):     ##x是一个真分数
        a,b,c=int(x[0]),int(x[1]),int(x[2])
        return a*c+b,c
    else:       ##x是一个假分数
        return int(x[0]),int(x[1])

def unchange(fz,fm):        ##将分子和分母转化为整数或分数字符串
    if (fz%fm==0): return str(fz//fm)
    if (fz<fm): return str(fz)+'/'+str(fm)
    return str(fz//fm)+'’'+str(fz%fm)+'/'+str(fm)

def add(x,y):   ##加法
    fz1,fm1=change(x)
    fz2,fm2=change(y)
    fz1,fz2=fz1*fm2,fz2*fm1 ##通分
    fz,fm=fz1+fz2,fm1*fm2
    x=math.gcd(fz,fm)   ##约分
    return fz//x,fm//x

def sub(x,y):      ##减法
    fz1,fm1=change(x)
    fz2,fm2=change(y)
    fz1,fz2=fz1*fm2,fz2*fm1     ##通分
    fz,fm=fz1-fz2,fm1*fm2
    x=math.gcd(fz,fm)       ##约分
    return fz//x,fm//x

def mul(x,y):       ##乘法
    fz1,fm1=change(x)
    fz2,fm2=change(y)
    fz,fm=fz1*fz2,fm1*fm2
    x=math.gcd(fz,fm)       ##约分
    return fz//x,fm//x

def div(x,y):       ##除法
    fz1,fm1=change(x)
    fm2,fz2=change(y)
    fz,fm=fz1*fz2,fm1*fm2
    x=math.gcd(fz,fm)       ##约分
    return fz//x,fm//x

def randomnumber(r):    ##随机生成一个数字
    if (r==1): op=1
    else: op=random.randint(1,3)        ##op为1则生成整数，为2则生成假分数，为3则生成真分数
    if (op==1):
        return str(random.randint(1,r))
    elif (op==2):
        fm=random.randint(2,r)
        fz=random.randint(1,fm-1)
        p=math.gcd(fm,fz)       ##通分
        return str(fz//p)+'/'+str(fm//p)
    else:
        fm=random.randint(2,r)
        fz=random.randint(1,fm-1)
        p=math.gcd(fm,fz)       ##通分
        return str(random.randint(1,r-1))+'’'+str(fz//p)+'/'+str(fm//p)

def cal(formula):       ##计算表达式的结果，并判断运算过程中是否产生负数和除0，若不符合则返回-1，符合则返回结果
    l_brack,r_brack=next((i for i in range(0,len(formula)) if formula[i]=='('),-1),next((i for i in range(0,len(formula)) if formula[i]==')'),-1)     ##返回左右括号的位置
    if (l_brack!=-1):       ##若有括号则先运算括号内的值
        f1,f2,f3=[],[],[]       ##f1中存计算完括号的表达式结果，f2中存括号内计算完*和/的结果，f3存f2计算完-的结果
        for i in range(0,l_brack):
            f1.append(formula[i])
        f2.append(formula[l_brack+1])
        for i in range(l_brack+2,r_brack):
            if (f2[-1]=='*'):
                f2.pop()
                fz,fm=mul(f2[-1],formula[i])
                f2.pop()
                f2.append(unchange(fz,fm))
            elif (f2[-1]=='/'):
                f2.pop()
                fz,fm=div(f2[-1],formula[i])
                if (fm==0): return -1
                f2.pop()
                f2.append(unchange(fz,fm))
            else: f2.append(formula[i])
        f3.append(f2[0])
        for i in range(1,len(f2)):
            if (f3[-1]=='-'):
                f3.pop()
                fz,fm=sub(f3[-1],f2[i])
                f3.pop()
                if (fz<0): return -1
                f3.append(unchange(fz,fm))
            else: f3.append(f2[i])
        p=f3[0]
        for i in range(1,len(f3)):
            if (f3[i]!='+'):
                fz,fm=add(p,f3[i])
                p=unchange(fz,fm)
        f1.append(p)
        for i in range(r_brack+1,len(formula)):
            f1.append(formula[i])
        formula=f1
    f1,f2=[],[]     ##f1存formula计算完*和/的结果，f2存f1计算完-的结果
    f1.append(formula[0])
    for i in range(1,len(formula)):
        if (f1[-1]=='*'):
            f1.pop()
            fz,fm=mul(f1[-1],formula[i])
            f1.pop()
            f1.append(unchange(fz,fm))
        elif (f1[-1]=='/'):
            f1.pop()
            fz,fm=div(f1[-1],formula[i])
            if (fm==0): return -1
            f1.pop()
            f1.append(unchange(fz,fm))
        else:
            f1.append(formula[i])
    f2.append(f1[0])
    for i in range(1,len(f1)):
        if (f2[-1]=='-'):
            f2.pop()
            fz,fm=sub(f2[-1],f1[i])
            f2.pop()
            if (fz<0): return -1
            f2.append(unchange(fz,fm))
        else:
            f2.append(f1[i])
    p=f2[0]
    for i in range(1,len(f2)):
        if (f2[i]!='+'):
            fz,fm=add(p,f2[i])
            p=unchange(fz,fm)
    return p

def work(n,r):
    nn=0        ##已产生表达式的数量
    while (nn<n):
        formula=[]
        symbol,brack=random.randint(1,3),random.randint(1,2)        ##symbol表示运算符的数量，brack表示是否有括号
        number=symbol+1     ##number表示数字的数量
        if (symbol==1): brack=1
        l_brack,r_brack=-1,-1
        if (brack==2):
            while (l_brack==r_brack or (l_brack==1 and r_brack==number)):   ##随机生成两个不同的数字作为左右括号的位置
                l_brack,r_brack=random.randint(1,number),random.randint(1,number)
                if (l_brack>r_brack): l_brack,r_brack=r_brack,l_brack       ##小的数字为左括号位置，大的数字为右括号位置
        if (l_brack==1): formula.append('(')
        formula.append(randomnumber(r))
        for i in range(1,symbol+1):
            fh=random.randint(0,3)      ##随机生成运算符的种类
            formula.append(k1[fh])
            if (i+1==l_brack): formula.append('(')
            formula.append(randomnumber(r))
            if (i+1==r_brack): formula.append(')')
        if (cal(formula)!=-1 and checkrepeat(formula)):      ##检查计算结果中无负数和表达式是否重复
            nn+=1
            ans.append(formula)
    f1=open("Exercises.txt","w")        ##输出结果
    f2=open("Answer.txt","w")
    for i in range(0,n):
        for j in range(0,len(ans[i])):
            if (ans[i][j] in k1):
                f1.write(' '+ans[i][j]+' ')
            else: f1.write(ans[i][j])
        f1.write(' =\n')
        f2.write(str(cal(ans[i]))+'\n')

def checkans(exercise,answer):
    while (exercise[-1]==''): exercise.pop()     ##将末尾的空串去除
    while (answer[-1]==''): answer.pop()
    m1,m2=len(exercise),len(answer)
    if (m1!=m2):
        print("答案与题目数目不同\n")
        return
    f1=open("Grade.txt","w")
    correct,wrong=[],[]
    for i in range(0,m2):
        e=exercise[i].split(' ')
        if (e[-1]=='='): e.pop()
        f=[]
        for j in range(0,len(e)):       ##将左右括号单独分开
            if (e[j] in k1): f.append(e[j])
            else:
                op=0        ##标记是否有右括号
                if (e[j].count('(')!=0): f.append('(')
                if (e[j].count(')')!=0): op=1
                e[j]=e[j].strip('()')       ##去除字符串中的左右括号
                f.append(e[j])
                if (op==1): f.append(')')
        if (cal(f)==answer[i]):
            correct.append(i+1)
        else: wrong.append(i+1)
    f1.write("Correct: %d ("%(len(correct)))        ##输出
    for i in range(0,len(correct)):
        f1.write("%d"%(correct[i]))
        if (i!=len(correct)-1): f1.write(",")
    f1.write(")\nWrong: %d ("%(len(wrong)))
    for i in range(0, len(wrong)):
        f1.write("%d"%(wrong[i]))
        if (i!=len(wrong)-1): f1.write(",")
    f1.write(")\n")


if __name__ == '__main__':
    read=input().split(' ')
    n=10
    while (len(read)<4): read.append('')
    if ((read[0]=='-e' and read[2]=='-a')or(read[0]=='-a' and read[2]=='-e')):
        if (read[0]=='-a'):
            read[1],read[3]=read[3],read[1]
        if (not os.path.exists(read[1])):
            print("题目文件路径不存在\n")
        elif (not os.path.exists(read[3])):
            print("答案文件路径不存在\n")
        else:
            with open(read[1],"r") as f:
                exercise=f.read()
            with open(read[3],"r") as f:
                answer=f.read()
            exercise,answer=exercise.split('\n'),answer.split('\n')
            checkans(exercise,answer)
    elif ((read[0]=="-r" and read[2]=='') or (read[0]=='-n' and read[2]=='-r') or (read[0]=='-r' and read[2]=='-n')):
        if (read[1].isdigit() and ((read[2]=='' and read[3]=='') or (read[3].isdigit()))):
            if (read[0]=='-n'): n=int(read[1])
            else: r=int(read[1])
            if (read[2]=='-n'): n=int(read[3])
            elif (read[2]=='-r'): r=int(read[3])
            work(n,r)
        else: print("参数错误\n")
    else: print("命令格式错误\n")