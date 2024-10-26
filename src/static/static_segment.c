#include "mod.h"

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
    /* Your initialization code goes here */

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
    /* Your loop code goes here */

    /**
     * The code we replaced with our hook originally calls `controller_readData`
     * Make the call here at the very end to resume normal execution
     */
    controller_readData();
}
