#ifndef ENEMY_TARGET_GFX_H
#define ENEMY_TARGET_GFX_H

#include "actor.h"

typedef enum enemyTargetData_flags {
    FACING_ENEMY         = 0x0001,
    RETICLE_TURNS_RED    = 0x0002,
    NOT_FACING_ENEMY     = 0x0004,
    RETICLE_TURNS_YELLOW = 0x0008,
    HIDE_RETICLE         = 0x8000
} enemyTargetData_flags;

typedef struct {
    u16 flags;
    vec3s field_0x02;
    vec3f field_0x08;
    f32 height_targetGfx_player; // The height difference between the enemy target gfx and the player
    f32 reticle_display_distance; // The maximum distance between the player and the enemy that makes the reticle appear. If you're beyond this distance, the reticle will hide
    animation_info spinning_anim_info;
    cv64_actor_t* targeted_enemy_ptr; // The enemy that has the reticle over them
    s16 field_0x34;
    s16 field_0x36;
    cv64_actor_t* red_targeted_enemy_ptr; // The enemy that has the red reticle over them
    vec3f enemy_position;
    vec3f distance_enemy_player;    // The distance between the enemy and the player
    cv64_actor_t* facing_enemy_ptr; // The enemy you're facing
    vec3f field_0x58;
    cv64_actor_t* field_0x64; // This is written to, but never read from?
    vec3f enemy_to_player_distance;
} enemyTargetData_t;

// ID: 0x007A
typedef struct {
    cv64_object_hdr_t header;
    u8 field_0x20[4];
    cv64_model_inf_t* model;
    u8 field_0x28[72];
    enemyTargetData_t* data;
} enemyTargetGfx;

extern void enemyTargetGfx_entrypoint(enemyTargetGfx* self);
extern void enemyTargetGfx_init(enemyTargetGfx* self);
extern void enemyTargetGfx_onTarget(enemyTargetGfx* self);
extern void func_800260F8_26CF8(enemyTargetGfx* self);
extern void enemyTargetGfx_hidden(enemyTargetGfx* self);

typedef void (*enemyTargetGfx_func_t)(enemyTargetGfx*);

extern enemyTargetGfx_func_t enemyTargetGfx_functions[];
extern s32 enemyTargetGfx_hierarchy;

typedef enum enemyTargetGfx_func_id {
    ENEMYTARGETGFX_INIT,
    ENEMYTARGETGFX_ON_TARGET,
    FUNC_800260F8,
    ENEMYTARGETGFX_HIDDEN
} enemyTargetGfx_func_id_t;

extern enemyTargetGfx* ptr_enemyTargetGfx;

#endif
