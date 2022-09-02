import psycopg2
from datetime import datetime
import pandas as pd

from digi.xbee.devices import ZigBeeDevice
from digi.xbee.models.mode import APIOutputModeBit
from digi.xbee.util import utils

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM6"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600


def main():
    
    global df
    df = []
    print(" +--------------------------------------------------+")
    print(" | XBee Python Library Receive Explicit Data Sample |")
    print(" +--------------------------------------------------+\n")

    device = ZigBeeDevice(PORT, BAUD_RATE)
    try:
        device.open()

        device.set_api_output_mode_value(
            APIOutputModeBit.calculate_api_output_mode_value(
                device.get_protocol(), {APIOutputModeBit.EXPLICIT}))

        def explicit_data_callback(explicit_xbee_message):
            
            try:
                conn = psycopg2.connect(dbname="d1i6dvpph4obn9",
                        user="ktsrsbwiogtzmf",
                        password="eff425d775e4ed73b5a781df5fdfbb9a0b41f35307ee9da2b73376b324257741",
                        host="ec2-44-193-111-218.compute-1.amazonaws.com")


                curs = conn.cursor()
                if len(df) != 0:
                    
                    curs.executemany("INSERT INTO dados_datasensor (endereco, data, capacitancia) VALUES(%s,%s,%s)", df)
                    df.clear()
                    #df = []

               
                try:
                    curs.execute('INSERT INTO dados_datasensor (endereco, data, capacitancia) VALUES(%s, %s, %s)',
                             (str(explicit_xbee_message.remote_device.get_64bit_addr()),
                              datetime.fromtimestamp(int(explicit_xbee_message.timestamp)),
                              explicit_xbee_message.data.decode()[0:-2]))
                        
                    conn.commit()
                        
                except:
                    curs.execute('INSERT INTO dados_datasensor (endereco, data, capacitancia) VALUES(%s, %s, %s)',
                             (str(explicit_xbee_message.remote_device.get_64bit_addr()),
                              datetime.fromtimestamp(int(explicit_xbee_message.timestamp)),1))
                    
                    conn.commit()
            except (Exception, psycopg2.DatabaseError) as error: 
                print(error)
                try: 
		        
			c = [str(explicit_xbee_message.remote_device.get_64bit_addr()),
			         datetime.fromtimestamp(int(explicit_xbee_message.timestamp)),
			         explicit_xbee_message.data.decode()[0:-2]]
			df.append(c)
            	except:
            		pass	
                		
        device.flush_queues()
        device.add_expl_data_received_callback(explicit_data_callback)

        print("Waiting for data in explicit format...\n")

        while True:
            explicit_xbee_message = device.read_data()
            if explicit_xbee_message is not None:
                pass
            #input()
            
    except:
        print('porta usb desconectada')
        
    finally:
        if device is not None and device.is_open():
            device.close()
            #conn.close()

    

if __name__ == '__main__':
    main()
