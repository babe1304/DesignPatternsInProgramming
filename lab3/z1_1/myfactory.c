#include "myfactory.h"
#include <stdlib.h>
#include <dlfcn.h>
#include <string.h>

typedef void* (*CREATE_FUN)(const char *);
typedef size_t (*SIZEOF_FUN)(void);
typedef void (*CONSTRUCT_FUN)(void *, const char *);

static const char *cwd = "./";
static const char *extension = ".so";
static const char *sym_create = "create";
static const char *sym_construct = "construct";
static const char *sym_sizeof = "sizeOf";

size_t libsize(char const *libname) {

};

void *myfac(char const* libname, void *mem, char const* ctorarg) {

};

void *myfactory(char const* libname, char const* ctorarg) {
    int length = strlen(cwd) + strlen(libname) + strlen(extension) + 1;
    char loc[length];
    strcpy(loc, cwd); strcat(loc, libname); strcat(loc, extension);

    void *o = dlopen(loc, RTLD_LAZY);
    if (o == NULL) return NULL;

    void *fac = dlsym(o, "create");
	if (fac == NULL) return NULL;

    CREATE_FUN cf = (CREATE_FUN) fac;
	void *obj = cf(ctorarg);
	// dlclose(handle);
	
	return obj;

};
