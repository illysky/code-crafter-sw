/*
{##_LOGO_##}

{##_DESCRIPTION_##} {##_VERSION_##}
{##_COPYRIGHT_##}
*/  

#define DT_DRV_COMPAT {##_MANU_##}_{##_DEVICE_LOWER_##}

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/{##_BUS_##}.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/logging/log.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/drivers/charger.h>
#include "{##_DEVICE_LOWER_##}.h"

LOG_MODULE_REGISTER({##_DEVICE_LOWER_##}, CONFIG_{##_API_UPPER_##}_LOG_LEVEL);

// ##################################################################
// Config Structure 
// ##################################################################
struct {##_DEVICE_LOWER_##}_config 
{
	// Add more elements to config stuct as need, eg gpios for irqs
	// Remember to update instantiation if you need
	// them initialised at boot
	struct {##_BUS_##}_dt_spec {##_BUS_##};

};

// ##################################################################
// Data Structure 
// ##################################################################
struct {##_DEVICE_LOWER_##}_data
{
	// Add more elements to the driver data structure that need to 
	// persist at runtime. Remove if not needed
	bool ready;
	
};

// ##################################################################
// Private Functions 
// ##################################################################
{##_FUNCTIONS_##}
// ##################################################################
// Driver API Implementation
// ##################################################################
// Visit https://docs.zephyrproject.org/latest/develop/api/overview.html 
// to get the API calls you need to implement for this type of driver
// eg. sensor or charger. 
// Update the _driver_api struct accordingly 

// ##################################################################
// Driver API 
// ##################################################################
static const struct {##_API_L_##}_driver_api {##_DEVICE_LOWER_##}_api = 
{
	// Manually add api calls here...
};

// ##################################################################
// Init 
// ##################################################################
static int {##_DEVICE_LOWER_##}_init(const struct device *dev)
{
	const struct {##_DEVICE_LOWER_##}_config *cfg = dev->config;
	
	// Init code added here
	
	return 0;
}


// ##################################################################
// Instantiation 
// ##################################################################
#define {##_DEVICE_UPPER_##}_INIT(inst) \
	static const struct {##_DEVICE_LOWER_##}_config {##_DEVICE_LOWER_##}_config_##inst = {.i2c = I2C_DT_SPEC_INST_GET(inst)};\
	static struct {##_DEVICE_LOWER_##}_data {##_DEVICE_LOWER_##}_data_##inst;	\
	DEVICE_DT_INST_DEFINE(inst, {##_DEVICE_LOWER_##}_init, NULL, &{##_DEVICE_LOWER_##}_data_##inst, &{##_DEVICE_LOWER_##}_config_##inst, POST_KERNEL, CONFIG_{##_API_UPPER_##}_INIT_PRIORITY, &{##_DEVICE_LOWER_##}_api);
DT_INST_FOREACH_STATUS_OKAY({##_DEVICE_UPPER_##}_INIT)