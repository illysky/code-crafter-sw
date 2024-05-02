/*
 ____   ____  _______     _________ _____            _  __
|  _ \ / __ \|  __ \ \   / /__   __|  __ \     /\   | |/ /
| |_) | |  | | |  | \ \_/ /   | |  | |__) |   /  \  | ' / 
|  _ <| |  | | |  | |\   /    | |  |  _  /   / /\ \ |  <  
| |_) | |__| | |__| | | |     | |  | | \ \  / ____ \| . \ 
|____/ \____/|_____/  |_|     |_|  |_|  \_\/_/    \_\_|\_\

 Driver for TI BQ25792 v1.0.0
 Copyright (c) 2023 Inova Design Solutions Ltd
 */  

#ifndef __HAL_H
#define __HAL_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct  
{
    int32_t (*write)(uint8_t addr, uint8_t* data, uint32_t size); 
    int32_t (*read)(uint8_t addr, uint8_t* data, uint32_t size); 
    uint8_t dev_addr; 
} hal_i2c_t; 


#ifdef __cplusplus
}
#endif
#endif // TI_BQ25792_H