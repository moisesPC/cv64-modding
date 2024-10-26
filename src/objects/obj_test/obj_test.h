/**
 * @file obj_test.h
 *
 * Main header file for `obj_test.c`
 */

#ifndef OBJ_TEST_H
#define OBJ_TEST_H

#include "object.h"

// ID: 0x213F (replaces the vanilla game's `object_213F`)
typedef struct {
    ObjectHeader header;
    u8 field_0x20[OBJECT_SIZE - 0x20];
} objTest;
_Static_assert(sizeof(objTest) == OBJECT_SIZE, "ERROR: Objects can only be 0x74 bytes long");

void objTest_entrypoint(objTest* self);
void objTest_init(objTest* self);
void objTest_loop(objTest* self);
void objTest_destroy(objTest* self);

typedef void (*objTest_funcs)(objTest*);

#endif
