#include "mod.h"

#include <ultra64.h>
#include "objects/player/player.h"
#include "crash_screen.h"
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
 * Returns `TRUE` if the Expansion Pak is installed
 */
s32 expansionPakInstalled() {
    return (osMemSize >= 0x800000);
}

/**
 * Called once, right after the custom segment is loaded during bootup
 * Extra initialization code can go here
 */
void customSegment_init() {
    /* Your initialization code goes here */
    osSyncPrintf("Custom static segment loaded!\n\n");

    /**
     * Optional: Initialize the crash screen thread to be able
     * to see debug output to the console when the game crashes
     */
    crashScreen_Init();
}

/**
 * Called every frame at 60FPS
 */
void customSegment_loop() {
    /* Your loop code goes here */

    /* Warp to the Test Grid when holding L + R + Z on the first controller */
    /* We have a custom modded Test Grid map where we defined some custom actors */
    if (insideGameplay()) {
        if (CONT_BTNS_HELD(CONT_0, L_TRIG) && CONT_BTNS_HELD(CONT_0, R_TRIG) && CONT_BTNS_HELD(CONT_0, Z_TRIG)) {
            sys.map = TEST_GRID;
            sys.spawn = 0;
        }
    }

    /**
     * The code we replaced with our hook originally calls `controller_readData`
     * Make the call here at the very end to resume normal execution
     */
    controller_readData();
}
