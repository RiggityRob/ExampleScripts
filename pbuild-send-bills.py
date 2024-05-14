# Import smtplib for the actual sending function
import smtplib
import os
import csv

# Here are the email package modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Create the outer email message.

sender = '"Gold Team" <gold-help@rob.haus>'
bcc = "archives@rob.haus"
cfy = "24"
nfy = "25"
ccost = "35"
ncost = "36.75"
# Change Percentage - this is not calculated so as to use whatever rounding we decide looks best
change = "1.05"

rows = []

with open("FY" + cfy + "Billing.csv", encoding="utf_8_sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rows.append(row)

e = 1
for row in rows:
    # Skip Housing Email
    # 	if (e == 42):
    # 		continue
    to = []
    erows = dict(row)
    print(erows)

    # Append up to three email address contacts to email sending list, comment out until ready for real sending
    for i in range(2):
        if f"CONTACT1EMAIL" in erows:
            email = erows[f"CONTACT{i+1}EMAIL"]
            name = erows[f"CONTACT{i+1}"]
            to.append(f'"{name}" <{email}>')
    dept = erows["DEPARTMENT"]
    print(dept)
    deptfilename = f"{dept.replace(': ','-')}.csv"
    # Override To header for testing
    # to = ['"Chris Nolin" <cnolin@andrew.cmu.edu>']

    # Generate EmailGroup/Department CSV
    with open(deptfilename, "a", newline="") as deptcsvfile:
        to = "|".join(to)
        deptwriter = csv.DictWriter(
            deptcsvfile,
            fieldnames=[
                "To",
                "Location",
                "Location Description",
                "Extra Description",
                "Group",
                "Group Description",
                "Oracle Charge String",
            ],
        )
        deptwriter.writerow(
            {
                "To": to,
                "Location": erows["LOCATION"],
                "Location Description": erows["LOCATION_DESCRIPTION"],
                "Extra Description": erows["NODE_DESCRIPTION"],
                "Group": erows["BILLING_GROUP_NAME"],
                "Group Description": erows["BILLING_GROUP_DESCRIPTION"],
                "Oracle Charge String": str(erows["CHARGE_FUNDING_SOURCE"])
                + str(erows["CHARGE_ACTIVITY"])
                + str(erows["CHARGE_FUNCTION"])
                + str(erows["CHARGE_ORG"])
                + str(erows["CHARGE_ENTITY"]),
            }
        )
directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        csv_path = os.path.join(directory, filename)
        with open(csv_path, "r") as f:
            reader = csv.reader(f)
            to = next(reader)[0]
            devices = sum(1 for _ in f)
        dept = str([filename])
        msg = MIMEMultipart("alternative")
        msg[
            "Subject"
        ] = f"{dept} FY{cfy}/{nfy} Charges for Physical Access Devices (CSGold)"
        msg["From"] = sender
        to = to.split("|")
        msg["To"] = ",".join(to)
        with open(csv_path, "r") as f:
            attachment = MIMEApplication(f.read())
            attachment.add_header(
                "Content-Disposition", "text/csv", filename="Billed Locations.csv"
            )
            msg.attach(attachment)

        # textfile='Billing.txt'
        # with open(textfile, 'rb') as fp:
        #    text = fp.read()
        htmlfile = "FY" + cfy + "Billing.html"
        with open(htmlfile, "rb") as fp:
            html = fp.read()

        tablerows = ""

        html = html.replace(b"{tablerows}", bytes(tablerows, "us-ascii"))
        html = html.replace(b"{cfy}", bytes(cfy, "us-ascii"))
        html = html.replace(b"{nfy}", bytes(nfy, "us-ascii"))
        html = html.replace(b"{ccost}", bytes(ccost, "us-ascii"))
        html = html.replace(b"{ncost}", bytes(ncost, "us-ascii"))
        html = html.replace(b"{change}", bytes(change, "us-ascii"))
        html = html.replace(b"{devices}", bytes(str(devices), "us-ascii"))
        html = html.replace(
            b"{ccost*devices}", bytes(str(float(ccost) * devices), "us-ascii")
        )
        html = html.replace(
            b"{ncost*devices}", bytes(str(float(ncost) * devices), "us-ascii")
        )

        # msg.attach(MIMEText(text, "plain", 'us-ascii'))
        msg.attach(MIMEText(html, "html", "us-ascii"))

        # Send the email via our own SMTP server.
        s = smtplib.SMTP("SECRET")
        # The below (usually commented) line is how you override the actual email send.  You can use this to see how every email looks before they actually get sent to customers.
        # s.sendmail(sender, "goodeve@rob.haus", msg.as_string())
        s.sendmail(sender, to + [bcc], msg.as_string())
        s.quit()
