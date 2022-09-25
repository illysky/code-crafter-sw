
from datetime import datetime
import re
import sys
import os
import math

# *******************************************************************
# * @brief: Gets a snippet of code from the main snippet file
# ********************************************************************
def _get_snippet (name):

    # Open Snippet File
    file = open(f"snips.txt", "r");
    d = file.read(); 

    # Create Pattern 
    p = f"{{@@_{name.upper()}_START_@@}}(.*?){{@@_{name.upper()}_END_@@}}"

    # Search for Snippet Markers
    result = re.search(p,d,re.DOTALL); 
    if result == None:
        print(f"Error: Header snippet \"{name.upper()}\" not found, please add to snip.data")
        exit()
    snippet = result.group(1).strip()
    file.close()
    return snippet

# *******************************************************************
# * @brief: Replaces text inside snippet
# ********************************************************************
def _replace_snippet (name, snippet, text): 
    pattern = f"{{$$_{name}_$$}}"
    snippet = snippet.replace(pattern,text)
    return snippet

# *******************************************************************
# * @func: 
# * @brief: 
# ********************************************************************
def _parse_address (addr, line):

    # Hex
    if "h" in addr:
        addr = addr.replace("h",""); 
    elif "H" in addr:
        addr = addr.replace("H","");   
    elif "0x" in addr:
        addr = addr.replace("0x","");   
    elif "0X" in addr:
        addr = addr.replace("0X","");  
    else:
        print(f"Error: Not a valid address format @ ln {line}")
        exit()

    # Work out the address width 
    width = math.ceil((len(addr) / 2))
    addr_int = int(addr, 16);

    # Upper case 
    addr = f"0x{addr_int:02X}"
    return (addr, width)

# *******************************************************************
# * @func: 
# * @brief: 
# ********************************************************************
def _create_block (driver, reg, addr, width, bitfields, write, read):
    
    block = {}
    block['function'] = ""
    block['prototype'] = ""
    block['typedef'] = ""


    reg_name = f"{driver.upper()}_{reg.upper()}"
    reg_size = f"{width}"
    reg_addr = f"{addr}"
    typedef_name = f"{driver.lower()}_{reg.lower()}_t"

    # Width 
    if width == 1: 
        word = "uint8_t val"
    elif width == 2:
        word = "uint16_t val"
    else:
        word = "uint32_t val"


    # Create bitfields for the struct
    structs = ""
    bitfields.reverse()
    stride = 1; 
    for bitfield in bitfields:

        span = bitfield[0] 
        name = bitfield[1] 

        span = span.split(":")

        if len(span) > 2: 
            print(f"Error: Invalid bitfield span")
            exit()
        
        if len(span) == 1:
            stride = 1; 

        if len(span) == 2:
            stride = (int(span[0]) - int(span[1])) + 1;

        structs += f"        unsigned {bitfield[1].lower()}:{stride};\n"


    # Create the typedef
    typedef = _get_snippet ("TYPEDEF")
    typedef = _replace_snippet ("REGADDR", typedef, f"{reg_name}_ADDR {reg_addr}")
    typedef = _replace_snippet ("REGSIZE",typedef, f"{reg_name}_SIZE {reg_size}")
    typedef = _replace_snippet ("WORD",typedef, word)
    typedef = _replace_snippet ("BITFIELDS",typedef,structs[:-1])
    typedef = _replace_snippet ("TYPEDEF",typedef,typedef_name)
    typedef += "\n\n"
    block['typedef'] = typedef; 

    # Create Function
    if read == True:
        function_read = _get_snippet ("CODE"); 
        function_read = _replace_snippet ("DRIVER", function_read, f"{driver.lower()}")
        function_read = _replace_snippet ("RW", function_read, "read")
        function_read = _replace_snippet ("OVERVIEW", function_read, f"Function to read from {reg_name.upper()} register")
        function_read = _replace_snippet ("REGNAME", function_read, f"{reg.lower()}")
        function_read = _replace_snippet ("TYPEDEF", function_read, f"{typedef_name.lower()}")
        function_read = _replace_snippet ("REGADDR", function_read, f"{reg_name}_ADDR")
        function_read = _replace_snippet ("REGSIZE", function_read, f"{reg_name}_SIZE")
        function_read += "\n\n"
        block['function'] += function_read; 
        block['prototype'] += function_read.split("*/\n")[1].splitlines()[0] + ";\n" # Parse end of comments, then take first line and add semicolon and new line

    if write == True:
        function_write = _get_snippet ("CODE"); 
        function_write = _replace_snippet ("DRIVER", function_write, f"{driver.lower()}")
        function_write = _replace_snippet ("RW", function_write, "write")
        function_write = _replace_snippet ("OVERVIEW", function_write, f"Function to write to {reg_name.upper()} register")
        function_write = _replace_snippet ("REGNAME", function_write, f"{reg.lower()}")
        function_write = _replace_snippet ("TYPEDEF", function_write, f"{typedef_name.lower()}")
        function_write = _replace_snippet ("REGADDR", function_write, f"{reg_name}_ADDR")
        function_write = _replace_snippet ("REGSIZE", function_write, f"{reg_name}_SIZE")
        function_write += "\n\n"
        block['function'] += function_write; 
        block['prototype'] += function_write.split("*/\n")[1].splitlines()[0] + ";\n" # Parse end of comments, then take first line and add semicolon and new line

    return block; 


