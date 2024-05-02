#include "bq25792.h"
#include "hal.h"

// Define the hal structure for the bq device
hal_i2c_t i2c_for_bq25_0 = 
{
    .write = a_function_to_write_i2c, 
    .read = a_function_to_read_i2c, 
    .addr = 0x03, 
}

// You may have two!!
hal_i2c_t i2c_for_bq25_1 = 
{
    .write = a_function_to_write_i2c, 
    .read = a_function_to_read_i2c, 
    .addr = 0x04, 
}

void main (void) 
{

    // Lets read this register: 
    bq25792_minimal_system_voltage_t voltage; 
    bq25792_minimal_system_voltage_read(&i2c_for_bq25, &voltage); 


    // Lets write a bit in this this register to enable charge 
    // Remember to read/modify/write if you want to keep the other values
    bq25792_charger_control_0_t charge_ctrl;
    bq25792_charger_control_0_read(&i2c_for_bq25, &charge_ctrl);  
    charge_ctrl.EN_CHG = 1; 
    bq25792_charger_control_0_write(&i2c_for_bq25, &charge_ctrl);  

}