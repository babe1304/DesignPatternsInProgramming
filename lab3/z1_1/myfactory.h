#ifndef MYFACTORY_H
#define MYFACTORY_H

#include <stddef.h>

size_t libsize(char const *libname);
void *myfac(char const* libname, void *mem, char const* ctorarg);
void *myfactory(char const* libname, char const* ctorarg);

#endif