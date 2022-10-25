# IBM Watson IOT Platform
# pip install wiotp-sdk
import cv2
import os
from pyzbar.pyzbar import decode
from PIL import Image
import wiotp.sdk.device
import time
from ibmcloudant.cloudant_v1 import CloudantV1
from ibmcloudant.cloudant_v1 import Document, CloudantV1
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator

data0 = {}
a = 0
data1 = ""
id1 = ""
rev1 = ""
count = 0
myConfig = {
    "identity": {
        "orgId": "p3cru2",
        "typeId": "IOT217",
        "deviceId": "20485A0217"
    },
    "auth": {
        "token": "VI-LazC6B)g(*6Zvwx"
    }
}
a = ""


def qr_reader(a):
    r = ""
    if a != "":
        camera = cv2.VideoCapture(0)
        for i in range(1):
            return_value, image = camera.read()
            cv2.imwrite('opencv' + str(i) + '.png', image)
            del (camera)
        for i in range(1):
            a = 'opencv' + str(i) + '.png'
            d = decode(Image.open(a))
            r = (d[0].data.decode("ascii"))
            a = ""
            return r
        os.remove(a)

    # if(os.listdir("C:\\Users\\praka\\OneDrive\\Desktop\\generator\\opencv0.png")


def scanner(a):
    data1 = qr_reader(a)
    myData = {'Product_Id': data1, 'Add': "IN"}

    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)
    # client.commandCallback = myCommandCallback
    time.sleep(1)


# client.disconnect()
def scanner1(a):
    data1 = qr_reader(a)
    myData = {'Product_Id': data1, 'Out': "OUT"}

    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)
    # client.commandCallback = myCommandCallback
    time.sleep(1)


# client.disconnect()
def doc_rem(id1, rev1):
    authenticator = BasicAuthenticator('apikey-v2-19escfsu0s4deq1e18q4uixkd2u0ljzshmhkkwk1u4by',
                                       '5125c184e1bff7a2cbb49280735e6164')
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(
        'https://apikey-v2-19escfsu0s4deq1e18q4uixkd2u0ljzshmhkkwk1u4by:5125c184e1bff7a2cbb49280735e6164@1845b684-e63a-486c-9fcb-22a580750cd8-bluemix.cloudantnosqldb.appdomain.cloud')
    response = service.delete_document(
        db='inventory_management',
        doc_id=id1,
        rev=rev1
    ).get_result()
    # print(response)


def getData():
    authenticator = BasicAuthenticator('apikey-v2-19escfsu0s4deq1e18q4uixkd2u0ljzshmhkkwk1u4by',
                                       '5125c184e1bff7a2cbb49280735e6164')
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url('https://1845b684-e63a-486c-9fcb-22a580750cd8-bluemix.cloudant.com')
    response = service.post_all_docs(
        db='inventory_management',
        include_docs=True,
        limit=100
    ).get_result()
    with open("data.txt", 'r+') as f:
        f.truncate(0)
    for i in range(response['total_rows']):
        s = str(i + 1) + " " + (response['rows'][i]['doc']['payload']['data'])
        print(s)
        f = open("data.txt", "a")
        f.write(s + "\n")
        f.close()
        data0['data' + str(i)] = s
        mydata = {'d': data0}

    client.publishEvent(eventId="status", msgFormat="json", data=mydata, qos=0, onPublish=None)


def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m = cmd.data['command']
    a = m
    print(m)

    if a == "inn":
        print("Command :", m)
        scanner(a)
    elif a == "out":
        print("Command :", m)
        scanner1(a)
        # doc_rem()
    elif a == 'list':
        getData()
    elif (len(m[0]['_id']) >= 32):
        id1 = m[0]['_id']
        rev1 = m[0]['_rev']
        doc_rem(id1, rev1)
        


client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()
while True:
    client.commandCallback = myCommandCallback




