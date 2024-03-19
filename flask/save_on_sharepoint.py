username = 'JanPoglod@rabyte21.onmicrosoft.com'
password =  '(blured)' 

site_url = "blured"


from py_topping.data_connection.sharepoint import da_tran_SP365

sp = da_tran_SP365(site_url = 'blured'
                   , client_id = 'blured'
                   , client_secret = 'blured')

download_path = sp.create_link('blured')

sp.download(sharepoint_location = download_path 
            , local_location = './')


SPUrl = "blured"
username = BLURED
password =  BLURED
site = "blured" 

site_url = "https://rabyte21.sharepoint.com/Shared%20Documents/Forms/AllItems.aspx"
ctx = ClientContext(site_url).with_credentials(UserCredential("{username}", "{password}"))
file = ctx.web.get_file_by_guest_url(sharing_link_url).execute_query()

test_team_site_url = "blured"

username = BLURED
password =  BLURED

sharing_link_url = "blured"

file = ctx.web.get_file_by_guest_url(sharing_link_url).execute_query()
print(file.name)

url = "blured"
from py_topping.data_connection.sharepoint import da_tran_SP365

sp = da_tran_SP365(site_url = 'blured'
                   , client_id = 'blured'
                   , client_secret = 'blured')

download_path = sp.create_link(url)
sp.download(sharepoint_location = download_path 
            , local_location = './')

web = ctx.web
ctx.load(web)
ctx.execute_query()
print("Web site title: {0}".format(web.properties['Title']))
