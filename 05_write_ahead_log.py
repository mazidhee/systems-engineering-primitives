import os

# i need a python database, dictionary
# it needs to to write to a local file on disk before it does anything to the database 

class WAL:
    def __init__(self, filepath: str):
        self.db = dict()
        self.path = filepath
        self._rebuild_log()

    def _append_raw_txt(self, cmd: str):
        if not cmd:
            print("please provide a valid command to be appended")
            return
        with open(self.path,"a") as file:
           file.write(f"{cmd}\n") #\
           print(f"{cmd} save to local disk file {self.path}")

    def _rebuild_log(self):
        if not os.path.exists(self.path):
            return
        with open(self.path, "r") as file:
            for line in file:
                parts = line.strip().split(maxsplit=2) #2 zero index
                if len(parts) == 3 and parts[0] == "SET":
                    self.db[parts[1]] = parts[2]
                elif len(parts) == 2 and parts[0] == "DEL":
                    self.db.pop(parts[1], None)

    def set(self, key, value):
        cmd = f"SET {key} {value}"
        self._append_raw_txt(cmd)
        self.db[key] = str(value)

    def get(self, key):
        return self.db.get(key)

    def delete(self, key):
        cmd = f"DEL {key}"
        self._append_raw_txt(cmd)
        self.db.pop(key, None)



my_db = WAL("my_database.txt")

my_db.set("GOOGL", 60000)
my_db.set("AAPL", 3000)
my_db.delete("GOOGL")

print(my_db.get("AAPL"))