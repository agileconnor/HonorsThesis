import uuid
import csv

uuid_file = open("uuid_table.csv", 'r')
uuid_table = csv.reader(uuid_file)

uuid_dict = {rows[0]:rows[1] for rows in uuid_table}
uuid_file.close()
print("UUIDs loaded...")


new_id = str(uuid.uuid4())

adv_file = open("adversary/"+new_id+".yml", 'w')
adv_file.write("---\n\n")
adv_file.write("id: "+new_id+"\n")
adv_file.write("name: AI Adversary\n")
adv_file.write("description: N/A\n")
adv_file.write("phases:\n")

adv_file.write("  1:\n")
adv_file.write("    - "+uuid_dict["VNC"]+"\n")
adv_file.write("    - "+uuid_dict["FTP"]+"\n")
adv_file.write("    - "+uuid_dict["SMTP"]+"\n")

adv_file.close()
print("Adversary Created")
