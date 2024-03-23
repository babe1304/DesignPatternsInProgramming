#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

typedef struct Animal_vtable {
  const PTRFUN greet;
  const PTRFUN menu;
} Animal_vtable;

typedef struct Animal {
    const Animal_vtable* vtable;
    const char* name;
} Animal;

char const* dogGreet(void){
  return "vau!";
}
char const* dogMenu(void){
  return "kuhanu govedinu";
}
char const* catGreet(void){
  return "mijau!";
}
char const* catMenu(void){
  return "konzerviranu tunjevinu";
}

const Animal_vtable catfun = { greet: catGreet, menu: catMenu };
const Animal_vtable dogfun = { greet: dogGreet, menu: dogMenu };

void animalPrintGreeting(Animal* animal) {
    printf("%s pozdravlja: %s\n", animal->name, animal->vtable->greet());
}

void animalPrintMenu(Animal* animal) {
    printf("%s voli %s\n", animal->name, animal->vtable->menu());
}

void constructDog(Animal* animal, const char* name) {
    animal->vtable = &dogfun;
    animal->name = name;
}

void constructCat(Animal* animal, const char* name) {
    animal->vtable = &catfun;
    animal->name = name;
}

Animal* createCat(const char* name) {
    Animal* animal = malloc(sizeof(Animal));
    constructCat(animal, name);
    return animal;
}

Animal* createDog(const char*  name) {
    Animal* animal = malloc(sizeof(Animal));
    constructDog(animal, name);
    return animal;
}

Animal createDogStack(const char*  name) {
    Animal animal;
    constructDog(&animal, name);
    return animal;
}

Animal createCatStack(const char*  name) {
    Animal animal;
    constructDog(&animal, name);
    return animal;
}

Animal* createDogs(int n, const char** names) {
    Animal* animals = malloc(n * sizeof(Animal));
    for (int i = 0; i < n; i++) {
      constructDog(&animals[i], names[i]);
    }
    return animals;
}

void testAnimals(void){
  Animal* p1=createDog("Hamlet");
  Animal* p2=createCat("Ofelija");
  Animal* p3=createDog("Polonije");

  animalPrintGreeting(p1);
  animalPrintGreeting(p2);
  animalPrintGreeting(p3);

  animalPrintMenu(p1);
  animalPrintMenu(p2);
  animalPrintMenu(p3);

  const char* names[] = {"Bruno", "Loris"};
  Animal* animals = createDogs(2, names);
  
  animalPrintGreeting(&animals[0]);
  animalPrintGreeting(&animals[1]);

  animalPrintMenu(&animals[0]);
  animalPrintMenu(&animals[1]);

  free(p1); free(p2); free(p3); free(animals);
}

int main (void) {
    testAnimals();
}