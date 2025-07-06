import requests
import sys
import os
import asyncio
import websockets
import keyboard


PORT = 8426
HOST_IP = "127.0.0.1"
URL = f"http://{HOST_IP}:{PORT}"
WS_URL = f"ws://{HOST_IP}:{PORT}"

APP_NAME:str = "Krolaks Dungeon"
APP_VERSION:str = "0.1.0"

register_data = {
    "username": "user",
    "passcode": "6FGL28",
    "email": "user@webmail.com"
}

login_data = {
    "username": "user",
    "passcode": "6FGL28",
}

print(f"{APP_NAME}: {APP_VERSION}")



def get_login_credentials():
    username = ""
    password = ""
    selected = 0  # 0 = username, 1 = password

    def set_cursor_position(x, y):
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    def clear_line():
        sys.stdout.write("\033[K") # Clear from cursor to end of line
        sys.stdout.flush()

    # Initial setup: clear screen and print static instructions
    clear_screen()
    sys.stdout.write("Use ↑ ↓ to move, type to enter, and Enter to login\n\n") # Added an extra newline for spacing
    sys.stdout.flush()

    # Define print_form to only update dynamic parts
    def print_form():
        # Print Username field
        set_cursor_position(1, 4) # Go to start of username line (line 4 because of 2 newlines above)
        clear_line()
        sys.stdout.write("-> Username: " if selected == 0 else "   Username: ") # Added space for better alignment
        sys.stdout.write(username)

        # Print Password field
        set_cursor_position(1, 5) # Go to start of password line
        clear_line()
        sys.stdout.write("-> Password: " if selected == 1 else "   Password: ") # Added space
        sys.stdout.write("*" * len(password))

        # Position cursor for input
        if selected == 0:
            set_cursor_position(15 + len(username), 4) # 15 is "   Username: " length
        else:
            set_cursor_position(15 + len(password), 5) # 15 is "   Password: " length
        sys.stdout.flush() # Flush after positioning cursor

    # Initial call to print the form
    print_form()

    error = ""
    while True:
        # Print error message if any
        set_cursor_position(1, 7) # Position for error message
        clear_line()
        sys.stdout.write(error)
        sys.stdout.flush()
        error = "" # Clear error after displaying

        event = keyboard.read_event()

        if event.event_type != keyboard.KEY_DOWN:
            continue

        key = event.name

        # Arrow keys to switch input
        if key == "up":
            selected = (selected - 1) % 2
        elif key == "down":
            selected = (selected + 1) % 2

        # Alphanumeric input
        elif len(key) == 1:
            if selected == 0:
                username += key
            else:
                password += key

        elif key == "tab":
            selected = not selected


        # Handle backspace
        elif key == "backspace":
            if selected == 0 and username:
                username = username[:-1]
            elif selected == 1 and password:
                password = password[:-1]

        # Submit with Enter
        elif key == "enter":
            if 3 < len(username) < 9 and len(password) > 5: # Corrected boolean logic
                break
            else:
                error = "Please Enter a Valid Name and Password!\n( Between 4-9 characters )"

        print_form() # This will now only update the dynamic parts
    clear_screen() # Clear screen before returning
    return username, password

def get_register_credentials():
    username = ""
    password = ""
    email = ""
    selected = 0  # 0 = username, 1 = password, 2 = email

    def set_cursor_position(x, y):
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    def clear_line():
        sys.stdout.write("\033[K") # Clear from cursor to end of line
        sys.stdout.flush()

    # Initial setup: clear screen and print static instructions
    clear_screen()
    sys.stdout.write("Use ↑ ↓ to move, type to enter, and Enter to submit\n\n") # Added an extra newline for spacing
    sys.stdout.flush()

    # Define print_form to only update dynamic parts
    def print_form():
        sys.stdout.write("Register New Account:\n")
        # Print Username field
        set_cursor_position(1, 5) # Go to start of username line (line 4 because of 2 newlines above)
        clear_line()
        sys.stdout.write("-> Username: " if selected == 0 else "   Username: ") # Added space for better alignment
        sys.stdout.write(username)

        # Print Password field
        set_cursor_position(1, 6) # Go to start of password line
        clear_line()
        sys.stdout.write("-> Password: " if selected == 1 else "   Password: ") # Added space
        sys.stdout.write("*" * len(password))

        # Print Email field
        set_cursor_position(1, 7) # Go to start of email line
        clear_line()
        sys.stdout.write("-> Email: " if selected == 2 else "   Email: ") # Added space
        sys.stdout.write(email)

        # Position cursor for input
        if selected == 0:
            set_cursor_position(15 + len(username), 5) # 15 is "   Username: " length
        elif selected == 1:
            set_cursor_position(15 + len(password), 6) # 15 is "   Password: " length
        else:
            set_cursor_position(12 + len(email), 7) # 12 is "   Email: " length
        sys.stdout.flush() # Flush after positioning cursor

    # Initial call to print the form
    print_form()

    error = ""
    while True:
        # Print error message if any
        set_cursor_position(1, 9) # Position for error message
        clear_line()
        sys.stdout.write(error)
        sys.stdout.flush()
        error = "" # Clear error after displaying

        event = keyboard.read_event()

        if event.event_type != keyboard.KEY_DOWN:
            continue

        key = event.name

        # Arrow keys to switch input
        if key == "up":
            selected = (selected - 1) % 3
        elif key == "down":
            selected = (selected + 1) % 3

        # Alphanumeric input
        elif len(key) == 1:
            if selected == 0:
                username += key
            elif selected == 1:
                password += key
            else:
                email += key

        elif key == "tab":
            selected = (selected + 1) % 3


        # Handle backspace
        elif key == "backspace":
            if selected == 0 and username:
                username = username[:-1]
            elif selected == 1 and password:
                password = password[:-1]
            elif selected == 2 and email:
                email = email[:-1]

        # Submit with Enter
        elif key == "enter":
            if 3 < len(username) < 9 and len(password) > 5 and "@" in email and "." in email: # Corrected boolean logic
                break
            else:
                error = "Please Enter a Valid Name, Password, and Email!\n(Name: 4-9 chars, Pass: >5 chars, Email: valid format)"

        print_form() # This will now only update the dynamic parts
    clear_screen() # Clear screen before returning
    return username, password, email



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')    
    
