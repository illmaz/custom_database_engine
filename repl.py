from query import insert, select_all, select_where, delete, select_by_id

def parse_value(value):
    try:
        return int(value)
    except ValueError: 
        return value

def run():
    print("custom-engine. type 'help' for commands, 'exit' to quit.")
    while True: 
        line = input("> ").strip()
        if line == "exit":
            print("bye.")
            break
        elif line == "help":
            print("commands:")
            print("  insert <id> <name> <age>")
            print("  select all")
            print("  select id <id>")
            print("  select where <field> <value>")
            print("  delete <field> <value>")
            print("  exit")

        elif line == "select all":
            rows = select_all()
            if len(rows) == 0:
                print("no rows.")
            else:
                for row in rows:
                    print(row)
        
        elif line.startswith("insert"):
            parts = line.split()
            if len(parts) != 4:
                print("usage: insert <id> <name> <age>")
            else: 
                insert({"id": int(parts[1]), "name": parts[2], "age": int(parts[3])})
                print("inserted.")
        
        elif line.startswith("select where"):
            parts = line.split()
            if len(parts) !=4:
                print("usage: select where <field> <value>")
            else: 
                rows = select_where(parts[2], parse_value(parts[3]))
                if len (rows) == 0:
                    print("no rows.")
                else: 
                    for row in rows: 
                        print(row)

        elif line.startswith("select id"):
            parts = line.split()
            if len(parts) !=3:
                print("usage: select id <id>")
            else:
                row = select_by_id(int(parts[2]))
                if row is None:
                    print("no row found.")
                else:
                    print(row)
        
        elif line.startswith("delete"):
            parts = line.split()
            if len(parts) != 3:
                print("usage: delete <field> <value>")
            else:
                delete(parts[1], parse_value(parts[2]))
                print("deleted.")
        else: 
            print(f"unknown command: '{line}'. type 'help' for commands.")

run()