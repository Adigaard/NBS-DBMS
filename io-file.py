#Setting up the interface

#Setting up the interface
import os
import sys
from engine import Table
from bst_file import bs_tree
from bst_file import TreeNode
# You will import File 3 and File 4 here later!
# from engine import Table
# from storage import save_database

def clear_screen():
    # Clears terminal for both Windows ('cls') and Linux/Mac ('clear')
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("========================================")
    print("       AIGA DBMS PROJECT v1.0          ")
    print("      Type 'EXIT' to save and close     ")
    print("========================================\n")
# ---------------------------------------------


def main():
    clear_screen()
    print_banner()
    table=[]
    table_index={}
    # Initialize your Database Engine here (from File 3)
    # my_db = Table() 

    # --- THIS IS THE PART YOUR TEAM WRITES (The REPL) ---
    while True:
        try:
            # 1. The Prompt
            raw_input = input("dbms>> ")
            
            # 2. The Lexer (Clean and split the input)
            clean_input = raw_input.strip()
            if not clean_input:
                continue # If they just hit Enter, do nothing and loop again
                
            # Split into words: ["INSERT", "101", "Alice"]
            command_parts = clean_input.split(" ") 
            
            # The first word is the action. Convert it to UPPERCASE so 
            # 'insert', 'Insert', and 'INSERT' all work.
            action = command_parts[0].upper()

            # 3. The Router
            if action == "EXIT":
                print("Compressing and saving data...")
                # Call File 4's save function here!
                sys.exit(0)
            elif action=="CREATE_TABLE":
                print("created table")











































            elif action == "ENTER_TABLE":
                print("entered table")




            











































            elif action == "SHOW_TABLE":
                print("show table")
















































            elif action == "EXIT_TABLE":
                print("EXIT TABLE")
















































            elif action == "INSERT":
                # Check if they provided enough arguments
                if len(command_parts) < 4:
                    print("Error: INSERT requires ID, Name, and Email.")
                else:
                    user_id = int(command_parts[1])
                    name = command_parts[2]
                    email = command_parts[3]
                    # my_db.insert(user_id, name, email)
                    print(f"Success: Inserted {name} into database.")


































                    
            elif action == "DISPLAY":
                # my_db.display_all()
                print("Displaying all records...")















































            elif action=="DELETE":
                print("Deleted node")
















































            elif action=="EDIT":
                print("EDITED the data")
















































            elif action=="SEARCH":
                print("search")
















































            else:
                print(f"Error: Unknown command '{action}'")

        # Catch Ctrl+C gracefully
        except KeyboardInterrupt:
            print("\nForce quitting. Data may not be saved!")
            sys.exit(0)
        # Catch if they type letters for the ID instead of numbers
        except ValueError:
            print("Error: ID must be a number.")

if __name__ == "__main__":
    main()
