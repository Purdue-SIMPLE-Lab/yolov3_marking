import time
import sys

def getTime(string,format,returnFormat):
    return time.strftime(returnFormat, time.strptime(string, format)) # Convert date and time to a nice printable format

def getLatLng(latString,lngString):
    if latString == "":
        return "Not", "Found"
    lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:])*1.0/60.0).lstrip("0.")
    lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:])*1.0/60.0).lstrip("0.")
    return lat,lng

def printRMC(lines):
    print("========================================RMC========================================")
    #print(lines, '\n')
    print("Fix taken at:", getTime(lines[1]+lines[9], "%H%M%S.%f%d%m%y", "%a %b %d %H:%M:%S %Y"), "UTC")
    print("Status (A=OK,V=KO):", lines[2])
    latlng = getLatLng(lines[3],lines[5])
    if latlng[0] == "Not":
        print("Lat,Long: Not Found")
    else:
        print("Lat,Long: ", latlng[0], lines[4], ", ", latlng[1], lines[6], sep='')
    print("Speed (knots):", lines[7])
    print("Track angle (deg):", lines[8])
    print("Magnetic variation: ", lines[10], end='')
    if len(lines) == 13: # The returned string will be either 12 or 13 - it will return 13 if NMEA standard used is above 2.3
        print(lines[11])
        print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):", lines[12].partition("*")[0])
    else:
        print(lines[11].partition("*")[0])

def parseRMC(lines):
    time_str = getTime(lines[1]+lines[9], "%H%M%S.%f%d%m%y", "%a %b %d %H:%M:%S %Y")
    lat = ""
    lng = ""
    latlng = getLatLng(lines[3],lines[5])
    if latlng[0] == "Not":
        lat = "Not Found"
        lng = "Not Found"
    else:
        lat = latlng[0] + lines[4]
        lng = latlng[1] + lines[6]

    return time_str, lat, lng

def checksum(line):
    checkString = line.partition("*")
    checksum = 0
    for c in checkString[0]:
        checksum ^= ord(c)

    try: # Just to make sure
        inputChecksum = int(checkString[2].rstrip(), 16)
    except:
        print("Error in string")
        return False

    if checksum == inputChecksum:
        return True
    else:
        print("=====================================================================================")
        print("===================================Checksum error!===================================")
        print("=====================================================================================")
        print(hex(checksum), "!=", hex(inputChecksum))
        return False

if __name__ == "__main__":
    filepath = 'G_2020_0413_1709_004.txt'
    fp = open(filepath)
    cnt = 0
    while cnt < 100:
        line = fp.readline()
        lines = line.split(",")
        cnt += 1

        t, la, lg = parseRMC(lines)
        print("Time: ", t, " Latitude: ", la, " Longitude: ", lg)
        pass
        # if checksum(line):
        #     printRMC(lines)
        #     pass