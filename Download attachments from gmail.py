import imaplib
import email
import os

#variables 
username = 'YOUR_GMAIL_ADDRESS'
password = 'YOUR_APP_PASSWORD' 
download_folder = 'YOUR_DIRECTORY_TO_DOWNLOAD_FILES'
imap_url ='imap.gmail.com'
label = 'downloaded' #Label to mark emails once downloaded

# search email for a key value pair
def search(key, value, my_mail):
    data = my_mail.search(key, '"{}"'.format(value))
    return data

# get list of emails under key value pair 
def get_emails(result_bytes):
	msgs = [] # all the email data are pushed inside an array
	for num in result_bytes[0].split():
		typ, data = my_mail.fetch(num, '(RFC822)')
		msgs.append(data)
	return msgs

# connect to server
my_mail = imaplib.IMAP4_SSL(imap_url)
my_mail.login(username, password)
my_mail.select('Inbox') #can change to '[Gmail]/All Mail' or '[Gmail]/Sent Mail' depending on what folder you want to search 

# search for emails from specific address 
msgs = get_emails(search('FROM', "name@email.com", my_mail)) 
mail_ids = msgs[1]
id_list = mail_ids[0].split(b' ')  
first_email_id = int(id_list[0])
latest_email_id = int(id_list[-1]) 

for i in range(latest_email_id,first_email_id, -1):
     data = my_mail.fetch(str(i), '(RFC822)' )
     for response_part in data:
        arr = response_part[0]
        if isinstance(arr, tuple):
            msg = email.message_from_bytes(arr[1])   
            email_subject = msg['subject']
            index = (msg['from']).find('<')
            email_from = (msg['from'])[0:index]
            email_date =  msg['Date']

            # print list of emails that were accessed
            if 'name' in email_from: #if email is from specific sender - can change to another identifier like 'subject' in email_subject 
                print('From : ' + email_from)
                print('Subject : ' + email_subject)
                print('Date: ' + email_date + '\n')

            # walk through the email parts to find emails with attachments - each attachment must have a different name or it will be overwritten
            for part in msgs.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                fileName = part.get_filename()
                
                # place label on all downloaded emails
                for uid in msgs: 
                    my_mail.store(str(i), '+X-GM-LABELS', label)
                                
                if bool(fileName):
                    filePath = os.path.join(download_folder, fileName)
                    if not os.path.isfile(filePath) :
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()

#close connection
my_mail.close()
my_mail.logout()