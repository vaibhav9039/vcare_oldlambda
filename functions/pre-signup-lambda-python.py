import boto3
import os


def lambda_handler(event, context):
    trigger_source = event['triggerSource']
    print("trigger_source==" + str(trigger_source))

    username = event['userName']
    user_data = event['request']['userAttributes']
    email = user_data.get('email')
    phone_number = user_data.get('phone_number')
    custom_group = user_data.get('custom:group')
    origin = user_data.get('custom:Origin')

    event['response']['autoConfirmUser'] = True

    print("Userdata===" + str(user_data))

    if 'email' in event['request']['userAttributes']:
        print("This is for Web")
        print("Email===" + str(email))
        event['response']['autoVerifyEmail'] = True
        event['response']['autoVerifyPhone'] = True

        if custom_group == "CustomerAdmin":
            print("custom_group===" + str(custom_group))

            with open('CustomerAdmin_template.html', 'r') as file:
                email_template = file.read()

            print("origin===" + str(origin))

            if str(origin) == "stage":
                password_link = os.environ.get('PASSWORD_LINK_STAGE')
                print("Password-Link===" + str(password_link + username))

                email_body = email_template.replace('{{username}}', username).replace('{{email}}', email).replace(
                    '{{LinK}}', str(password_link + username)).replace('{{Role}}', custom_group)
                ses_client = boto3.client('ses')

                # subject = 'Account Password Reset'
                subject = os.environ.get('EMAIL_SUBJECT')
                print("sender_email===" + str(subject))

                message = {
                    'Subject': {'Data': subject},
                    'Body': {
                        'Html': {
                            'Data': email_body
                        }
                    }
                }

                # sender_email = "aj@vcareit.dk"
                sender_email = os.environ.get('SENDER_EMAIL')
                print("sender_email===" + str(sender_email))

                recipient_email = f"{email}"

                response = ses_client.send_email(
                    Source=sender_email,
                    Destination={
                        'ToAddresses': [recipient_email]
                    },
                    Message=message
                )

                print("Response===" + str(response))
                print("EmailEvent===" + str(event))
                return event

            if str(origin) == "prod":
                password_link = os.environ.get('PASSWORD_LINK_PROD')
                print("Password-Link===" + str(password_link + username))

                email_body = email_template.replace('{{username}}', username).replace('{{email}}', email).replace(
                    '{{LinK}}', str(password_link + username)).replace('{{Role}}', custom_group)
                ses_client = boto3.client('ses')

                # subject = 'Account Password Reset'
                subject = os.environ.get('EMAIL_SUBJECT')
                print("sender_email===" + str(subject))

                message = {
                    'Subject': {'Data': subject},
                    'Body': {
                        'Html': {
                            'Data': email_body
                        }
                    }
                }

                # sender_email = "aj@vcareit.dk"
                sender_email = os.environ.get('SENDER_EMAIL')
                print("sender_email===" + str(sender_email))

                recipient_email = f"{email}"

                response = ses_client.send_email(
                    Source=sender_email,
                    Destination={
                        'ToAddresses': [recipient_email]
                    },
                    Message=message
                )

                print("Response===" + str(response))
                print("EmailEvent===" + str(event))
                return event

        if custom_group == "practitioner" or "nurse" or "auditor":
            print("custom_group===" + str(custom_group))

            with open('Practitioner_template.html', 'r') as file:
                email_template = file.read()

            print("origin===" + str(origin))
            if str(origin) == "stage":
                password_link = os.environ.get('PASSWORD_LINK_STAGE')
                print("Password-Link===" + str(password_link + username))
                email_body = email_template.replace('{{username}}', username).replace('{{email}}', email).replace(
                    '{{LinK}}',
                    str(password_link + username)).replace('{{Role}}', custom_group)
                ses_client = boto3.client('ses')

                subject = os.environ.get('EMAIL_SUBJECT')
                print("sender_email===" + str(subject))

                message = {
                    'Subject': {'Data': subject},
                    'Body': {
                        'Html': {
                            'Data': email_body
                        }
                    }
                }

                sender_email = os.environ.get('SENDER_EMAIL')
                print("sender_email===" + str(sender_email))

                recipient_email = f"{email}"

                response = ses_client.send_email(
                    Source=sender_email,
                    Destination={
                        'ToAddresses': [recipient_email]
                    },
                    Message=message
                )

                print("Response===" + str(response))
                print("EmailEvent===" + str(event))
                return event

            if str(origin) == "prod":
                password_link = os.environ.get('PASSWORD_LINK_PROD')
                print("Password-Link===" + str(password_link + username))

                email_body = email_template.replace('{{username}}', username).replace('{{email}}', email).replace(
                    '{{LinK}}',
                    str(password_link + username)).replace('{{Role}}', custom_group)
                ses_client = boto3.client('ses')

                subject = os.environ.get('EMAIL_SUBJECT')
                print("sender_email===" + str(subject))

                message = {
                    'Subject': {'Data': subject},
                    'Body': {
                        'Html': {
                            'Data': email_body
                        }
                    }
                }

                sender_email = os.environ.get('SENDER_EMAIL')
                print("sender_email===" + str(sender_email))

                recipient_email = f"{email}"

                response = ses_client.send_email(
                    Source=sender_email,
                    Destination={
                        'ToAddresses': [recipient_email]
                    },
                    Message=message
                )

                print("Response===" + str(response))
                print("EmailEvent===" + str(event))
                return event


    else:
        print("This is for Mobile App")
        print("Phone-No===" + str(phone_number))
        event['response']['autoVerifyPhone'] = True

        print("PhoneEvent===" + str(event))
        return event
