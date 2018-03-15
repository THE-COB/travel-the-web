import smtplib

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("noreply.traveltheweb@gmail.com", "Mytraveltheweb321$")

message = "test message"
server.sendmail("noreply.traveltheweb@gmail.com", "rohanmathur01@gmail.com", message)
server.quit()