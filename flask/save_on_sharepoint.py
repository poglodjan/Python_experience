username = 'JanPoglod@rabyte21.onmicrosoft.com'
password =  '(blur)' 

site_url = "https://rabyte21-admin.sharepoint.com/"


from py_topping.data_connection.sharepoint import da_tran_SP365

sp = da_tran_SP365(site_url = 'https://rabyte21.sharepoint.com'
                   , client_id = 'c842ca55-7bd9-4a84-aaab-30d92edea6bc'
                   , client_secret = 'lo/OoyNbekCZuHKogAKqcinFb0bj3KPi71ikJAMjn+E=')

download_path = sp.create_link('https://rabyte21.sharepoint.com/:x:/g/EeQRnxN8bHlKnWfRX-K7YY0BDpCLyoFV3fafK2eLpOKoEw?e=iixHUy')

sp.download(sharepoint_location = download_path 
            , local_location = './')


SPUrl = "https://rabyte21.sharepoint.com/"
username = 'JanPoglod@rabyte21.onmicrosoft.com'
password =  'Poker2022' 
site = "https://rabyte21.sharepoint.com/Shared%20Documents" 

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
site_url = "https://rabyte21.sharepoint.com/Shared%20Documents/Forms/AllItems.aspx"
ctx = ClientContext(site_url).with_credentials(UserCredential("{username}", "{password}"))
file = ctx.web.get_file_by_guest_url(sharing_link_url).execute_query()
#zz
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

test_team_site_url = "https://rabyte21.sharepoint.com/"

username = 'JanPoglod@rabyte21.onmicrosoft.com'
password =  'Poker2022' 

sharing_link_url = "https://rabyte21.sharepoint.com/:x:/g/EeQRnxN8bHlKnWfRX-K7YY0BDpCLyoFV3fafK2eLpOKoEw?e=BMVLvb"

ctx = ClientContext("https://rabyte21.sharepoint.com/Shared%20Documents").with_credentials(UserCredential("{username}", "{password}"))


file = ctx.web.get_file_by_guest_url(sharing_link_url).execute_query()
print(file.name)


url = "https://rabyte21.sharepoint.com/:x:/s/Development/EWyRWtS9SeVJrwWmIxqUeQYBMVpfxfa--q_lNeEQCEd2jA?e=9Mryzc"
from py_topping.data_connection.sharepoint import da_tran_SP365

sp = da_tran_SP365(site_url = 'https://rabyte21.sharepoint.com/sites/Development'
                   , client_id = '604278c3-62ed-4933-b939-ef4b8c8cebe2'
                   , client_secret = '+4+qFcyiKyUCW2qfsRGjmQhZf0al66etxTcoMk/3anw=')

download_path = sp.create_link(url)
sp.download(sharepoint_location = download_path 
            , local_location = './')

from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext

username = 'JanPoglod@rabyte21.onmicrosoft.com'
password =  'Poker2022' 

site_url = "https://rabyte21.sharepoint.com/"
client_id = "604278c3-62ed-4933-b939-ef4b8c8cebe2"
client_secret = "+4+qFcyiKyUCW2qfsRGjmQhZf0al66etxTcoMk/3anw="

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

root_url = "https://company.sharepoint.com"
full_url = "https://company.sharepoint.com/sites/Development/Shared%20Documents/sharepoint/test1.xlsx"

ctx = ClientContext(root_url)
ctx.with_user_credentials(username,password)

response = File.open_binary(ctx, full_url)
print(response.content)

client_id = "ae5e2ee7-9970-47e9-9faf-ad568695e3a4"
client_secret = "Bl+MxkszYiT0FwAK5kzXoFpNo1MMjpNloQOQEGNlgu0="

from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

credentials = ClientCredential(client_id, client_secret)
ctx = ClientContext(site_url).with_credentials(credentials)

web = ctx.web
ctx.load(web)
ctx.execute_query()
print("Web site title: {0}".format(web.properties['Title']))
