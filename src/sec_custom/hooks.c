#include <cv64.h>

#include "objects/player/player.h"
#include "system_work.h"

// Called once, right after the custom segment is loaded during bootup
// Extra initilisation code can go here
void hook_customSegmentInit() {
    
}

// Called every frame at 60FPS
void hook_customSegmentLoop() {
    /* Hold L to levitate */
    if ((ptr_PlayerData != NULL) && sys.map_is_setup) {
        if (CONT_BTNS_HELD(CONT_0, L_TRIG)) {
            sys.ptr_PlayerObject->header.current_function[0].function = PLAYER_JUMP;
            sys.ptr_PlayerObject->header.current_function[1].function = 7;   // Calls `Player_jump_fastMove_down`

            ptr_PlayerData->speed.y = 2.0f;
            ptr_PlayerData->visualData.flags |= JUMPING;
            // Avoid a glitch where levitating while taking damage
            // damages you again, but has the side effect of the player becoming
            // invincible if they try to levitate when they take damage at least once.
            ptr_PlayerData->visualData.flags &= ~DAMAGED;
        }
    }

    // The code we replaced with our hook originally calls `controller_readData`
    // Make the call here at the very end to resume normal execution
    controller_readData();
}
