#include<cstdio>
#include<map>
#include<string>
#include<iostream>

using namespace std;

int main()
{
    map<int, string> m;

    m.insert(pair(<10, "good">));

    cout << m[0].front();
}