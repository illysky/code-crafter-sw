from datetime import datetime
import yaml
import re
import os
import sys


ascii_logo = \
'''
 ____   ____  _______     _________ _____            _  __
|  _ \ / __ \|  __ \ \   / /__   __|  __ \     /\   | |/ /
| |_) | |  | | |  | \ \_/ /   | |  | |__) |   /  \  | ' / 
|  _ <| |  | | |  | |\   /    | |  |  _  /   / /\ \ |  <  
| |_) | |__| | |__| | | |     | |  | | \ \  / ____ \| . \ 
|____/ \____/|_____/  |_|     |_|  |_|  \_\/_/    \_\_|\_\ 
'''

##################################################################
frag_func_zephyr = \
''' 
// ##################################################################
// {##_FUNC_##}_{##_WR_##}
// ##################################################################
int32_t {##_FUNC_##}_{##_WR_##}(const struct device *dev, {##_TYPE_##} *buf)
{
    const struct {##_DEVICE_##}_config *cfg = dev->config;
    return i2c_burst_{##_WR_##}_dt(&cfg->i2c, {##_ADDR_##}, (uint8_t*)&buf->val, {##_SIZE_##}); 
}
'''

##################################################################
frag_func_hal = \
''' 
// ##################################################################
// {##_FUNC_##}_{##_WR_##}
// ##################################################################
int32_t {##_FUNC_##}_{##_WR_##}(hal_i2c_t *i2c,{##_TYPE_##} *buf)
{
    return i2c->read(i2c->dev_addr, (uint8_t*)&buf->val, {##_SIZE_##}); 
}
'''

##################################################################
frag_typedef = \
'''
#define {##_REGADDR_##}
#define {##_REGSIZE_##}
typedef union
{
    {##_VALUE_##} val;
    struct
    {
{##_BITFIELDS_##}
    }; 
} __attribute__((packed)) {##_TYPEDEF_##};
'''

##################################################################
frag_cmakelist = \
'''
if (CONFIG_{##_DEVICE_UPPER_##})
    zephyr_library()
    zephyr_include_directories(.)
    zephyr_library_sources({##_DEVICE_LOWER_##}.c)
endif()
'''

##################################################################
frag_kconfig = \
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

##################################################################
frag_module = \
'''
name: {##_DEVICE_##}

build:
  cmake: .
  kconfig: Kconfig

  settings:
    dts_root: .
'''

##################################################################
frag_dts = \
'''  
description: {##_DESC_##}
compatible: "{##_MANU_##},{##_DEVICE_##}"
# Add properties includes manually
include: [{##_BUS_##}-device.yaml]
# Add properties manually
properties:
'''

##################################################################
def get_api (name):
##################################################################

    # Open Snippet File
    with open("tmpl_zephyr_api.c", "r") as f:
        d = f.read(); 
        p = f"{{@@_{name.upper()}_START_@@}}(.*?){{@@_{name.upper()}_END_@@}}"
        result = re.search(p,d,re.DOTALL); 
        if result == None:
            print(f"Error: API \"{name.upper()}\" not found, please add manually")
            return None
        return result.group(1).strip()

##################################################################
def replace (marker, snip, str):
##################################################################
    return snip.replace(f"{{##_{marker}_##}}",str)

