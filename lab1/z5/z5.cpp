#include <iostream>

using namespace std;

class B{
public:
  virtual int prva()=0;
  virtual int druga(int)=0;
};

class D: public B{
public:
  virtual int prva(){return 42;}
  virtual int druga(int x){return prva()+x;}
};

void fun(B* b) {
    typedef unsigned long long addr;
    typedef int (*prva_funkcija)(B*);
    typedef int (*druga_funkcija)(B*, int);

    addr* vt = (addr *) *((addr *) b);

    prva_funkcija p_fun = (prva_funkcija) vt[0];
    druga_funkcija d_fun = (druga_funkcija) vt[1];

    cout << p_fun(b) << endl;
    cout << d_fun(b, 42) << endl;
    return;
}

int main(void) {
    B* b = new D;
    fun(b);
}