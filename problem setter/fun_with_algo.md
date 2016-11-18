## Problem name
Fun with Algorithm

## Problem Statement
I am kind of inquisitive learner so once while I was changing directory in Linux using cd command in command prompt I noticed this.

```
root@kali:~$ cd D                                         (pressing tab)
Desktop/ Documents/ Downloads/
root@kali:~$ cd De                                        (pressing tab )
root@kali:~$ cd Desktop/
```

I was kind of amazed to see this feature but could not understand the inside working. I need your help to solve this mystery.

## Input format  
Initially, your are given n number of strings, m number of queries.   
Next n lines follow strings s.  
Next m lines follow strings k.  

Each string k is inputted as:  
cd “string k”  

## output format
for every string k print all the strings s whose prefix matches in following ways, 

if one string  
cd “string s” + “/” (new line)

if more than one string  
“string s1” + “/” + “ ”“string s2” + “/” + “ ”..... (newline)

It is confirmed that atleast one string will match.

## constraints:
1<=n<=5000  
1<=m<=10000  
1<=length(s)<=1000  
1<=length(k)<=1000  

## input
5 4  
hi  
hello  
help  
heal  
heaven  
cd h  
cd he  
cd hea  
cd heav  



## Output :  
```
hi/ hello/ help/ heal/ heaven/
hello/ help/ heal/ heaven/
heal/ heaven/
cd heaven/
```

## my program
```c++
#include <bits/stdc++.h>
using namespace std;
#ifndef M
#define M 1000000007
#endif
typedef long long ll;
typedef pair<int,int>pp;
typedef std::vector<pp> vpp;
typedef long double ld;
#ifndef pb
#define pb push_back 
#endif 
int min(int x,int y){return(x<y)?x:y;}
int max(int x,int y){return(x>y)?x:y;}
typedef struct $
{
    struct $ **m;
    int *a,index;
}hell;
hell *init()
{
    hell *a=(hell *)malloc(sizeof(a));
    a->m=(hell **)malloc(27*sizeof(hell *));
    a->a=(int *)malloc(1000*sizeof(int));
    a->index=0;
    for(int i=0;i<26;i++)
        a->m[i]=NULL;
    return a;
}
void construct(char *s,hell *root,int index,int pos)
{
    if(s[index]=='\0')
        return;
    if(root->m[s[index]-'a']==NULL)
        root->m[s[index]-'a']=init();
    root->a[root->index++]=pos;
    construct(s,root->m[s[index]-'a'],index+1,pos);
}
hell *x;
void query(char s[],hell *root,int index)
{
    if(s[index]=='\0' || root->m[s[index]-'a']==NULL)
        return;
    else
    {
        x=root->m[s[index]-'a'];
        query(s,root->m[s[index]-'a'],index+1);
    }
}
char s[1000006];
int main()
{
    int n,q;
    scanf("%d %d",&n,&q);
    getchar();
    hell *start=init();
    std::vector<char *> v;
    for(int i=0;i<n;i++)
        v.pb((char *)malloc(1000 * sizeof(char)));
    for(int i=0;i<n;i++)
    {
        scanf("%s",v[i]);
        construct(v[i],start,0,i);
    }
    while(q--)
    {
        scanf("%s",s);
        scanf("%s",s);
        query(s,start,0);
        if(x->index==1)
            printf("cd ");
        for(int i=0;i<x->index;i++)
            printf("%s\\ ",v[x->a[i]]);
        printf("\n");
    }
    return 0;
}

```
