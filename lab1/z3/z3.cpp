#include <stdio.h>
#include <stdlib.h>
#include <iostream>

class CoolClass{
public:
  virtual void set(int x){x_=x;};
  virtual int get(){return x_;};
private:
  int x_;
};

class PlainOldClass{
public:
  void set(int x){x_=x;};
  int get(){return x_;};
private:
  int x_;
};

int main(void) {
    std::cout << "Size of PlainOldClass: " << sizeof(PlainOldClass) << "\n";
    std::cout << "Size of CoolClass: " << sizeof(CoolClass) << "\n";
}