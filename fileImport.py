import glob
import re
import requests

header_for_mp_file = """/DELIMITER="|"
/DATEFORMAT="YYYY-MM-DD HH24:MI:SS"
/TABLE_WHERE=<PATRONGROUPS><PATRONID=PIK(2) and GROUPNUMBER=VALUE(10)>"""
varz = "group_number", "start_date", "expiration_date", "ticket_number"

#expecting a csv with the header of the format: group #, start date, expiry date, ticket #
#rows of data under the header should be userid/email/pik (any of 1), first name, middle name, last name 

# dont leave these here lol
secrets_server = "???"
username = "???"

files = glob.glob("./*.csv")

for d in files:
    with open(d) as f, open("Import" + re.sub(r'\W+', '',str(d).split(".csv")[0]) + ".mp", "a") as append_file:
        error_file = open("errors.txt", "a")
        two_header_for_mp_file = "/FIELDS=UPDATE_MODE|PRIMARYKEYVALUE|PATRONGROUPS.GROUPNUMBER|","PATRONGROUPS.GROUPEFFECTIVE|","PATRONGROUPS.GROUPEXPIRE|","PATRONGROUPS.THECOMMENT"
        lines = f.read()
        try:
            first_line = lines.split("\n", 1)[0]
            first_line_dict = dict(zip(list(varz), list(first_line.split(","))))
            if len(first_line_dict["start_date"]) > 0 and len(first_line_dict["expiration_date"]) > 0:
                dates = two_header_for_mp_file[1] + two_header_for_mp_file[2]
            elif len(first_line_dict["start_date"]) > 0:
                dates = two_header_for_mp_file[1]
            elif len(first_line_dict["expiration_date"]) > 0:
                dates = two_header_for_mp_file[2]
            else:
                dates = ""
            two_header_for_mp_file = two_header_for_mp_file[0]+dates+two_header_for_mp_file[3]
            append_file.write(header_for_mp_file + "\n")
            append_file.write(two_header_for_mp_file + "\n")
        except Exception as e:
            error_file.write(
                "\nbadly formatted input file "
                + re.sub(r'\W+','',str(f).split(",")[0])
                + " with error "
                + str(e)
                + "\n"
            )
            pass
        lines = lines.split("\n")[1:]
        for line in lines:
            andrewid = line.split(",")[0]
            if bool(re.match("[a-z{1,10}]", userid)):
                try:
                    if "@" in andrewid:
                        userid = userid.split("@")[0]
                    else:
                        userid = userid.strip()
                    url = "https://{}/robhauswebservice/api/excel/pik/{}?username={}".format(
                        secrets_server, userid, username
                    )
                    response = requests.get(get_url)
                    out_string = (
                        "A|"
                        + response
                        + "|"
                        + "|".join(list(filter(None, first_line_dict.values())))
                        + "\n"
                    )
                    append_file.write(out_string)
                except Exception as e:
                    error_file.write(" bad user id " + andrewid + ",")
                    pass
            elif bool(re.match("[0-9{9}]", andrewid)):
                response = andrewid
                out_string = (
                        "A|"
                        + response
                        + "|"
                        + "|".join(list(filter(None, first_line_dict.values())))
                        + "\n"
                )
                append_file.write(out_string)
            else:
                error_file.write(" bad user id " + andrewid + ",")
                pass
        try:
            error_file.write("\n")
            error_file.close()
        except:
            pass
