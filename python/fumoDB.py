from pymongo import MongoClient
import requests

from fumo import FumoItem, FumoAuctionItem

_PASSWORD = 'HskVtFvFpvHxOWOK'


client = MongoClient(f'mongodb+srv://noodlebot:{_PASSWORD}@cluster0.36l2o.mongodb.net/fumoApp?retryWrites=true&w=majority')
db = client.fumoApp
collection = db.fumos

def dropFumoData():
    collection.drop()              # Dropping collection to update all, since there could price changes. or ones taken off the market

def updateFumoDB(fumoItems, isAuction):                               
    for n, fumo in enumerate(fumoItems):
        item = {
            'title'         : fumo.title,
            'fumoType'      : fumo.fumoType,
            'price'         : fumo.price,
            'buyoutPrice'   : fumo.buyoutPrice if isAuction else 0,
            'buyLink'       : fumo.buyLink,
            'imgLink'       : fumo.imgLink,
            'isAuction'     : type(fumo) is FumoAuctionItem
        }

        result = collection.insert_one(item)

        print(f'Added {n+1} of {len(fumoItems)} fumos ({fumo.fumoType} fumo)')
    
    print('Finished adding fumos')


if __name__ == '__main__':
    pass
    # reimus = db.fumoData.find({'fumoType': 'Reimu'})
    # for reimu in reimus:
    #     print(reimu['title'])
    #     print(reimu['buyLink'])
    #     print()

    # db.fumoData.rename('fumos', dropTarget=False)