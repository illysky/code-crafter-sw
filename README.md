# Code Crafter
An tool for the automated generation of code to read and write registers of ICs. This tool will generate source code for Hal and Zephyr.  

Follow these steps to define device registers, configure a YAML file, and run a script to generate driver versions for Zephyr and HAL:

1. **Define the Device Registers in YAML:**
   - Create a YAML file according to the attached example to define device registers.
   - Use the `example.yaml` as reference. 
   - Name the file to the part number of the device.

2. **Place the YAML File in the Script Directory:**
   - Ensure that the YAML file is placed in the same directory as the script.

3. **Run the Python Script:**
   - Execute the script by running the following command in your terminal:
     ```
     python3 app.py xxxx.yaml
     ```
   - Replacing  `xxxx.yaml` with the name of your device YAML file.

4. **Check the Output Folder:**
   - After running the script, a folder with the same name as your YAML file will be created.
   - Inside this folder, you will find two versions of the driver:
     - `zephyr`: For Zephyr operating systems (Zephyr)
     - `hal`: For hardware abstraction layers (Ganymede)



# HAL Driver (for Ganymede)
This version is simple driver for our current Ganymede firmware. It is basically a .c/.h pair that has all the functions and typedefs to read any register of the device defined in the YAML. It depends on a module called hal.h, which defines the i2c and addr that the device is using. But as an example:
```
#include "bq25792.h"
#include "hal.h"

// ##################################################################
// Define the hal structure for the BQ device
// ##################################################################
hal_i2c_t i2c_for_bq25_0 = 
{
    .write = a_function_to_write_i2c,  // <-- write function, see typedef for prototype
    .read = a_function_to_read_i2c,    // <-- write function, see typedef for prototype
    .addr = 0x03                       // <-- device address
}

// ##################################################################
// You may have two devices! 
// ##################################################################
hal_i2c_t i2c_for_bq25_1 = 
{
    .write = a_function_to_write_i2c, 
    .read = a_function_to_read_i2c, 
    .addr = 0x04, 
}

// ##################################################################
// Main function
// ##################################################################
void main (void) 
{
    // Lets read this register: 
    bq25792_minimal_system_voltage_t voltage; 
    bq25792_minimal_system_voltage_read(&i2c_for_bq25, &voltage); 

    // Lets write a bit in this this register to enable charge 
    // Remember to read/modify/write if you want 
    // to keep the other values that are in the register

    bq25792_charger_control_0_t charge_ctrl;
    bq25792_charger_control_0_read(&i2c_for_bq25, &charge_ctrl);  
    charge_ctrl.EN_CHG = 1; 
    bq25792_charger_control_0_write(&i2c_for_bq25, &charge_ctrl);
    
    // Enable the other device
    bq25792_charger_control_0_t charge_ctrl;
    bq25792_charger_control_0_read(&i2c_for_bq25_1, &charge_ctrl);  
    charge_ctrl.EN_CHG = 1; 
    bq25792_charger_control_0_write(&i2c_for_bq25_1, &charge_ctrl);

}
```