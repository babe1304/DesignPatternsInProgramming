#include <stdlib.h>

typedef const char* (*PTRFUN)();
typedef struct Parrot_Vtable Parrot_Vtable;
typedef struct Parrot Parrot;

struct Parrot_Vtable {
	PTRFUN name;
    PTRFUN greet;
    PTRFUN menu;
};

struct Parrot {
    const Parrot_Vtable *vtbl;
    const char *name;
};

const char *name_parrot_impl(const Parrot *parrot) {
	return parrot->name;
}

const char *greet_parrot_impl(void) {
	return "papiga!";
}

const char *menu_parrot_impl(void) {
	return "kikiriki";
}

static Parrot_Vtable vtbl = {
	.name = &name_parrot_impl,
	.greet = &greet_parrot_impl,
	.menu = &menu_parrot_impl
};

size_t sizeOf(void) {
	return sizeof(Parrot);
}

void construct(void *obj, const char *name) {
	Parrot *p = (Parrot *) obj;
	p->vtbl = &vtbl;
	p->name = name;
}

void *create(const char *name) {
	void *obj = malloc(sizeOf());
	construct(obj, name);
	return obj;
}