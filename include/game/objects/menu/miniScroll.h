#ifndef MINI_SCROLL_H
#define MINI_SCROLL_H

#include "cv64.h"
#include "gfx/camera.h"
#include "object.h"

typedef enum miniScroll_flags {
    MINISCROLL_FLAG_00000001 = 0x00000001,
    MINISCROLL_FLAG_00000004 = 0x00000004,
    MINISCROLL_FLAG_08000000 = 0x08000000
} miniScroll_flags;

// ID: 0x213E
typedef struct {
    cv64_object_hdr_t header;
    u8 field_0x20[4];
    cv64_model_inf_t* model;
    u8 field_0x28[12];
    /**
     * Vertices buffer
     * TODO: This may need its own struct
     */
    void* vtx_buffer;
    u32 flags;
    s32 field_0x3C;
    s32 field_0x40;
    s32 field_0x44;
    vec3f position;
    f32 open_max_height;
    vec3f width;
    s32 field_0x64;
    s32 field_0x68;
    s32 field_0x6C;
    camera* display_camera;
} miniScroll;

extern miniScroll* createMiniScroll(void* parent, camera* camera, s32 param_3, s32 param_4);
extern u32 miniScroll_checkFlags(miniScroll* self, u32 flags);
extern void miniScroll_editFlags(miniScroll* self, u32 flags, s32 setFlags);
extern cv64_model_inf_t* miniScroll_getModel(miniScroll* self);
extern void miniScroll_setFlags(miniScroll* self, u32 flags);
extern void miniScroll_setOpenMaxHeight(miniScroll* self, f32 open_max_height, s32 param_3);
extern void miniScroll_setPosition(miniScroll* self, f32 X, f32 Y, f32 Z);
extern void miniScroll_setWidth(miniScroll* self, f32 X, f32 Y, f32 Z);

typedef void (*miniScroll_func_t)(miniScroll*);

#endif
