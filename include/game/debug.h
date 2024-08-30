#ifndef DEBUG_H
#define DEBUG_H

// General debug functions

#include "cv64.h"
#include <ultra64.h>

typedef enum dbg_processmeter_state {
    START_GREEN_BAR,
    END_GREEN_BAR,
    START_BLUE_BAR,
    END_BLUE_BAR
} dbg_processmeter_state_t;

extern void func_80019BC0_1A7C0();
extern void func_80019BC8_1A7C8(s32);
extern void func_80019BD0_1A7D0(s32 arg0, s32 arg1, s32 arg2, s32 arg3);
extern void func_80019BE4_1A7E4(s32, s32, s32, s32);
extern void func_80019BF8_1A7F8();
extern void processMeter_updateTiming(OSMesgQueue*);
extern void processMeter_setSizeDivisor(f32 size_divisor);
extern extern void processMeter_update(s32 state);
extern extern void processMeter_render(Gfx** dlist);
extern void processMeter_renderDivisions(Gfx** dlist, f32 division_width);
extern void processMeter_renderBar(Gfx** dlist, u32 color, f32 bar_size, s32 row);
extern void crashScreen_Init();

#endif
