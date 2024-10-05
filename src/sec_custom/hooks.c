#include "cv64.h"

#include "objects/player/player.h"
#include "objects/engine/GameStateMgr.h"
#include "system_work.h"

/**
 * Returns `TRUE` if all gameplay state subsystems have been initialized.
 * 
 * This is a safe way of checking if gameplay has started before accessing
 * any of its elements.
 */
s32 insideGameplay() {
    return ((ptr_PlayerData != NULL) && (sys.map_is_setup) && (ptr_GameStateMgr->current_game_state == GAMESTATE_GAMEPLAY));
}

/**
 * Called once, right after the custom segment is loaded during bootup
 * Extra initialization code can go here
 */
void hook_customSegmentInit() {
    /**
     * Optional: Initialize the crash screen thread to be able
     * to see debug output to the console when the game crashes
     */
    crashScreen_Init();
}

/**
 * Called every frame at 60FPS
 */
void hook_customSegmentLoop() {
    /* Hold L to levitate */
    if (insideGameplay()) {
        if (CONT_BTNS_HELD(CONT_0, L_TRIG)) {
            sys.ptr_PlayerObject->header.current_function[0].function = PLAYER_JUMP;
            sys.ptr_PlayerObject->header.current_function[1].function = 7;   // Calls `Player_jump_fastMove_down`

            ptr_PlayerData->speed.y = 2.0f;
            ptr_PlayerData->visualData.flags |= PLAYER_FLAG_JUMPING;
            /**
             * Avoids a glitch where levitating while taking damage
             * damages you again, but has the side effect of the player becoming
             * invincible if they try to levitate when they take damage at least once.
             */
            ptr_PlayerData->visualData.flags &= ~PLAYER_FLAG_DAMAGED;
        }
    }

    /**
     * The code we replaced with our hook originally calls `controller_readData`
     * Make the call here at the very end to resume normal execution
     */
    controller_readData();
}
