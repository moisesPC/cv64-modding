/**
 * @file obj_test.c
 *
 * Test object / actor that will replace object 0x213F, which is used
 * at Castle Wall (Main), but doesn't really have any important functionality.
 * 
 * This object will print "Hello world!" and the player's screen to the debugging console
 * every 3 seconds.
 * Use the following script to view the contents of the debugging console in an emulator:
 * https://github.com/LuigiBlood/EmuScripts/blob/c9fef6bd6e109130d5d84746648a5c0180492726/N64/Project64_JSAPI2/Partner-N64_CartMapper.js
 * 
 * This code will be compiled as a Nisitenma-Ichigo overlay, and replace file ID 0xBA.
 */

#include <ultra64.h>
#include "objects/player/player.h"
#include "system_work.h"
#include "obj_test.h"

objTest_funcs objTest_functions[] = {
    objTest_init,
    objTest_loop,
    objTest_destroy
};

void objTest_entrypoint(objTest* self) {
    ENTER(self, objTest_functions);
}

void objTest_init(objTest* self) {
    /* Additional initialization code goes here */

    object_curLevel_goToNextFuncAndClearTimer(self->header.current_function, &self->header.function_info_ID);
}

void objTest_loop(objTest* self) {
    if (ptr_PlayerData != NULL) {
    // Print "Hello world" and the player's speed every 3 seconds (90 frames when the target framerate is 30FPS)
        if (sys.global_timer_capped % 90 == 0) {
            osSyncPrintf("Hello world!\n");

            Vec3f* player_speed_vector = &ptr_PlayerData->speed;
            f32 player_speed_XYZ = sqrtf(player_speed_vector->x * player_speed_vector->x + player_speed_vector->y * player_speed_vector->y + player_speed_vector->z * player_speed_vector->z);
            osSyncPrintf("Player's XYZ speed: %.4f\n\n", player_speed_XYZ);
        }
    }
}

void objTest_destroy(objTest* self) {
    self->header.destroy(self);
}
