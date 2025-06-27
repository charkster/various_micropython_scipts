import pyb
USB_VCP = pyb.USB_VCP

class USBTMCDevice:
    def __init__(self):
        self.usb = USB_VCP()
    
    def wait_for_command(self):
        while not self.usb.any():
            time.sleep(0.1)
        return self.usb.read(64) # Read up to 64 bytes (adjust as needed).
    
    def send_response(self, response):
        self.usb.write(response)

def main():
    usb_tmc = USBTMCDevice()

    while True:
        data = usb_tmc.wait_for_command()
        if data:
            command = data.decode('utf-8').strip()
            
            if command.upper() == "*IDN?":
                response_text = "MicropythonDevice, Model X, Serial: 12345, Version: 1.0\n"
            else:
                response_text = "Error: Command not recognized\n"
                
            usb_tmc.send_response(response_text.encode('utf-8'))

if __name__ == "__main__":
    main()
