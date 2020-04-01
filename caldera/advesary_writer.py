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

tgt_list = ['10.0.2.5', '10.0.2.6','10.0.2.7']

src_id = str(uuid.uuid4())
src_file = open("sources/"+src_id+".yml","w")
src_file.write("---\n\n")
src_file.write("id: "+src_id+"\n")
src_file.write("name: AI Filters\n")
src_file.write("facts: {}\n")
src_file.write("rules:\n")
src_file.write("  - action: DENY\n")
src_file.write("    fact: my.host.ip\n")
src_file.write("    match: .*\n")

for tgt in tgt_list:
    src_file.write("  - action: ALLOW\n")
    src_file.write("    fact: my.host.ip\n")
    src_file.write("    match: "+tgt+"\n")

print("Rules for "+str(len(tgt_list))+" targets created")
