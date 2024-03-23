#include "animal.h"
#include <stdio.h>

void animalPrintGreeting(const Animal *animal) {
    const char *greetMsg = animal->vtbl->greet();
    printf("%s pozdravlja: %s\n", animalName(animal), greetMsg);
    return;
}

void animalPrintMenu(const Animal *animal) {
    const char *menuMsg = animal->vtbl->menu();
    printf("%s voli %s\n", animalName(animal), menuMsg);
    return;
}

const char *animalName(const Animal *animal) {
	return animal->vtbl->name(animal);
}