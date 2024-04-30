from datetime import datetime
import yaml
import re


##################################################################
snippet_typedef = \
'''
#define {$$_REGADDR_$$}
#define {$$_REGSIZE_$$}
typedef union
{
    {$$_VALUE_$$};
    struct
    {
{$$_BITFIELDS_$$}
    }; 
} __attribute__((packed)) {$$_TYPEDEF_$$};

'''
##################################################################
#
##################################################################
snippet_h_file = \
'''
 /* 
 ____  __    __   _  _  ___  _  _  _  _ 
(_  _)(  )  (  ) ( \/ )/ __)( )/ )( \/ )
 _)(_  )(__  )(__ \  / \__ \ )  (  \  / 
(____)(____)(____)(__) (___/(_)\_) (__) 

 {$$_DESCRIPTION_$$}
 {$$_VERSION_$$}
 {$$_COPYRIGHT_$$}
 */  

#ifndef __{$$_DRIVER_$$}_H
#define __{$$_DRIVER_$$}_H

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

{$$_TYPEDEFS_$$}

#ifdef __cplusplus
}
#endif
#endif // {$$_DRIVER_$$}_H
'''
##################################################################
def replace (marker, snip, str):
##################################################################
    return snip.replace(f"{{$$_{marker}_$$}}",str)


##################################################################
if __name__ == "__main__":
##################################################################
    
    # Open the YAML file
    with open("test.yaml", "r") as f:
        device = yaml.safe_load(f)
        typedefs = ""
        
        #  Construct all the typedefs
        for r in device['registers']:
            t = snippet_typedef
            name = f" {device['device'].upper()}_{r['name'].replace(' ', '_').upper()}"
            t = replace("REGADDR", t, f"{name}_ADDR 0x{r['address']:02X}" )
            t = replace("TYPEDEF", t, f"{name.lower()}_t" )
            
            bits = 0; 
            bitfields = ""
            for b in r['bitfield']:
                field_name, bit_position = b.split(':')
                bits+=int(bit_position); 
                bitfields+=f"\t\tunsigned {field_name}: {bit_position};\n"
            
            if (bits % 8 != 0):
                print("not 8 bit aligned ")
                exit(1)
            
            t = replace("BITFIELDS", t, bitfields.rstrip())
            t = replace("REGSIZE", t, f"{name}_SIZE { int(bits/8)}" )
            t = replace("VALUE", t, f"uint{bits}_t v" )
            typedefs+= t

        # Construct the header file         
        h = snippet_h_file
        h = replace("DESCRIPTION", h, f"Driver header file for {device['manufacturer']} {device['device']}")
        h = replace("COPYRIGHT", h, device['copyright'])
        h = replace("VERSION", h, device['version'])
        h = replace("DRIVER", h, f"{device['manufacturer']}_{device['device']}".upper())
        h = replace("TYPEDEFS", h, typedefs)



        with open(f"{device['manufacturer']}_{device['device']}.h".lower(), 'w') as header:
            header.write(h)



