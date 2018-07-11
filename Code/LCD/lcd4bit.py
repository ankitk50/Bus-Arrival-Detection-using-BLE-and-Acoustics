from RPLCD import CharLCD
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[23, 29, 31, 33])
lcd.write_string(u'Bus C2305,      has arrived')
