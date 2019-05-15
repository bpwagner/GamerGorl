esptool.py --port /dev/cu.wchusbserial14610 erase_flash


esptool.py --port /dev/cu.wchusbserial14610 --baud 460800 write_flash --flash_size=detect 0 esp8266-20190301-v1.10-150-gf8f272429.bin


#esptool.py --port /dev/cu.wchusbserial14610 --baud 460800 write_flash --flash_size=detect 0 esp8266-20170108-v1.8.7.bin