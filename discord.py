from discord_webhook import DiscordWebhook
url = 'https://discord.com/api/webhooks/783083064279433256/2pPEwQOdCJkwYP3DNGLDUn70nrZzYV-J5wDFD6B3dott3_8ttyoo99QnP0GLmAVRytPr'
webhook = DiscordWebhook(url=url, content='Test Message')
response = webhook.execute()
print(response)