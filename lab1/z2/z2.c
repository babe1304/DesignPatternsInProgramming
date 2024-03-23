#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// Unary_Function
typedef struct Unary_Function_vtable Unary_Function_vtable;
typedef struct Unary_Function Unary_Function;

struct Unary_Function {
    Unary_Function_vtable* vtable;
    int lower_bound;
    int upper_bound;
};

struct Unary_Function_vtable {
    double (*value_at)(Unary_Function *, double);
    double (*negative_value_at)(Unary_Function *, double);
};

double negative_value_at(Unary_Function *o, double x) {
    return -(o->vtable->value_at(o, x));
};

Unary_Function_vtable unary_vtable = {
    value_at: NULL,
    negative_value_at: &negative_value_at,
};

void tabulate(Unary_Function *o) {
    for(int x = o->lower_bound; x <= o->upper_bound; x++) {
        printf("f(%d)=%lf\n", x, o->vtable->value_at(o, x));
      }
};

void Unary_Function_construct(Unary_Function *o, int lower_bound, int upper_bound) {
    o->lower_bound = lower_bound;
    o->upper_bound = upper_bound;
    o->vtable = &unary_vtable;
};

bool same_functions_for_ints(Unary_Function *f1, Unary_Function *f2, double tolerance) {
	if (f1->lower_bound != f2->lower_bound)
        return false;
    if (f1->upper_bound != f2->upper_bound)
        return false;
    for (int x = f1->lower_bound; x <= f1->upper_bound; x++) {
        double delta = f1->vtable->value_at(f1, x) - f2->vtable->value_at(f2, x);
        if (delta < 0)
            delta = -delta;
        if (delta > tolerance)
            return false;
   	}
    return true;
};

// Linear
typedef struct Linear_vtable Linear_vtable;

typedef struct {
    Linear_vtable* vtable; 
    int lower_bound;
    int upper_bound;
    double a; 
    double b;
} Linear;

struct Linear_vtable {
    double (*value_at)(Linear *, double);
    double (*negative_value_at)(Unary_Function *, double);
};

double linear_value_at(Linear *o, double x) {
    return o->a * x + o->b;
};

Linear_vtable linear_vtable = {
    value_at: &linear_value_at,
    negative_value_at: &negative_value_at,
};

Linear* Linear_create(int lower_bound, int upper_bound, double a_coef, double b_coef) {
    Linear* linear = malloc(sizeof(Linear));
    Unary_Function_construct((Unary_Function*) linear, lower_bound, upper_bound);
    linear->a = a_coef;
    linear->b = b_coef;
    linear->vtable = &linear_vtable;
    return linear;
};

// Square
typedef struct Square_vtable Square_vtable;

typedef struct {
    Square_vtable* vtable;
    int lower_bound;
    int upper_bound;
} Square;

struct Square_vtable {
    double (*value_at)(Square *, double);
    double (*negative_value_at)(Unary_Function *, double);
};

double sqaure_value_at(Square* o, double x) {
    return x*x;
};

Square_vtable sqaure_vtable = {
    value_at: &sqaure_value_at,
    negative_value_at: &negative_value_at,
};

Square* Square_create(int lower_bound, int upper_bound) {
    Square* square = malloc(sizeof(Square));
    Unary_Function_construct((Unary_Function*) square, lower_bound, upper_bound);
    square->vtable = &sqaure_vtable;
    return square;
};

int main() {
  Square* s1 = Square_create(-2, 2);
  Unary_Function *f1 = (Unary_Function *) s1;
  tabulate(f1);

  Linear* l1 = Linear_create(-2, 2, 5, -2);
  Unary_Function *f2 = (Unary_Function *) l1;
  tabulate(f2);

  printf("f1==f2: %s\n", same_functions_for_ints(f1, f2, 1E-6) ? "DA" : "NE");
  printf("neg_val f2(1) = %lf\n", f2->vtable->negative_value_at(f2, 1.0));
  free(f1);
  free(f2);
  return 0;
}