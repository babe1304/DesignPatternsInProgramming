#ifndef ANIMAL_H
#define ANIMAL_H

typedef const char* (*PTRFUN)();
typedef struct Animal_Vtable Animal_Vtable;
typedef struct Animal Animal;

struct Animal_Vtable {
	PTRFUN name;
    PTRFUN greet;
    PTRFUN menu;
};

struct Animal {
    const Animal_Vtable *vtbl;
};

void animalPrintGreeting(const Animal *animal);
void animalPrintMenu(const Animal *animal);
const char *animalName(const Animal *animal);

#endif