#|| Main Menu
main_menu_title = "Krolaks Dungeon\n"
main_menu_desc = main_menu_title + "Use ↑ ↓ to move, type to enter, and Enter to login\n"
main_menu_options = ["Login","Register","About","Quit"]
username:str = "no-username"
password:str = "no-password"

def run_choice_menu(selected:int=0, desc:str = "", options:[str]=[""]):
    def print_form():
        clear_screen()
        print(desc)
        s:int=0
        c_curs = ""
        for line in options:
            if s == selected:
                c_curs = " >"
            else:
                c_curs = ""
            print(c_curs+line)
            s+=1
            
    print_form()


    while True:
        event = keyboard.read_event()

        if event.event_type != keyboard.KEY_DOWN:
            continue

        key = event.name

        # Arrow keys to switch input
        options_length = len(options)
        if key == "up":
            selected = (selected - 1) % options_length
        elif key == "down":
            selected = (selected + 1) % options_length

        # Submit with Enter
        elif key == "enter":
            break

        print_form()

    clear_screen()
    
    return selected



in_login_menus:bool = True


l_choice = 0 #| Store Menu Cursor Position
while in_login_menus:
    # Input Username and Password
    mm_opt:int = run_choice_menu(l_choice, main_menu_desc, main_menu_options)

    match mm_opt:
        case 0:
            print("Login")
            username,password = get_login_credentials()
            login_data["username"] = username
            login_data['passcode'] = password
            response = requests.post(URL + "/submit_login/", data=login_data)

            print(response.json()["message"])
            if response.json()["message"] == "Logged In!":
                in_login_menus = False
                break   
            else:
                keyboard.read_key(True)
                keyboard.read_key(True)         
            #print("Status code:", response.status_code)
                
 



            #in_login_menus = False
            #break
        case 1:
            print("Register")
            username,password,email = get_register_credentials()
            register_data["username"] = username
            register_data['passcode'] = password
            register_data['email'] = email
            response = requests.post(URL + "/submit_register/", data=register_data)

            #print("Status code:", response.status_code)
            print("Response JSON:", response.json()["message"])    
            keyboard.read_key(True)
            keyboard.read_key(True)  

        case 2:
            print("About")
            print("An ode to the games and developers of the past...")
            print("\nA Multiplayer Console RPG Akin to Tabletops.\n")
            print("* Note Taking is advised! *")
            print("* Visit website for charactersheets * ")
            print("* https://krolaks-dungeon.online *")
            keyboard.read_key(True)
            keyboard.read_key(True)
        case 3:
            print("Quit")    
            in_login_menus=False
            sys.exit("Quit Game")
            
                        




# username, password = run_choice_menu()
print(username, password)



# Form fields (must match the names expected by FastAPI)
form_data = {
    "username": "user",
    "wins": 0,
    "deaths": 0
}



#response = requests.post(URL + "/submit_form/", data=form_data)

#print("Status code:", response.status_code)
#print("Response JSON:", response.json())

input("Press enter to continue")

# username = "user" # Assuming "user" is a valid username for testing
# my_stats = requests.get(f"{URL}/get_stats/{username}")
# print("Stats:", my_stats.json())

# input("Press enter to continue")

async def test_websocket():
    async with websockets.connect(WS_URL + "/ws") as websocket:
        await websocket.send("Hello WebSocket from Client!")
        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                print(f"Received from WebSocket: {message}")
            except asyncio.TimeoutError:
                # No message received, send a tick
                await websocket.send("Client Tick!")
            except Exception as e:
                print(f"WebSocket error: {e}")
                break

if __name__ == "__main__":
    asyncio.run(test_websocket())