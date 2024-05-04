import yaml
import sys
import os
from art import *
import argparse
from datetime import datetime
import re

macro = \
''''
#define BITS_PER_LONG   (__CHAR_BIT__ * __SIZEOF_LONG__)
#define LSB_GET	(value)	   ((value) & -(value))
#define FIELD_GET(mask,value ) (((value) & (mask)) / LSB_GET(mask))
#define FIELD_PREP( mask, value )(((value) * LSB_GET(mask)) & (mask))
#define GENMASK	(h,l ) (((~0UL) - (1UL << (l)) + 1) & (~0UL >> (BITS_PER_LONG - 1 - (h))))
'''
cmakefile = \
'''
if (CONFIG_{##_DEVICE_UPPER_##})
    zephyr_library()
    zephyr_include_directories(.)
    zephyr_library_sources({##_DEVICE_LOWER_##}.c)
endif()
'''
kconfig = \
'''  
config {##_DEVICE_UPPER_##}
	bool "{##_DESC_##}"
	default n
	depends on DT_HAS_{##_MANU_##}_{##_DEVICE_UPPER_##}_ENABLED
	select {##_BUS_##}
	select {##_API_UPPER_##}
	help
	  Enable {##_DEVICE_UPPER_##} {##_API_UPPER_##} driver.
'''

module = \
'''
name: {##_DEVICE_##}

build:
  cmake: .
  kconfig: Kconfig

  settings:
    dts_root: .
'''

##################################################################
dts = \
'''  
description: {##_DESC_##}
compatible: "{##_MANU_##},{##_DEVICE_##}"
# Add properties includes manually
include: [{##_BUS_##}-device.yaml]
# Add properties manually
# properties:
'''
##################################################################
def replace (marker, snip, str):
##################################################################
    return snip.replace(f"{{##_{marker.upper()}_##}}",str)

