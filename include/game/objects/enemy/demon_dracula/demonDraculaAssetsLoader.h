#ifndef DEMON_DRACULA_ASSETS_LOADER_H
#define DEMON_DRACULA_ASSETS_LOADER_H

#include "object.h"

// ID: 0x20B7
typedef struct {
    cv64_object_hdr_t header;
    u8 field_0x20[OBJECT_SIZE - 0x20];
} demonDraculaAssetsLoader;

void demonDraculaAssetsLoader_entrypoint(demonDraculaAssetsLoader* self);

#endif
