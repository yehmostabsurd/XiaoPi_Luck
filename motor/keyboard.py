import keyboard #Using module keyboard
while True:#making a loop
    try: #used try so that if user pressed other than the given key error will not be shown
	print("1")
	time.sleep(1)
        if keyboard.is_pressed('q'):#if key 'q' is pressed 
            print('You Pressed A Key!')
            break#finishing the loop
        else:
            pass
    except:
        break
