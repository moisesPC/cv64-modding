#ifndef CONTRACT_MGR_H
#define CONTRACT_MGR_H

#include "objects/cutscene/interactables.h"
#include "objects/effect/distortion.h"

// ID: 0x213B
typedef struct {
    ObjectHeader header;
    u8 field_0x20[20];
    Interactable* contract_item;
    void* field_0x38;
    s32 field_0x3C;
    obj_distortion* distortion;
    u8 field_0x44[OBJECT_SIZE - 0x44];
} contractMgr;

#endif
