import machine

class APDS9960:

    def __init__(self, i2c, slave_id=0x39, debug=False):
        self.slave_id  = slave_id
        self.bus       = i2c
        self.debug     = debug

    class bitfield_type:
        def __init__(self, NAME       = "",
                           ADDRESS    = 0x00,
                           RST_VAL    = 0x00,
                           WIDTH      = 0,
                           OFFSET     = 0,
                           ACCESS     = "",
                           TABLE_ENUM = {},
                           OTHER      = "" ):

            self.NAME        = NAME
            self.ADDRESS     = ADDRESS
            self.RST_VAL     = RST_VAL
            self.WIDTH       = WIDTH
            self.OFFSET      = OFFSET
            self.ACCESS      = ACCESS
            self.TABLE_ENUM  = TABLE_ENUM
            self.OTHER       = OTHER
            self.BIT_MASK    = int(2 ** self.WIDTH - 1) << self.OFFSET

    ######################################
    # ENABLE REGISTER 0x80
    ######################################

    # POWER ON (needed for all functions), low 
    BF_PON     = bitfield_type (
    NAME       = "PON",
    ADDRESS    = 0x80,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { "CHIP_OFF" : 0, "CHIP_ON" : 1 } )

    # Ambient Light Sensor (ALS) enable
    BF_AEN     = bitfield_type (
    NAME       = "AEN",
    ADDRESS    = 0x80,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 1,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )

    # Proximity detect enable
    BF_PEN     = bitfield_type (
    NAME       = "PEN",
    ADDRESS    = 0x80,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 2,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )

    #Wait timer enable
    BF_WEN     = bitfield_type (
    NAME       = "WEN",
    ADDRESS    = 0x80,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 3,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )
    
    # ALS Interrupt enable
    BF_AIEN    = bitfield_type (
    NAME       = "AIEN",
    ADDRESS    = 0x80,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 4,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )
    
    # Proximity Interrupt enable
    BF_PIEN    = bitfield_type (
    NAME       = "PIEN",
    ADDRESS    = 0x80,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 5,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )

    # Gesture enable
    BF_GEN     = bitfield_type (
    NAME       = "GEN",
    ADDRESS    = 0x80,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 6,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )

    ######################################
    # ATIME REGISTER 0x81
    ######################################

    # ADC integration time, time = (256 - value) * 2.78ms, value of 0xFF is 2.78ms, value of 0x00 is 712ms
    BF_ATIME   = bitfield_type (
    NAME       = "ATIME",
    ADDRESS    = 0x81,
    RST_VAL    = 0xFF,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } )

    ######################################
    # WTIME REGISTER 0x83
    ######################################
    
    # WTIME defines the low power mode time between Proximity and ALS cycles, time = (256 - value) * 2.78ms
    BF_WTIME   = bitfield_type (
    NAME       = "WTIME",
    ADDRESS    = 0x83,
    RST_VAL    = 0xFF,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } )

    ######################################
    # ALS THRESHOLD REGISTER 0x84
    ######################################

    # ALS Low byte of low interrupt threshold
    BF_AILTL   = bitfield_type (
    NAME       = "AILTL",
    ADDRESS    = 0x84,
    RST_VAL    = 0x0A,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = {  } )

    ######################################
    # ALS THRESHOLD REGISTER 0x85
    ######################################

    # ALS high byte of low interrupt threshold
    BF_AILTH   = bitfield_type (
    NAME       = "AILTH",
    ADDRESS    = 0x85,
    RST_VAL    = 0x03,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = {  } )

    ######################################
    # ALS THRESHOLD REGISTER 0x86
    ######################################

    # ALS Low byte of high interrupt threshold
    BF_AIHTL   = bitfield_type (
    NAME       = "AIHTL",
    ADDRESS    = 0x86,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = {  } )

    ######################################
    # ALS THRESHOLD REGISTER 0x87
    ######################################

    # ALS high byte of high interrupt threshold
    BF_AIHTH   = bitfield_type (
    NAME       = "AIHTH",
    ADDRESS    = 0x87,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = {  } )

    ######################################
    # PROXIMITY THRESHOLD REGISTER 0x89
    ######################################

    # PROX low byte of interrupt threshold
    BF_PILT    = bitfield_type (
    NAME       = "PILT",
    ADDRESS    = 0x89,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } )

    ######################################
    # PROXIMITY THRESHOLD REGISTER 0x8B
    ######################################

    # PROX low byte of interrupt threshold
    BF_PIHT    = bitfield_type (
    NAME       = "PIHT",
    ADDRESS    = 0x8B,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } )

    ######################################
    # PERSISTANCE REGISTER 0x8C
    ######################################

    # Proximity Interrupt Persistence. Controls rate of proximity interrupt to the host processor
    # value is consecutive cycles out of range
    BF_PPERS   = bitfield_type (
    NAME       = "PPERS",
    ADDRESS    = 0x8C,
    RST_VAL    = 0x00,
    WIDTH      = 4,
    OFFSET     = 4,
    ACCESS     = "RW",
    TABLE_ENUM = { "EVERY_CYCLE" : 0 } )

    # ALS Interrupt Persistence. Controls rate of Clear channel interrupt to the host processor
    # value is multiplied by 5 of consecutive cycles, value of 4 is 20 cycles, 15 is 60 consecutive cycles
    BF_APERS   = bitfield_type (
    NAME       = "APERS",
    ADDRESS    = 0x8C,
    RST_VAL    = 0x00,
    WIDTH      = 4,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { "EVERY_CYCLE" : 0, "ANY_OUTSIDE" : 1, "2_OUTSIDE" : 2, "3_OUTSIDE" : 3 } )

    ######################################
    # CONFIG ONE REGISTER 0x8D
    ######################################

    # When asserted, the wait cycle is increased by a factor 12x from that programmed in the WTIME register
    BF_WLONG   = bitfield_type (
    NAME       = "WLONG",
    ADDRESS    = 0x8D,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 1,
    ACCESS     = "RW",
    TABLE_ENUM = { "NORMAL_WTIME" : 0, "12X_WTIME" : 1 } )

    ######################################
    # PROXIMITY PULSE COUNT REGISTER 0x8E
    ######################################

    # Proximity Pulse Length. Sets the LED-ON pulse width during a proximity LDR pulse.
    BF_PPLEN   = bitfield_type (
    NAME       = "PPLEN",
    ADDRESS    = 0x8E,
    RST_VAL    = 0x01,
    WIDTH      = 2,
    OFFSET     = 6,
    ACCESS     = "RW",
    TABLE_ENUM = { "4US" : 0, "8US" : 1, "16US" : 2, "32US" : 3 } )

    # Proximity Pulse Count. Specifies the number of proximity pulses to be generated on LDR. Number of pulses is set by PPULSE value plus 1.
    BF_PPULSE  = bitfield_type (
    NAME       = "PPULSE",
    ADDRESS    = 0x8E,
    RST_VAL    = 0x00,
    WIDTH      = 6,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } )

    ######################################
    # CONTROL ONE REGISTER 0x8F
    ######################################

    # LED Drive Strength. 
    BF_LDRIVE  = bitfield_type (
    NAME       = "LDRIVE",
    ADDRESS    = 0x8F,
    RST_VAL    = 0x00,
    WIDTH      = 2,
    OFFSET     = 6,
    ACCESS     = "RW",
    TABLE_ENUM = { "100MA" : 0, "50MA" : 1, "25MA" : 2, "12MA" : 3 } )
    
    # Proximity Gain Control
    BF_PGAIN   = bitfield_type (
    NAME       = "PGAIN",
    ADDRESS    = 0x8F,
    RST_VAL    = 0x00,
    WIDTH      = 2,
    OFFSET     = 2,
    ACCESS     = "RW",
    TABLE_ENUM = { "1X" : 0, "2X" : 1, "4X" : 2, "8X" : 3 } )
    
    # ALS and Color Gain Control
    BF_AGAIN   = bitfield_type (
    NAME       = "AGAIN",
    ADDRESS    = 0x8F,
    RST_VAL    = 0x00,
    WIDTH      = 2,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { "1X" : 0, "4X" : 1, "16X" : 2, "64X" : 3 } )

    ######################################
    # CONFIG TWO REGISTER 0x90
    ######################################

    # Proximity Saturation Interrupt Enable
    BF_PSIEN  = bitfield_type (
    NAME       = "PSIEN",
    ADDRESS    = 0x90,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 7,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )
    
    # Clear Photodiode Saturation Interrupt Enable
    BF_CPSIEN   = bitfield_type (
    NAME       = "CPSIEN",
    ADDRESS    = 0x90,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 6,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )
    
    # Additional LDR current during proximity and gesture LED pulses. Current value, set by LDRIVE, is increased by the percentage of LED_BOOST
    BF_LED_BOOST = bitfield_type (
    NAME       = "LED_BOOST",
    ADDRESS    = 0x90,
    RST_VAL    = 0x00,
    WIDTH      = 2,
    OFFSET     = 4,
    ACCESS     = "RW",
    TABLE_ENUM = { "100%" : 0, "150%" : 1, "200%" : 2, "300%" : 3 } )

    ######################################
    # ID REGISTER 0x92
    ######################################

    # The read-only ID Register provides the device identification
    BF_PSIEN  = bitfield_type (
    NAME       = "PSIEN",
    ADDRESS    = 0x92,
    RST_VAL    = 0xAB,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = {  } )

    ######################################
    # STATUS REGISTER 0x93
    ######################################

    # Clear Photodiode Saturation. When asserted, the analog sensor was at the upper end of its dynamic range. The bit can be de-asserted by sending a Clear channel interrupt command (0xE6 CICLEAR) or by disabling the ADC (AEN=0). This bit triggers an interrupt if CPSIEN is set
    BF_CPSAT  = bitfield_type (
    NAME       = "CPSAT",
    ADDRESS    = 0x93,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 7,
    ACCESS     = "RO",
    TABLE_ENUM = {  } )
    
    # Indicates that an analog saturation event occurred during a previous proximity or gesture cycle. Once set, this bit remains set until cleared by clear proximity interrupt special function command (0xE5 PICLEAR) or by disabling Prox (PEN=0). This bit triggers an interrupt if PSIEN is set.
    BF_PGSAT  = bitfield_type (
    NAME       = "PGSAT",
    ADDRESS    = 0x93,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 6,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    # Proximity Interrupt. This bit triggers an interrupt if PIEN in ENABLE is set
    BF_PINT  = bitfield_type (
    NAME       = "PINT",
    ADDRESS    = 0x93,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 5,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    # ALS Interrupt. This bit triggers an interrupt if AIEN in ENABLE is set
    BF_AINT  = bitfield_type (
    NAME       = "AINT",
    ADDRESS    = 0x93,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 4,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    # Gesture Interrupt. GINT is asserted when GFVLV becomes greater than GFIFOTH or if GVALID has become asserted when GMODE transitioned to zero. The bit is reset when FIFO is completely emptied (read)
    BF_GINT  = bitfield_type (
    NAME       = "GINT",
    ADDRESS    = 0x93,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 2,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    # Proximity Valid. Indicates that a proximity cycle has completed since PEN was asserted or since PDATA was last read. A read of PDATA automatically clears PVALID
    BF_PVALID  = bitfield_type (
    NAME       = "PVALID",
    ADDRESS    = 0x93,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 1,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    # ALS Valid. Indicates that an ALS cycle has completed since AEN was asserted or since a read from any of the ALS/Color data registers
    BF_AVALID  = bitfield_type (
    NAME       = "AVALID",
    ADDRESS    = 0x93,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    ######################################
    # CLEAR DATA REGISTER 0x94
    ######################################

    # Clear data lower byte
    BF_CDATAL  = bitfield_type (
    NAME       = "CDATAL",
    ADDRESS    = 0x94,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    ######################################
    # CLEAR DATA REGISTER 0x95
    ######################################

    # Clear data High byte
    BF_CDATAH  = bitfield_type (
    NAME       = "CDATAH",
    ADDRESS    = 0x95,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } ) 
    
    ######################################
    # RED DATA REGISTER 0x96
    ######################################

    # Red data lower byte
    BF_RDATAL  = bitfield_type (
    NAME       = "RDATAL",
    ADDRESS    = 0x96,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    ######################################
    # RED DATA REGISTER 0x97
    ######################################

    # Red data High byte
    BF_RDATAH  = bitfield_type (
    NAME       = "RDATAH",
    ADDRESS    = 0x97,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } ) 

    ######################################
    # GREEN DATA REGISTER 0x98
    ######################################

    # Green data lower byte
    BF_GDATAL  = bitfield_type (
    NAME       = "GDATAL",
    ADDRESS    = 0x98,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    ######################################
    # GREEN DATA REGISTER 0x99
    ######################################

    # Green data High byte
    BF_GDATAH  = bitfield_type (
    NAME       = "GDATAH",
    ADDRESS    = 0x99,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } ) 

    ######################################
    # BLUE DATA REGISTER 0x9A
    ######################################

    # Blue data lower byte
    BF_BDATAL  = bitfield_type (
    NAME       = "BDATAL",
    ADDRESS    = 0x9A,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    ######################################
    # BLUE DATA REGISTER 0x9B
    ######################################

    # Blue data High byte
    BF_BDATAH  = bitfield_type (
    NAME       = "BDATAH",
    ADDRESS    = 0x9B,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } ) 

    ######################################
    # PROXIMITY DATA REGISTER 0x9C
    ######################################

    # Proximity data is stored as an 8-bit value
    BF_PDATA   = bitfield_type (
    NAME       = "PDATA",
    ADDRESS    = 0x9C,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } ) 

    ######################################
    # PROXIMITY OFFSET UP RIGHT REGISTER 0x9D
    ######################################

    # POFFSET_UR is an 8-bit value used to scale an internal offset correction factor to compensate for crosstalk. value is encoded in sign/magnitude format
    BF_POFFSET_UR = bitfield_type (
    NAME       = "POFFSET_UR",
    ADDRESS    = 0x9D,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } ) 

    ######################################
    # PROXIMITY OFFSET DOWN LEFT REGISTER 0x9E
    ######################################

    # POFFSET_DL is an 8-bit value used to scale an internal offset correction factor to compensate for crosstalk. value is encoded in sign/magnitude format
    BF_POFFSET_DL = bitfield_type (
    NAME       = "POFFSET_DL",
    ADDRESS    = 0x9E,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } ) 

    ######################################
    # CONFIG THREE REGISTER 0x9F
    ######################################

    # Proximity Gain Compensation Enable
    BF_PCMP  = bitfield_type (
    NAME       = "PCMP",
    ADDRESS    = 0x9F,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 5,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )

    # Sleep After Interrupt. When enabled, the device will automatically enter low power mode when the INT pin is asserted
    BF_SAI  = bitfield_type (
    NAME       = "SAI",
    ADDRESS    = 0x9F,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 4,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )
    
    # Proximity Mask UP Enable. Writing a 1 disables this photodiode
    BF_PMASK_U  = bitfield_type (
    NAME       = "PMASK_U",
    ADDRESS    = 0x9F,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 3,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )
    
    # Proximity Mask DOWN Enable. Writing a 1 disables this photodiode
    BF_PMASK_D  = bitfield_type (
    NAME       = "PMASK_D",
    ADDRESS    = 0x9F,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 2,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )
    
    # Proximity Mask LEFT Enable. Writing a 1 disables this photodiode
    BF_PMASK_L  = bitfield_type (
    NAME       = "PMASK_L",
    ADDRESS    = 0x9F,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 1,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )
    
    # Proximity Mask RIGHT Enable. Writing a 1 disables this photodiode
    BF_PMASK_R  = bitfield_type (
    NAME       = "PMASK_R",
    ADDRESS    = 0x9F,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )

    ######################################
    # GESTURE PROXIMITY THRESHOLD REGISTER 0xA0
    ######################################

    # Gesture Proximity Entry Threshold. This register sets the Proximity threshold value used to determine a “gesture start” 
    BF_GPENTH  = bitfield_type (
    NAME       = "GPENTH",
    ADDRESS    = 0x9E,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } ) 

    ######################################
    # GESTURE EXIT THRESHOLD REGISTER 0xA1
    ######################################

    # Gesture Exit Threshold. This register sets the threshold value used to determine a “gesture end”
    BF_GPEXTH  = bitfield_type (
    NAME       = "GPEXTH",
    ADDRESS    = 0xA1,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } ) 

    ######################################
    # GESTURE CONFIG ONE REGISTER 0xA2
    ######################################

    # Gesture FIFO Threshold. This value is compared with the FIFO Level ) to generate an interrupt
    BF_GFIFOTH  = bitfield_type (
    NAME       = "GFIFOTH",
    ADDRESS    = 0xA2,
    RST_VAL    = 0x00,
    WIDTH      = 2,
    OFFSET     = 6,
    ACCESS     = "RW",
    TABLE_ENUM = { "1_DATASET" : 0, "4_DATASET" : 1, "8_DATASET" : 2, "16_DATASET" : 3 } )

    # Gesture Exit Mask. Controls which of the gesture detector photodiodes (UDLR) will be included
    BF_GEXMSK_U= bitfield_type (
    NAME       = "GEXMSK_U",
    ADDRESS    = 0xA2,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 5,
    ACCESS     = "RW",
    TABLE_ENUM = { "U_DATA_INCLUDED" : 0, "U_DATA_NOT_INCLUDED" : 1} )
    
     # Gesture Exit Mask. Controls which of the gesture detector photodiodes (UDLR) will be included
    BF_GEXMSK_D= bitfield_type (
    NAME       = "GEXMSK_D",
    ADDRESS    = 0xA2,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 4,
    ACCESS     = "RW",
    TABLE_ENUM = { "D_DATA_INCLUDED" : 0, "D_DATA_NOT_INCLUDED" : 1} )
    
     # Gesture Exit Mask. Controls which of the gesture detector photodiodes (UDLR) will be included
    BF_GEXMSK_L= bitfield_type (
    NAME       = "GEXMSK_L",
    ADDRESS    = 0xA2,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 3,
    ACCESS     = "RW",
    TABLE_ENUM = { "L_DATA_INCLUDED" : 0, "L_DATA_NOT_INCLUDED" : 1} )
    
     # Gesture Exit Mask. Controls which of the gesture detector photodiodes (UDLR) will be included
    BF_GEXMSK_R= bitfield_type (
    NAME       = "GEXMSK_R",
    ADDRESS    = 0xA2,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 2,
    ACCESS     = "RW",
    TABLE_ENUM = { "R_DATA_INCLUDED" : 0, "R_DATA_NOT_INCLUDED" : 1} )
    
    # Gesture Exit Persistence. When a number of consecutive “gesture end” occurrences become equal or greater to the GEPERS value, the Gesture state machine is exited
    BF_GEXPERS = bitfield_type (
    NAME       = "GEXPERS",
    ADDRESS    = 0xA2,
    RST_VAL    = 0x00,
    WIDTH      = 2,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { "1ST_GESTURE_END" : 0, "2ND_GESTURE_END" : 1, "4TH_GESTURE_END" : 2, "7TH_GESTURE_END" : 3 } )

    ######################################
    # GESTURE CONFIG TWO REGISTER 0xA3
    ######################################

    # Gesture Gain Control. Sets the gain of the proximity receiver in gesture mode
    BF_GGAIN  = bitfield_type (
    NAME       = "GGAIN",
    ADDRESS    = 0xA3,
    RST_VAL    = 0x00,
    WIDTH      = 2,
    OFFSET     = 6,
    ACCESS     = "RW",
    TABLE_ENUM = { "1X" : 0, "2X" : 1, "4X" : 2, "8X" : 3 } )

    # Gesture LED Drive Strength. Sets LED Drive Strength in gesture mode
    BF_GLDRIVE = bitfield_type (
    NAME       = "GLDRIVE",
    ADDRESS    = 0xA3,
    RST_VAL    = 0x00,
    WIDTH      = 2,
    OFFSET     = 3,
    ACCESS     = "RW",
    TABLE_ENUM = { "100MA" : 0, "50MA" : 1, "25MA" : 2, "12.5MA" : 3 } )
    
    # Gesture Wait Time. The GWTIME controls the amount of time in a low power mode between gesture detection cycles
    BF_GWTIME  = bitfield_type (
    NAME       = "GWTIME",
    ADDRESS    = 0xA3,
    RST_VAL    = 0x00,
    WIDTH      = 3,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { "0MS" : 0, "2.8MS" : 1, "5.6MS" : 2, "8.4MS" : 3, "14MS" : 4, "22.4MS" : 5, "30.8MS" : 6, "39.2MS" : 7 } )

    ######################################
    # GESTURE UP OFFSET REGISTER 0xA4
    ######################################

    # 8-bit value used to scale an internal offset correction factor to compensate for crosstalk in the application. This value is encoded in sign/magnitude format
    BF_GOFFSET_U = bitfield_type (
    NAME       = "GOFFSET_U",
    ADDRESS    = 0xA4,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } )
    
    ######################################
    # GESTURE UP OFFSET REGISTER 0xA4
    ######################################

    # 8-bit value used to scale an internal offset correction factor to compensate for crosstalk in the application. This value is encoded in sign/magnitude format
    BF_GOFFSET_U = bitfield_type (
    NAME       = "GOFFSET_U",
    ADDRESS    = 0xA4,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } )
    
    ######################################
    # GESTURE DOWN OFFSET REGISTER 0xA5
    ######################################

    # 8-bit value used to scale an internal offset correction factor to compensate for crosstalk in the application. This value is encoded in sign/magnitude format
    BF_GOFFSET_D = bitfield_type (
    NAME       = "GOFFSET_D",
    ADDRESS    = 0xA5,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } )
    
    ######################################
    # GESTURE LEFT OFFSET REGISTER 0xA7
    ######################################

    # 8-bit value used to scale an internal offset correction factor to compensate for crosstalk in the application. This value is encoded in sign/magnitude format
    BF_GOFFSET_L = bitfield_type (
    NAME       = "GOFFSET_L",
    ADDRESS    = 0xA7,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } )
    
    ######################################
    # GESTURE RIGHT OFFSET REGISTER 0xA9
    ######################################

    # 8-bit value used to scale an internal offset correction factor to compensate for crosstalk in the application. This value is encoded in sign/magnitude format
    BF_GOFFSET_R = bitfield_type (
    NAME       = "GOFFSET_R",
    ADDRESS    = 0xA9,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } )

    ######################################
    # GESTURE PULSE COUNT AND LENGTH REGISTER 0xA6
    ######################################

    # Gesture Pulse Length. Sets the LED_ON pulse width during a Gesture LDR Pulse
    BF_GPLEN  = bitfield_type (
    NAME       = "GPLEN",
    ADDRESS    = 0xA6,
    RST_VAL    = 0x01,
    WIDTH      = 2,
    OFFSET     = 6,
    ACCESS     = "RW",
    TABLE_ENUM = { "4US" : 0, "8US" : 1, "16US" : 2, "32US" : 3 } )
    
    # Number of Gesture Pulses. Specifies the number of pulses to be generated on LDR. Number of pulses is set by GPULSE value plus 1
    BF_GPULSE  = bitfield_type (
    NAME       = "GPULSE",
    ADDRESS    = 0xA6,
    RST_VAL    = 0x00,
    WIDTH      = 6,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { } )
    
    ######################################
    # GESTURE CONFIG THREE REGISTER 0xAA
    ######################################

    # Gesture Dimension Select. Selects which gesture photodiode pairs are enabled to gather results during gesture
    BF_GDIMS  = bitfield_type (
    NAME       = "GDIMS",
    ADDRESS    = 0xAA,
    RST_VAL    = 0x00,
    WIDTH      = 2,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { "UP_DOWN_LEFT_RIGHT_VALID" : 0, "ONLY_UP_DOWN" : 1, "ONLY_LEFT_RIGHT" : 2 } )
    
    ######################################
    # GESTURE CONFIG FOUR REGISTER 0xAB
    ######################################

    # Setting this bit to '1' clears GFIFO, GINT, GVALID, GFIFO_OV and GFIFO_LVL
    BF_GFIFO_CLR = bitfield_type (
    NAME       = "GFIFO_CLR",
    ADDRESS    = 0xAB,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 2,
    ACCESS     = "WO",
    TABLE_ENUM = { "FIFO_CLEAR" : 1 } )
    
    # Gesture interrupt enable. When asserted, all gesture related interrupts are unmasked
    BF_GIEN    = bitfield_type (
    NAME       = "GIEN",
    ADDRESS    = 0xAB,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 1,
    ACCESS     = "RW",
    TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )
    
    # Gesture Mode. Writing a 1 to this bit causes immediate entry in to the gesture state machine
    BF_GMODE   = bitfield_type (
    NAME       = "GMODE",
    ADDRESS    = 0xAB,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 0,
    ACCESS     = "RW",
    TABLE_ENUM = { "ALS_MODE" : 0, "GESTURE_MODE" : 1 } )
    
    ######################################
    # GESTURE FIFO LEVEL REGISTER 0xAE
    ######################################

    # Gesture FIFO Level. This register indicates how many four byte data sets - UDLR are ready for read over I2C. One four-byte dataset is equivalent to a single count in GFLVL.
    BF_GFLVL  = bitfield_type (
    NAME       = "GFLVL",
    ADDRESS    = 0xAE,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    ######################################
    # GESTURE STATUS REGISTER 0xAF
    ######################################

    # Gesture FIFO Overflow. A setting of 1 indicates that the FIFO has filled to capacity and that new gesture detector data has been lost
    BF_GFOV  = bitfield_type (
    NAME       = "GFOV",
    ADDRESS    = 0xAF,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 1,
    ACCESS     = "RO",
    TABLE_ENUM = { "NO_OVERFLOW" : 0, "OVERFLOW" : 1 } )
    
    # GVALID bit is high when GFLVL becomes greater than GFIFOTH (i.e. FIFO has enough data to set GINT). GFIFOD is reset when GMODE = 0 and the GFLVL=0 (i.e., All FIFO data has been read)
    BF_GVALID  = bitfield_type (
    NAME       = "GVALID",
    ADDRESS    = 0xAF,
    RST_VAL    = 0x00,
    WIDTH      = 1,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    ######################################
    # FORCE INTERRUPT REGISTER 0xE4
    ######################################

    # Forces an interrupt (any value)
    BF_IFORCE  = bitfield_type (
    NAME       = "IFORCE",
    ADDRESS    = 0xE4,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "WO",
    TABLE_ENUM = { } )
    
    ######################################
    # PROXIMITY INTERRUPT CLEAR REGISTER 0xE5
    ######################################

    # Proximity interrupt clear (any value)
    BF_PICLEAR = bitfield_type (
    NAME       = "PICLEAR",
    ADDRESS    = 0xE5,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "WO",
    TABLE_ENUM = { } )
    
    ######################################
    # ALS INTERRUPT CLEAR REGISTER 0xE6
    ######################################

    # ALS interrupt clear (any value
    BF_CICLEAR = bitfield_type (
    NAME       = "CICLEAR",
    ADDRESS    = 0xE6,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "WO",
    TABLE_ENUM = { } )
    
    ######################################
    # NON-GESTURE INTERRUPT CLEAR REGISTER 0xE7
    ######################################

    # Clears all non-gesture interrupts (any value)
    BF_AICLEAR = bitfield_type (
    NAME       = "AICLEAR",
    ADDRESS    = 0xE7,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "WO",
    TABLE_ENUM = { } )
    
    ######################################
    # GESTURE UP FIFO REGISTER 0xFC
    ######################################

    # Gesture FIFO UP value
    BF_GFIFO_U = bitfield_type (
    NAME       = "GFIFO_U",
    ADDRESS    = 0xFC,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    ######################################
    # GESTURE DOWN FIFO REGISTER 0xFD
    ######################################

    # Gesture FIFO DOWN value
    BF_GFIFO_D = bitfield_type (
    NAME       = "GFIFO_D",
    ADDRESS    = 0xFD,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    ######################################
    # GESTURE LEFT FIFO REGISTER 0xFE
    ######################################

    # Gesture FIFO LEFT value
    BF_GFIFO_L = bitfield_type (
    NAME       = "GFIFO_L",
    ADDRESS    = 0xFE,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } )
    
    ######################################
    # GESTURE RIGHT FIFO REGISTER 0xFF
    ######################################

    # Gesture FIFO RIGHT value
    BF_GFIFO_R = bitfield_type (
    NAME       = "GFIFO_R",
    ADDRESS    = 0xFF,
    RST_VAL    = 0x00,
    WIDTH      = 8,
    OFFSET     = 0,
    ACCESS     = "RO",
    TABLE_ENUM = { } )


    LIST_OF_BIT_FIELDS = [ BF_PON, BF_AEN, BF_PEN, BF_WEN, BF_AIEN, BF_PIEN, BF_GEN,
                           BF_ATIME, BF_WTIME, BF_AILTL, BF_AILTH, BF_AIHTL, BF_AIHTH,
                           BF_PILT, BF_PIHT, BF_PPERS, BF_APERS, BF_WLONG, BF_PPLEN,
                           BF_PPULSE, BF_LDRIVE, BF_PGAIN, BF_AGAIN, BF_PSIEN, BF_CPSIEN,
                           BF_LED_BOOST, BF_PSIEN, BF_CPSAT, BF_PGSAT, BF_PINT, BF_AINT,
                           BF_GINT, BF_PVALID, BF_AVALID, BF_CDATAL, BF_CDATAH, BF_RDATAL,
                           BF_RDATAH, BF_GDATAL, BF_GDATAH, BF_BDATAL, BF_BDATAH, BF_PDATA,
                           BF_POFFSET_UR, BF_POFFSET_DL, BF_PCMP, BF_SAI, BF_PMASK_U,
                           BF_PMASK_D, BF_PMASK_L, BF_PMASK_R, BF_GPENTH, BF_GPEXTH,
                           BF_GFIFOTH, BF_GEXMSK_U, BF_GEXMSK_D, BF_GEXMSK_L, BF_GEXMSK_R,
                           BF_GEXPERS, BF_GGAIN, BF_GLDRIVE, BF_GWTIME, BF_GOFFSET_U, BF_GOFFSET_U,
                           BF_GOFFSET_D, BF_GOFFSET_L, BF_GOFFSET_R, BF_GPLEN, BF_GPULSE,
                           BF_GDIMS, BF_GFIFO_CLR, BF_GIEN, BF_GMODE, BF_GFLVL, BF_GFOV,
                           BF_GVALID, BF_IFORCE, BF_PICLEAR, BF_CICLEAR, BF_AICLEAR, BF_GFIFO_U,
                           BF_GFIFO_D, BF_GFIFO_L, BF_GFIFO_R ]

    LIST_OF_INT_STATUS_BIT_FIELDS = [ BF_CPSAT, BF_PGSAT, BF_PINT, BF_AINT, BF_GINT, BF_PVALID, BF_AVALID ]

    def i2c_bf_read(self, bit_field):
        try:
            address  = 0xFF & bit_field.ADDRESS
            read_byte = self.bus.readfrom_mem(self.slave_id, address, 1)
            read_int   = list(read_byte)[0]
            bf_read_data = ( read_int & bit_field.BIT_MASK ) >> bit_field.OFFSET 
            if (self.debug):
                print("Read bit_field {} address 0x{:02x}, bit mask is 0x{:02x}, value is 0x{:02x}".format(bit_field.NAME, address, bit_field.BIT_MASK, bf_read_data))
            return bf_read_data
        except:
            print("ERROR with i2c_bf_read")

    def i2c_bf_write(self, bit_field, bf_wdata):
        try:
            address = 0xFF & bit_field.ADDRESS
            read_byte = self.bus.readfrom_mem(self.slave_id, address,1)
            read_int   = list(read_byte)[0]
            wdata = ( read_int & ~bit_field.BIT_MASK) | ((bf_wdata << bit_field.OFFSET) & bit_field.BIT_MASK)
            self.bus.writeto_mem(self.slave_id, address, bytearray([wdata & 0xFF]))
            if (self.debug):
                print("Wrote bit_field {} address 0x{:02x}, bit mask is 0x{:04x}, data 0x{:02x}".format(bit_field.NAME, address, bit_field.BIT_MASK, bf_wdata))
        except:
            print("ERROR with i2c_bf_write")

    def read_flags(self):
        list_of_flags = []
        try:
            read_byte = self.bus.readfrom_mem(self.slave_id, 0x93, 1)
            read_int   =  list(read_byte)[0]
            for bit_field in self.LIST_OF_INT_STATUS_BIT_FIELDS:
                if (2 ** bit_field.OFFSET & read_int):
                    list_of_flags.append(bit_field.NAME)
            if (self.debug):
                print("Flag raw data is 0x{:04x}".format(word_read))
                print(*list_of_flags)
            return list_of_flags
        except:
            print("ERROR with read_flags")

    def check_default_values(self,debug=False):
        list_of_bit_fields = []
        for bit_field in self.LIST_OF_BIT_FIELDS:
            if (bit_field.ACCESS == "RW"):
                value       = self.i2c_bf_read(bit_field)
                reset_value = bit_field.RST_VAL
                if (value != reset_value):
                    list_of_bit_fields.append(bit_field)
                    if (self.debug or debug):
                        print("{:<10s} value is {:d}, reset value is {:d}".format(bit_field.NAME,value,reset_value))
        return list_of_bit_fields

    def restore_default_values(self):
        for bit_field in self.LIST_OF_BIT_FIELDS:
            if (bit_field.ACCESS == "RW"):
                self.i2c_bf_write(bit_field, bit_field.RST_VAL)

    def get_key(self, val, my_dict):
        for key, value in my_dict.items():
            if val == value:
                return key

    def read_bf_and_print(self, bit_field):
        value = self.i2c_bf_read(bit_field)
        if (len(bit_field.TABLE_ENUM) != 0):
            print("Bit Field {} is {}".format(bit_field.NAME, self.get_key(value,bit_field.TABLE_ENUM)))
        else:
            print("Bit Field {} has value 0x{:04x}".format(bit_field.NAME, value))