#ifndef DEMO50_H
#define DEMO50_H

#include "cutscene.h"
#include "animation.h"
#include "objects/enemy/death.h"

typedef struct Demo50Data {
    Model* death_model[1];
    animationMgr* death_anim_mgr[1];
    Camera* cutscene_camera;
    Model* player_model;
    Camera* game_camera;
    CutsceneCurrentCameraMovement current_camera_movement;
    CutsceneCameraMovementState field_0x28[1];
    CutsceneCameraMovementState field_0x44;
    CutsceneCameraMovementState field_0x60;
    CutsceneCameraMovementState field_0x7C;
    DeathData* death_data;
} Demo50Data;

// ID: 0x2059
typedef struct Demo50 {
    ObjectHeader header;
    u8 field_0x20[4];
    Camera* cutscene_camera;
    Death* death;
    u8 field_0x2C[8];
    Demo50Data* data;
    u8 field_0x38[48];
    u16 current_time;
    s16 max_time;
    u8 field_0x6C[4];
    u8 skip_cutscene;
    u8 set_player_anim_speed;
    u8 state;
    u8 field_0x73;
} Demo50;

void Demo50_Entrypoint(Demo50* self);
void Demo50_Init(Demo50* self);
void Demo50_SetupMainCutsceneParams(Demo50* self);
void Demo50_SetupData(Demo50* self);
void Demo50_Loop(Demo50* self);
void Demo50_Restart(Demo50* self);
void Demo50_PlayDeathAnimations(Demo50* self, CutsceneCoordinatesConfig* coords);

typedef void (*Demo50Func)(Demo50*);

typedef enum Demo50FuncID {
    DEMO50_INIT,
    DEMO50_SETUP_MAIN_CUTSCENE_PARAMS,
    DEMO50_SETUP_DATA,
    DEMO50_LOOP,
    DEMO50_RESTART
} Demo50FuncID;

#endif
