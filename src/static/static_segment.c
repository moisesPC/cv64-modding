#include "item.h"

u32 data_var = 10;
const u32 rodata_var = 3;
u32 bss_var;

void static_main() {
    data_var += ITEM_MATERIAL_DL * rodata_var;
    bss_var  *= ITEM_MATERIAL_DL;
}