if __name__ == "__main__":
  
    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    register = {}; 
    fields = []; 
    stage = 0;  
    reg_addr = ""
    reg_addr_width = 1
    reg_addr_width_max = 1
    
    reg_name = ""
    reg_rw = ""
    bitfields = []

    # This is where the snippets get stored
    typedefs = ""       # typedefs of the driver
    prototypes = ""     # prototypes of the driver 
    functions = ""      # functions of the driver
    stubs = ""          # stubs of code for the user to add to
    address_size = ""
    try: 
        driver_name = sys.argv[1]; 

    except:
        print("Error: Missing driver name")
        exit()

    try: 
        f = open(f"reg/{driver_name}.reg", "r")
    except:
        print(f"Error: Cannot find register layout file {driver_name}.reg")
        exit()



    lines = f.readlines()
    for index, line in enumerate(lines):

        # Stage 1: Get register address
        if stage == 0:
            stage = 1; 
            if line.isspace() == False:
                line = line.strip()
                addr = _parse_address (line, index+1)
                reg_addr = addr[0]          # Address
                reg_addr_width = addr[1]          # Address
                if addr[1] > reg_addr_width_max:   # Width of address 
                    reg_addr_width_max = addr[1]   # Log the highest width
            continue; 

        # Stage 2: Get Permissions
        if stage == 1:
            stage = 2; 
            if line.isspace() == False:
                line = line.strip()
                reg_rw = line.lower(); 
                continue; 
            else: 
                print(f"Error: Expected permissions at @ ln {index+1}")
                exit(); 
            

        # Stage 2: Get register name
        if stage == 2:
            stage = 3; 
            if line.isspace() == False:
                line = line.strip()
                reg_name = line.lower(); 
                continue; 
            else: 
                print(f"Error: Expected register name at @ ln {index+1}")
                exit(); 

        # Stage 3: Get fields
        if stage == 3:
            if line.isspace() == False:
                line = line.strip()
                field = line.split()
                if (len(field) < 2):
                    print(f"Error: Expected bit field and name @ ln {index+1}")
                    exit();  
                else:  
                    # TODO: Sense check bit field and name
                    bitfields.append((field[0].lower(), field[1].lower()))
                    continue
            else:
                if len(bitfields) == 0:
                    print(f"Error: Expected at least one field @ ln {index+1}")
                    exit();  
                else: 
                    read = False
                    write = False

                    if reg_rw == "rw":
                        read = True
                        write = True
                    elif reg_rw == "wo":
                        write = True                     
                    elif reg_rw == "ro":
                        read = True

                    block = _create_block (driver_name, reg_name, reg_addr, reg_addr_width, bitfields, write, read )
                    typedefs += block ['typedef']
                    functions += block['function']
                    prototypes += block['prototype']

                    reg_addr = ""
                    reg_addr_width = 1
                    reg_name = ""
                    reg_rw = ""
                    bitfields = []
                    stage = 0;      

    if reg_addr_width_max == 1:
        reg_address_variable = "uint8_t"
    elif reg_addr_width_max == 2:
        reg_address_variable = "uint16_t"
    else:
        reg_address_variable = "uint32_t"
    
    # Create Stubs
    stub = _get_snippet ("STUB"); 
    stub = _replace_snippet ("DRIVER", stub, f"{driver_name.lower()}")
    stub = _replace_snippet ("RW", stub, "write")
    stub = _replace_snippet ("OVERVIEW", stub, f"Stub to write to {driver_name.upper()}")
    stub = _replace_snippet ("REGADDRSIZE", stub, reg_address_variable)
    stub += "\n\n"
    functions+=stub; 
    prototypes += stub.split("*/\n")[1].splitlines()[0] + ";\n" # Parse end of comments, then take first line and add semicolon and new line

    # Create Stubs
    stub = _get_snippet ("STUB"); 
    stub = _replace_snippet ("DRIVER", stub, f"{driver_name.lower()}")
    stub = _replace_snippet ("RW", stub, "read")
    stub = _replace_snippet ("OVERVIEW", stub, f"Stub to read from {driver_name.upper()}")
    stub = _replace_snippet ("REGADDRSIZE", stub, reg_address_variable)
    stub += "\n\n"
    functions+=stub; 
    prototypes += stub.split("*/\n")[1].splitlines()[0] + ";\n" # Parse end of comments, then take first line and add semicolon and new line

    # Create Stubs
    stub = _get_snippet ("INIT"); 
    stub = _replace_snippet ("DRIVER", stub, f"{driver_name.lower()}")
    stub = _replace_snippet ("OVERVIEW", stub, f"Stub to initialise the {driver_name.upper()}")
    stub += "\n\n"
    functions+=stub; 
    prototypes += stub.split("*/\n")[1].splitlines()[0] + ";\n" # Parse end of comments, then take first line and add semicolon and new line

    # Create Header Files
    snippet = _get_snippet("HDR")
    snippet  = _replace_snippet("DRIVER_FILE", snippet, driver_name.lower())
    snippet  = _replace_snippet("DRIVER_DESC",snippet,  f"A driver file for {driver_name.upper()}")
    snippet  = _replace_snippet("DRIVER_DEF", snippet, driver_name.upper())
    snippet  = _replace_snippet("DATE", snippet, now)
    snippet  = _replace_snippet("TYPEDEFS", snippet, typedefs.strip())
    snippet  = _replace_snippet("PROTOTYPES", snippet, prototypes)
    if not os.path.exists(driver_name):
        os.mkdir(driver_name)
    file = open(f"{driver_name}/{driver_name}.h", "w"); 
    file.write(snippet)
    file.close()

    # Create C Files
    snippet = _get_snippet("C")
    snippet  = _replace_snippet("DRIVER_FILE", snippet, driver_name.lower())
    snippet  = _replace_snippet("DRIVER_DESC",snippet,  f"A driver file for {driver_name.upper()}")
    snippet  = _replace_snippet("DATE", snippet, now)
    snippet  = _replace_snippet("HEADER_FILE", snippet, f"{driver_name.lower()}")
    snippet  = _replace_snippet("FUNCTIONS", snippet, functions)
    if not os.path.exists(driver_name):
        os.mkdir(driver_name)
    file = open(f"{driver_name}/{driver_name}.c", "w"); 
    file.write(snippet)
    file.close()


