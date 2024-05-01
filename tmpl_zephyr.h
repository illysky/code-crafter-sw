/*
{##_LOGO_##}

{##_DESCRIPTION_##} {##_VERSION_##}
{##_COPYRIGHT_##}
*/   

#ifndef __{##_DEVICE_##}_H
#define __{##_DEVICE_##}_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/{##_BUS_##}.h>
#include <zephyr/drivers/gpio.h>

{##_TYPEDEFS_##}

#ifdef __cplusplus
}
#endif
#endif // {##_DEVICE_##}_H