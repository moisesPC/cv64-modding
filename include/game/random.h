#ifndef RANDOM_H
#define RANDOM_H

#include <ultra64.h>

extern s32 rand();
extern f32 rand_f32();
extern void random_initSeed();
extern u16 random_range(u16 limit);
extern void srand(u32 seed);
extern s32 getRandomFromGuRandom();

extern u32 seed_RNG_C_rand_srand;

#endif