##################################################################
if __name__ == "__main__":
##################################################################
    
    print("###########################################")
    print("# Code Crafter v2.0.0")
    print("###########################################")


    if len(sys.argv) > 1:
        # The first argument (sys.argv[0]) is the script name itself
        # The actual arguments start from sys.argv[1]
        filename = sys.argv[1]
        print(f"Generating source code for {filename}")
    else:
        print(f"Error: no device yaml has been provided")
        exit(1)

    # Open the YAML file
    with open(filename, "r") as file_yaml:
        device = yaml.safe_load(file_yaml)
        
        ############################################################
        # Iterate Registers
        ############################################################
        typedefs = ""
        z_funcs = ""
        z_protos = ""
        h_funcs = ""
        h_protos = ""

        
        for r in device['registers']:
            print(f"Register {r['address']:02X}")
            
            ################################################
            # Names
            ################################################
            reg_name = f"{device['device'].upper()}_{r['name'].replace(' ', '_').upper()}"
            reg_addr = f"{reg_name}_ADDR 0x{r['address']:02X}"
            reg_typedef = f"{reg_name.lower()}_t"
 
            ################################################
            # Typedefs
            ################################################
            bits = 0; 
            bitfields = ""
            for b in r['bitfield']:
                field_name, bit_position = b.split(':')
                field_name = field_name.replace(" ", "_").upper()
                bits+=int(bit_position); 
                if field_name == "RESERVED":
                    field_name = ""
                bitfields+=f"\t\tunsigned {field_name}: {bit_position};\n"
            
            # Check for 8 bit alignment
            if (bits % 8 != 0):
                print(f"Error: not 8 bit aligned: {reg_name}")
                exit(1)

            # Get the reg size
            reg_size = f"{reg_name}_SIZE {int(bits/8)}"
            reg_size_def = f"{reg_name}_SIZE"


            ################################################
            # Construct Typedef
            ################################################
            t = frag_typedef
            t = replace("REGADDR", t, reg_addr)
            t = replace("TYPEDEF", t, reg_typedef)
            t = replace("BITFIELDS", t, bitfields.rstrip())
            t = replace("REGSIZE", t, reg_size)
            t = replace("VALUE", t, f"uint{bits}_t")
            typedefs+= t


            ################################################
            # Construct Function and Prototype (Zephyr)
            ################################################
            func = frag_func_zephyr
            func = replace("FUNC", func, reg_name.lower())
            func = replace("WR", func, "read")
            func = replace("TYPE", func, reg_typedef)
            func = replace("DEVICE", func, device['device'].lower())
            func = replace("SIZE", func, reg_size_def)
            func = replace("ADDR", func, f"{reg_name}_ADDR")

            z_funcs +=  func
            z_protos+=  func.split("\n")[4].strip() +";\n"

            if (r['write'] == True): 
                func = frag_func_zephyr
                func = replace("FUNC", func, reg_name.lower())
                func = replace("WR", func, "write");
                func = replace("TYPE", func, reg_typedef);
                func = replace("DEVICE", func, device['device'].lower())
                func = replace("SIZE", func, reg_size_def);
                func = replace("ADDR", func, f"{reg_name}_ADDR");
                z_funcs +=  func
                z_protos+=  func.split("\n")[4].strip() +";\n"


            ################################################
            # Construct Function and Prototype (Hal)
            ################################################
            func = frag_func_hal
            func = replace("FUNC", func, reg_name.lower())
            func = replace("WR", func, "read");
            func = replace("TYPE", func, reg_typedef);
            func = replace("SIZE", func, reg_size_def);
            h_funcs +=  func
            h_protos+=  func.split("\n")[4].strip() +";\n"

            if (r['write'] == True):    
                func = frag_func_hal
                func = replace("FUNC", func, reg_name.lower())
                func = replace("WR", func, "write");
                func = replace("TYPE", func, reg_typedef);
                func = replace("SIZE", func, reg_size_def);
                h_funcs +=  func
                h_protos+=  func.split("\n")[4].strip() +";\n"


        ############################################################
        #  Zephyr Generation
        ############################################################ 
        root = f"{device['device']}".lower()
        os.makedirs(f"{root}/zephyr/{root}", exist_ok=True); 
        os.makedirs(f"{root}/zephyr/{root}/dts/bindings", exist_ok=True); 
        os.makedirs(f"{root}/zephyr/{root}/zephyr", exist_ok=True); 

        ############################################################
        #  Header
        ############################################################ 
        with open("tmpl_zephyr.h", "r") as f:
            header = f.read(); 
    
        header = replace("LOGO", header, ascii_logo.strip())
        header = replace("DESCRIPTION", header, f"Driver for {device['manufacturer']} {device['device']}")
        header = replace("COPYRIGHT", header, device['copyright'])
        header = replace("VERSION", header, device['version'])
        header = replace("DEVICE", header, f"{device['device']}".lower())
        header = replace("TYPEDEFS", header, typedefs)
        header = replace("BUS", header, device['bus'].lower())

        with open(f"{root}/zephyr/{root}/{root}.h", "w") as f:
            f.write(header)

        #############################################################
        # Source 
        #############################################################
        with open("tmpl_zephyr.c", "r") as f:
            source = f.read(); 
        source = replace("LOGO", source, ascii_logo.strip())
        source = replace("DESCRIPTION", source, f"Driver for {device['manufacturer']} {device['device']}")
        source = replace("COPYRIGHT", source, device['copyright'])
        source = replace("VERSION", source, device['version'])
        source = replace("MANU", source, f"{device['manufacturer']}".lower())
        source = replace("DEVICE_UPPER", source, f"{device['device']}".upper())
        source = replace("DEVICE_LOWER", source, f"{device['device']}".lower())
        source = replace("FUNCTIONS", source, z_funcs)
        source = replace("API_UPPER", source, device['api'].upper())
        source = replace("API_L", source, device['api'].lower())
        source = replace("BUS", source, device['bus'].lower())
        with open(f"{root}/zephyr/{root}/{root}.c", "w") as f:
            f.write(source)


        #############################################################
        # CMakeList 
        #############################################################
        # TODO:
        cmakelist = frag_cmakelist
        cmakelist = replace("DEVICE_UPPER", cmakelist, device['device'].upper())
        cmakelist = replace("DEVICE_LOWER", cmakelist, device['device'].lower())
        with open(f"{root}/zephyr/{root}/CMakeLists.txt", "w") as f:
            f.write(cmakelist)

        #############################################################
        # KConfig 
        #############################################################
        kconfig = frag_kconfig
        kconfig = replace("DEVICE_UPPER", kconfig, device['device'].upper())
        kconfig = replace("DESC", kconfig, device['device'].lower())
        kconfig = replace("BUS", kconfig, device['bus'].upper())
        kconfig = replace("API_UPPER", kconfig, device['api'].upper())
        kconfig = replace("MANU", kconfig, device['manufacturer'].upper())
        with open(f"{root}/zephyr/{root}/Kconfig", "w") as f:
            f.write(kconfig)

        #############################################################
        # DTS 
        #############################################################
        dts = frag_dts
        dts = replace("MANU", dts, device['manufacturer'].lower())    
        dts = replace("DEVICE", dts, device['device'].lower())  
        dts = replace("BUS", dts, device['bus'].lower())  
        dts = replace("DESC", dts, f"Driver for {device['manufacturer']} {device['device'].lower()}")  
        with open(f"{root}/zephyr/{root}/dts/bindings/{device['manufacturer'].lower()},{device['device'].lower()}.yaml", "w") as f:
            f.write(dts.strip())

        #############################################################
        # Module 
        #############################################################
        module = frag_module
        module = replace("DEVICE", module, device['device'].lower()) 
        with open(f"{root}/zephyr/{root}/zephyr/module.yaml", "w") as f:
            f.write(module.strip())

        ############################################################
        #  HAL Generation
        ############################################################ 
        root = f"{device['device']}".lower()
        os.makedirs(f"{root}/hal/{root}/", exist_ok=True); 
        
        ############################################################
        #  Header
        ############################################################ 
        with open("tmpl_hal.h", "r") as f:
            header = f.read(); 
        header = replace("LOGO", header, ascii_logo.strip())
        header = replace("DESCRIPTION", header, f"Driver for {device['manufacturer']} {device['device']}")
        header = replace("COPYRIGHT", header, device['copyright'])
        header = replace("VERSION", header, device['version'])
        header = replace("DEVICE", header, f"{device['device']}".lower())
        header = replace("TYPEDEFS", header, typedefs.strip())
        header = replace("PROTOTYPES", header, h_protos)
        header = replace("MANU", header, device['manufacturer'].upper())
        header = replace("DEVICE_U", header, device['device'].upper())
        with open(f"{root}/hal/{root}/{root}.h", "w") as f:
            f.write(header)

        ############################################################
        #  Header
        ############################################################ 
        with open("tmpl_hal.c", "r") as f:
            source = f.read(); 
        source = replace("LOGO", source, ascii_logo.strip())
        source = replace("DESCRIPTION", source, f"Driver for {device['manufacturer']} {device['device']}")
        source = replace("COPYRIGHT", source, device['copyright'])
        source = replace("VERSION", source, device['version'])
        source = replace("DEVICE", source, f"{device['device']}".lower())
        source = replace("FUNCTIONS", source, h_funcs.strip())
        with open(f"{root}/hal/{root}/{root}.c", "w") as f:
            f.write(source)
    
        print(f"Complete")