##################################################################
def generate_zephyr (owner, device, macro):
##################################################################
    
    name = device['device'].lower()
    logo = text2art(owner)
    copyright = f"Copyright \u00A9 {datetime.now().year} {owner}"

    
    os.makedirs(f"{name}/zephyr/{name}", exist_ok=True); 
    os.makedirs(f"{name}/zephyr/{name}/dts/bindings", exist_ok=True); 
    os.makedirs(f"{name}/zephyr/{name}/zephyr", exist_ok=True); 


    with open("zephyr.yaml", 'r') as f:
        apis = yaml.safe_load(f)

    # Generate API calls
    api = apis[device['api']]

    # Include Files
    api_includes = ""
    for i in api['includes']:
        api_includes+=i + '\n'; 
    api_includes+=f"#include <zephyr/drivers/{device['bus']}.h>\n"

    # Functions 
    api_functions = ""
    api_pointers = ""
    for f in api['functions']:
        api_functions+= f'// ##################################################################\n'
        api_functions+= f'// {f}\n'
        api_functions+= f'// ##################################################################\n'
        api_functions+= f"{f}\n{{\n\treturn 0;\n}}\n\n"
        r = re.findall(r'\b\w+\b(?=\s*\()', f)[0]
        api_pointers+= f"\t.{r} = {r},\n"
    
    api_pointers = api_pointers.rstrip()[:-1]
    api_functions = api_functions.rstrip()

    #############################################################
    # Source 
    #############################################################
    with open("tmpl_zephyr.c", "r") as f:
        buf = f.read(); 
    buf = replace("LOGO", buf, logo.rstrip())
    buf = replace("DESCRIPTION", buf, f"Driver for {device['manufacturer']} {device['device']}")
    buf = replace("COPYRIGHT", buf, copyright)
    buf = replace("AUTHOR", buf, "by Code Crafter")
    buf = replace("VERSION", buf, device['version'])
    buf = replace("MANU", buf, f"{device['manufacturer']}".lower())
    buf = replace("DEVICE_UPPER", buf, f"{device['device']}".upper())
    buf = replace("DEVICE_LOWER", buf, f"{device['device']}".lower())
    buf = replace("API_UPPER", buf, device['api'].upper())
    buf = replace("API_L", buf, api['name'].lower())
    buf = replace("api_pointers", buf, api_pointers)
    buf = replace("api_functions", buf, api_functions)
    buf = replace("api_includes", buf, api_includes.rstrip())


    buf = replace("BUS", buf, device['bus'].lower())
    with open(f"{name}/zephyr/{name}/{name}.c", "w") as f:
        f.write(buf)

    ############################################################
    # Header
    ############################################################ 
    with open("tmpl_zephyr.h", "r") as f:
        buf = f.read(); 
    buf = replace("LOGO", buf, logo.rstrip())
    buf = replace("DESCRIPTION", buf, f"Driver for {device['manufacturer']} {device['device']}")
    buf = replace("COPYRIGHT", buf, copyright)
    buf = replace("AUTHOR", buf, "by Code Crafter")
    buf = replace("VERSION", buf, device['version'])
    buf = replace("DEVICE", buf, f"{device['device']}".lower())
    buf = replace("MACROS", buf, macro)
    buf = replace("BUS", buf, device['bus'].lower())

    with open(f"{name}/zephyr/{name}/{name}.h", "w") as f:
        f.write(buf)

    #############################################################
    # CMakeList 
    #############################################################
    buf = cmakefile
    buf = replace("DEVICE_UPPER", buf, device['device'].upper())
    buf = replace("DEVICE_LOWER", buf, device['device'].lower())
    with open(f"{name}/zephyr/{name}/CMakeLists.txt", "w") as f:
        f.write(buf)

    #############################################################
    # KConfig 
    #############################################################
    buf = kconfig
    buf = replace("DEVICE_UPPER", buf, device['device'].upper())
    buf = replace("DESC", buf, device['device'].lower())
    buf = replace("BUS", buf, device['bus'].upper())
    buf = replace("API_UPPER", buf, device['api'].upper())
    buf = replace("MANU", buf, device['manufacturer'].upper())
    with open(f"{name}/zephyr/{name}/Kconfig", "w") as f:
        f.write(buf.strip())

    #############################################################
    # DTS 
    #############################################################
    buf = dts
    buf = replace("MANU", buf, device['manufacturer'].lower())    
    buf = replace("DEVICE", buf, device['device'].lower())  
    buf = replace("BUS", buf, device['bus'].lower())  
    buf = replace("DESC", buf, f"Driver for {device['manufacturer']} {device['device'].lower()}")  
    with open(f"{name}/zephyr/{name}/dts/bindings/{device['manufacturer'].lower()},{device['device'].lower()}.yaml", "w") as f:
        f.write(buf.strip())

    #############################################################
    # Module 
    #############################################################
    buf = module
    buf = replace("DEVICE", buf, device['device'].lower()) 
    with open(f"{name}/zephyr/{name}/zephyr/module.yaml", "w") as f:
        f.write(buf.strip())

if __name__ == "__main__":

    print("###########################################")
    print("# Code Crafter v2.0.0")
    print("###########################################")

    parser = argparse.ArgumentParser(description="Creates driver source code for devices ")
    parser.add_argument("filename", help="Name of the file to process")
    parser.add_argument("-o", "--owner", help="Optional banner string")
    args = parser.parse_args()




    with open(args.filename, 'r') as f:
        device = yaml.safe_load(f)
        d_name = device['device'].replace(' ', '_').upper()

        # Generate macros for each register 
        out = ""
        for register in device['registers']:

            defines = ""; 
            r_name = register['name'].replace(' ', '_').upper()
            r_addr = register['address']
            bitfields = register['bitfield']; 

            bit = 0; 
            for b in range(len(bitfields) - 1, -1, -1):
                fname, span = bitfields[b].split(':')
                span = int(span)
                if fname.upper() != "RESERVED":
                    defines += f"#define {d_name}_{r_name}_{fname}_GET(val) FIELD_GET(GENMASK({(bit+span)-1 },{bit}),val)\n"
                    defines += f"#define {d_name}_{r_name}_{fname}_SET(val) FIELD_PREP(GENMASK({(bit+span)-1 },{bit}),val)\n"
                bit+=span; 
            
            out += f"// {d_name}_{r_name}\n"
            out += f"#define {d_name}_{r_name}_ADDR 0x{r_addr:02X}\n"
            out += f"#define {d_name}_{r_name}_SIZE {int(bit/8)}\n"
            out += defines; 
            out += "\n"; 
        

        generate_zephyr(args.owner,device,out); 

