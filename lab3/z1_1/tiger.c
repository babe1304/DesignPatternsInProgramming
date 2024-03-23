#include <stdlib.h>

typedef const char* (*PTRFUN)();
typedef struct Tiger_Vtable Tiger_Vtable;
typedef struct Tiger Tiger;

struct Tiger_Vtable {
	PTRFUN name;
    PTRFUN greet;
    PTRFUN menu;
};

struct Tiger {
    const Tiger_Vtable *vtbl;
    const char *name;
};

const char *name_tiger_impl(const Tiger *tiger) {
	return tiger->name;
}

const char *greet_tiger_impl(void) {
	return "roar!";
}

const char *menu_tiger_impl(void) {
	return "mesa";
}

static Tiger_Vtable vtbl = {
	.name = &name_tiger_impl,
	.greet = &greet_tiger_impl,
	.menu = &menu_tiger_impl
};

size_t sizeOf(void) {
	return sizeof(Tiger);
}

void construct(void *obj, const char *name) {
	Tiger *t = (Tiger *) obj;
	t->vtbl = &vtbl;
	t->name = name;
}

void *create(const char *name) {
	void *obj = malloc(sizeOf());
	construct(obj, name);
	return obj;
}