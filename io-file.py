#Setting up the interface

#Setting up the interface
import os
import sys
from engine import Table
from bst_file import bs_tree
from bst_file import TreeNode
from storage import load_database, save_database
def clear_screen():
    # Clears terminal for both Windows ('cls') and Linux/Mac ('clear')
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("========================================")
    print("         NBS DBMS PROJECT v1.0          ")
    print("========================================\n")
# ---------------------------------------------


def main():
    clear_screen()
    print_banner()
    table,table_index=load_database()
    curr_table = None 
    curr_table_name = None
    while True:
        try:
            if curr_table is None:
                prompt = "dbms>> "
            else:
                prompt = f"dbms>>{curr_table_name}>> "
            raw_input = input(prompt)
            
            clean_input = raw_input.strip()
            if not clean_input:
                continue
                
            command_parts = clean_input.split() 
            action = command_parts[0].upper()

            if action == "EXIT":
                print("Compressing and saving data...")
                save_database(table, table_index)
                # Call File 4's save function here!
                sys.exit(0)
            elif action=="CREATE_TABLE":
                if len(command_parts)<4:
                    print("ERROR:INSUFFICIENT DATA")
                    continue
                table_name = command_parts[1]
                if table_index.get(table_name) != None:
                    print("ERROR:TABLE ALREADY EXIST ")
                    continue

                a = Table(8)
                a.col_name = command_parts[3:]
                table.append(a)
                n = len(table)-1
                table_index[table_name] = n



            elif action == "ENTER_TABLE":
                if curr_table != None:
                    print("ERROR:TABLE ALREADY OPEN")
                    continue
                if(len(command_parts)!=2):
                    print("ERROR: INVALID SYNTAX")
                    continue
                b = table_index.get(command_parts[1])
                if b == None:
                    print("ERROR:TABLE DOESN'T EXIST")
                    continue

                curr_table = table[b]
                curr_table_name = command_parts[1]


            elif action == "SHOW_TABLE":
                if len(table_index) == 0:
                    print("ERROR:NO TABLE CREATED")
                    continue
                for i,j in table_index.items():
                    print(i)
                    


            elif action == "EXIT_TABLE":
                curr_table = None
                curr_table_name = None


            elif action == "INSERT":
                
                lst = command_parts[1:]
                for i in range(len(lst)):
                    if lst[i].isdigit() == True:
                        lst[i] = int(lst[i])

                if curr_table == None:
                    print("ERROR:NO TABLE OPEN")
                    continue
                if len(lst) != len(curr_table.col_name):
                    print("ERROR:INSUFFICIENT DATA")
                    continue
                p=curr_table.search(lst[0])
                if(p!="ERROR: NOT FOUND"):
                    print("ERROR:DATA ALREADY PRESENT")
                    continue
                curr_table.insert(lst)
                continue
       
            elif action == "DISPLAY":
                if curr_table == None:
                    print("ERROR: NO TABLE OPEN")
                    continue
                # my_db.display_all()
                a=curr_table.display()
                if(a== None):
                    print("ERROR: NO INPUT FOUND")
                    continue
                print("| ",end="")
                for i in curr_table.col_name:
                    print(f" {i} |", end="")
                print()
                print()
                for i in a:
                    print("| ",end="")
                    for j in i:
                        print(f" {j} |", end="")
                    print("\n")
 

            elif action=="DELETE":
                if curr_table == None:
                    print("ERROR : NO TABLE OPEN")
                    continue
                a = command_parts[1]
                if a.isdigit() == True:
                    a = int(a)
                if curr_table.datatype == None:
                    print("ERROR:DATA NOT PRESENT")
                    continue
                if type(a) != curr_table.datatype :
                    print("ERROR:DATATYPE DOESN'T MATCH")
                    continue
                
                curr_table.delete(a)


            elif action=="EDIT":
                if curr_table == None:
                    print("ERROR:NO TABLE OPEN")
                    continue
                if curr_table.datatype == None:
                    print("ERROR:DATA NOT PRESENT")
                    continue
                if (len(command_parts) !=6):
                    print("ERROR:INVALID SYNTAX")
                    continue
                a = command_parts[5]
                if a.isdigit()==True:
                    a=int(a)
                if type(a) != curr_table.datatype:
                    print("ERROR:INPUT HAS WRONG DATATYPE")
                    continue
                try:
                    b = curr_table.col_name.index(command_parts[1])
                except ValueError:
                    print("ERROR:COLUMN DOESN'T EXIST")
                    continue
                c = command_parts[3]
                if command_parts[3].isdigit() == True:
                    c = int(command_parts[3])
                if b == 0 and type(c) != curr_table.datatype:
                    print("ERROR: NEW PRIMARY KEY MUST MATCH TABLE DATATYPE")
                    continue
                curr_table.edit(a , b , c)

                
            elif action=="SEARCH":
                if curr_table == None:
                    print("ERROR:NO TABLE OPEN")
                    continue
                a = command_parts[1]
                if a.isdigit() == True:
                    a = int(a)
                if curr_table.datatype == None:
                    print("ERROR:DATA DOESN'T EXIST")
                    continue
                if type(a) != curr_table.datatype:
                    print("ERROR:DATATYPE DOESN'T MATCH")
                    continue
                p=curr_table.search(a)
                if(p=="ERROR: NOT FOUND"):
                    print("ERROR: NOT FOUND")
                    continue
                print("| ",end="")
                for i in p:
                    print(f" {i} |", end="")
                print()

            else:
                print(f"Error: Unknown command '{action}'")

        # Catch Ctrl+C gracefully
        except KeyboardInterrupt:
            print("\nForce quitting. Data may not be saved!")
            save_database(table, table_index)
            sys.exit(0)
        except IndexError:
            print("Error: Missing arguments. Please check your command syntax.")
        # Catch if they type letters for the ID instead of numbers
        except ValueError as e:
            print(f"System Error: Invalid data format as ({e})")

if __name__ == "__main__":
    main()
