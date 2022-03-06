import login
import utils
import jwtoken as jwt
import os

loginAttempts = 1
requiredToGenerateAccessToken = False
wfRunCounter = os.environ['wfRunCounter']
print("*** WOKFLOW RAN ", wfRunCounter , " TIMES SINCE ITS CREATION ***")
daysSinceAccessTokenGenerated = int(wfRunCounter)%30  # access token expires after some days [not sure when]. So re-generating it every 30 days
if daysSinceAccessTokenGenerated == 0:
    requiredToGenerateAccessToken = True
    print("*** IT'S BEEN 30 DAYS SINCE THE ACCESS TOKEN IS GENERATED. NEED TO RE-GENERATE ACCESS TOKEN ***")

generatePlaylist = True
while generatePlaylist:
    try:
        userDetails = jwt.getUserDetails()
    except FileNotFoundError:
        logged_in = "false"
    else:
        logged_in = userDetails["loggedIn"]

    print("Already Logged in? : " + logged_in)
    print("====================================")
    SID = os.environ['SID']
    RMN = os.environ['RMN']
    PASSWORD = os.environ['PASSWORD']
    
    if logged_in == "true" and not requiredToGenerateAccessToken:
            print("SID - {0} and\n Name - {1}".format(userDetails['sid'],userDetails['sName']))
            print("***********************")
            print("Please wait till the playlist is generated...")
            print("You may see a lot of lines being printed, you may ignore it")
            print("The generated m3u will be saved as tataSkyChannels.m3u")
            print("************************************")
            utils.m3ugen()
            print("Playlist generated")
            generatePlaylist = False
    else:
         if loginAttempts <= 2:
            login.loginWithPass(sid=SID, rmn=RMN, pwd=PASSWORD)
            requiredToGenerateAccessToken = False
            loginAttempts += 1
         else:
            print("Multiple Login attempts. check if all details available in userDetails.json file.")
            break