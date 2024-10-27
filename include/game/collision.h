#ifndef COLLISION_H
#define COLLISION_H

#include "math.h"
#include <ultra64.h>

#define COLL_TYPE_FLOOR   1
#define COLL_TYPE_WALL    2
#define COLL_TYPE_CEILING 4 // Officially known as "TOP"

#define COLL_TYPE_FLOOR_FULL_WORD     0x00010000
#define COLL_TYPE_WALL_FULL_WORD      0x00020000
#define COLL_TYPE_CEILING_FULL_WORD   0x00040000

#define FOOTSTEP_SFX_STONE     0x00000001

typedef struct CollisionTri {
    union {
        u8 type;
        // For example, footstep_sfx. If 0x80, fall death.
        // If 0xA2, lava death.
        u8 variable;
        u16 type_and_variable;
    };
    Vec3 vtx_pos[3]; // Vertices positions
} CollisionTri;

#endif
