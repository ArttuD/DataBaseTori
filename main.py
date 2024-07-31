
from classes.server_manager import Server_Manager
from classes.dropbox_manager import DropBox

import argparse


#https://www.dropbox.com/developers/apps

#Donwload possiblee updates from dropbox

parser = argparse.ArgumentParser(
    description="""Download results in the folder and ouputs results
                """)
parser.add_argument('--token','-t',default=False,
                    help='access token')
parser.add_argument('--path','-p',required=False, default= 'bases/DataBase.db',
                    help='access token')
parser.add_argument('--init','-i',default=False,
                    help='access token')
parser.add_argument('--table','-ta',default=False,
                    help='access token')

args = parser.parse_known_args()[0]


if args.init:
    dropM = DropBox(args.token)
    succ = dropM.download_dropbox()
    dropM.download_dumps()

    if succ == -1:
        print("download failed")
        exit()

sever_host = Server_Manager(args.path, args.table, False)
#sever_host.vis_tables()
ret = sever_host.open_socket()
sever_host.wait_clients()
sever_host.close_socket()


#succ = sm.init_tables()

#if succ == -1:
#    print("table creation failed")
#

#dataM.close()

