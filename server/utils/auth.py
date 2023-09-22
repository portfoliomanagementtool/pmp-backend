import jwt
try:
    pemfile = open(r"secrets/key.pem", 'r')
    keystring = pemfile.read()
    pemfile.close()
except Exception as e:
    import os
    print(os.getcwd())
    raise(SystemExit("Could Not Find the File : secrets/key.pem. Please Create secrets/key.pem based on secrets.example"))

    

def verify_token(token,user):
    if(user==None or token==None):
        return False
    try:
        tkn=token.split(" ")
        token=tkn[-1]
        payload = jwt.decode(token, keystring,algorithms=["RS256"], verify=True)
        return payload["sub"]==user
    except Exception as e:
        print("Error Occured",e)
        return False

if __name__=="__main__":
    ##This is just to test functions
    user=verify_token("eyJhbGciOiJSUzI1NiIsImtpZCI6Imluc18yVHcyZVNvMDNEcEFyNzVBMXNCaHd2VVhtcjgiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwOi8vbG9jYWxob3N0OjMwMDAiLCJleHAiOjE2OTI3NjMyODksImlhdCI6MTY5Mjc2MzIyOSwiaXNzIjoiaHR0cHM6Ly9idXJzdGluZy1zd2luZS02Ny5jbGVyay5hY2NvdW50cy5kZXYiLCJuYmYiOjE2OTI3NjMyMTksInNpZCI6InNlc3NfMlVNdUU5aUFsa05xdlJmWVBEZEI2RDQ2UXNkIiwic3ViIjoidXNlcl8yVU11NUkxNnVpS1RkM1hOMlNKc2Y3ano3M0gifQ.Y9DpPxW7OzWnUT0AQ5nqL0F_hHAoxyN0IguVf02qy1AaRYQUtSJZPlenPzULzRkEVvJILXGspeyp9lBAKq9Og6Z5EuMYDeKyb4mHWIAr-6DsCsbZ4TrlvQh_F2ZN6_VwteZeMCNhb2rvduPN3HsIkWyOEb1ncImessS0m7djfpFb8sZCi0zvCPufaeYhA-_4xOWX4J1S9cH3OHRIGXhobZoYTvUOTX62tLifwgmDz0DIdp_TM7OiOX5nDkFTo4fjQTyQGsMZLXC_pTw2nwtr53AwE9r7EMas4cn3Z1QJ01SWm9dCMWV-MynBFzqsCHk6n86LYdfvBOlpimumMEeV2g"
                      ,"user_2UMu5I16uiKTd3XN2SJsf7jz73H") 
    print(user)