#!/usr/bin/env python3
import sys, requests, time, json
from hashlib import md5

endpoint = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
sysconf = "http://{0}/cgi-bin/sysconf.cgi".format(endpoint)
infos = []
print("Using sysconf: ", sysconf, file=sys.stderr)

BAND_ARR={'40':'GSM_450','41':'GSM_480','42':'GSM_750','43':'GSM_850','44':'GSM_900_EXTENDED'
    ,'45':'GSM_900_PRIMARY','46':'GSM_900_RAILWAYS','47':'GSM_1800','48':'GSM_1900','80':'WCDMA_2100'
    ,'81':'WCDMA_PCS_1900','82':'WCDMA_DCS_1800','83':'WCDMA_1700_US','84':'WCDMA_850','85':'WCDMA_800'
    ,'86':'WCDMA_2600','87':'WCDMA_900','88':'WCDMA_1700_JAPAN','90':'WCDMA_1500_JAPAN','91':'WCDMA_850_JAPAN'
    ,'120':'LTE_BAND1','121':'LTE_BAND2','122':'LTE_BAND3','123':'LTE_BAND4','124':'LTE_BAND5'
    ,'125':'LTE_BAND6','126':'LTE_BAND7','127':'LTE_BAND8','128':'LTE_BAND9','129':'LTE_BAND10'
    ,'130':'LTE_BAND11','131':'LTE_BAND12','132':'LTE_BAND13','133':'LTE_BAND14','134':'LTE_BAND17'
    ,'135':'LTE_BAND33','136':'LTE_BAND34','137':'LTE_BAND35','138':'LTE_BAND36','139':'LTE_BAND37'
    ,'140':'LTE_BAND38','141':'LTE_BAND39','142':'LTE_BAND40','143':'LTE_BAND18','144':'LTE_BAND19'
    ,'145':'LTE_BAND20','146':'LTE_BAND21','147':'LTE_BAND24','148':'LTE_BAND25','149':'LTE_BAND41'           
    ,'150':'LTE_BAND42','151':'LTE_BAND43','152':'LTE_BAND23','153':'LTE_BAND26'
    ,'200':'TDSCDMA_BAND_A','201':'TDSCDMA_BAND_B','202':'TDSCDMA_BAND_C'
    ,'203':'TDSCDMA_BAND_D','204':'TDSCDMA_BAND_E','205':'TDSCDMA_BAND_F','0':'N/A','':'N/A'}

AUTH_TYPE = {"0": "NONE", "1": "PAP", "2": "PAP/CHAP"}


def get_sysconf(s: requests.session, page: str, act: str, params):
    return s.get(url=sysconf, params= dict({
        "page": page,
        "action": act
    }, **params), verify=False)

def post_sysconf(s: requests.session, page: str, act: str, params, data):
    return s.post(url=sysconf, params= dict({
        "page": page,
        "action": act
    }, **params), data=data, verify=False)

def get_sysconf_with_sid_header(s: requests.session, page: str, act: str, params):
    return s.get(url=sysconf, params= dict({
        "page": page,
        "action": act
    }, **params), verify=False, headers={
        "sid": s.cookies.get("sid")
    })

def login(s: requests.session, username: str, password: str):   
    check_code = md5("user_name={0}&user_check_code={1}".format(username,password).encode()).hexdigest()
    r = get_sysconf(s, "ajax.asp", "user_level_default_check", {
        "checkval": check_code,
        "user_name": username,
        "user_chdeck_code": password
    })
    if r.status_code < 200 or r.status_code > 299:
        print("Failed to login", file=sys.stderr)
        exit(1) 

    r = post_sysconf(s, "login.asp", "login", {}, {
        "user_name": username,
        "user_passwd": password
    })
    if r.status_code != 200:
        print("Failed to login", file=sys.stderr)
        exit(1)
    if s.cookies.get("userlevel") != '0':
        print("Failed to login (userlevel)", file=sys.stderr)
        exit(1)
    s.cookies.set("userlevel", "2")
    
def status_wan_info(s: requests.session):
    # Radio info
    # WMX info aren't parsed!
    r = get_sysconf_with_sid_header(s, "ajax.asp", "status_wanInfo", {})
    if r.status_code != 200:
        print("Failed wan info", file=sys.stderrs)
        return {}
    dat = r.text.split(";")
    general = dat[0].split("\t")
    wanInfo = dat[1].split("\t")
    updownLink = dat[2].split("\t")
    secondCellInfo = dat[3].split("\t")
    info = {}
    info["raw"] = {
        "text": r.text,
        "splitted": dat,
        "general": general,
        "wanInfo": wanInfo,
        "updownLink": updownLink,
        "secondCellInfo": secondCellInfo
    }
    info["network_status"] = general[1]
     
    info["unknown14"] = general[0]
    if general[1] == "5":
        info["network_status_text"] = "connected" 
    else:
        info["network_status_text"] = "connecting"
    info["ISP"] = general[2] 
    info["network_mode"] = general[3]
    info["scan_mode"] = general[4]
    if general[4] == "1":
        info["scan_mode_text"] = "lte"
    elif general[4] == "2":
        info["scan_mode_text"] = "3g"
    elif general[4] == "6":
        info["scan_mode_text"] = "wimax"
    info["connection_uptime_seconds"] = general[5]
    info["lte_RSSI"] = general[6]
    
    info["lte_mode"] = wanInfo[0]
    info["wan_status"] = wanInfo[1]
    if wanInfo[1] == "0":
        info["wan_status_text"] = "device_init"
    elif wanInfo[1] == "1":
        info["wan_status_text"] = "sim_detecting"
    elif wanInfo[1] == "2":
        info["wan_status_text"] = "device_ready"
    elif wanInfo[1] == "3":
        info["wan_status_text"] = "search"
    elif wanInfo[1] == "4":
        info["wan_status_text"] = "network_entry"
    elif wanInfo[1] == "5":
        info["wan_status_text"] = "attached"
    elif wanInfo[1] == "6":
        info["wan_status_text"] = "idle"
    elif wanInfo[1] == "7":
        info["wan_status_text"] = "no_signal"
    else:
        info["wan_status_text"] = "N/A"
    
    info["3g_band"] =  wanInfo[0]
    if wanInfo[0] in BAND_ARR:
        info["3g_band_text"] = BAND_ARR[wanInfo[0]]
    else:
        info["3g_band_text"] = "not_supported"
    info["2g_band"] =  wanInfo[0]
    if wanInfo[0] in BAND_ARR:
        info["2g_band_text"] = BAND_ARR[wanInfo[0]]
    else:
        info["2g_band_text"] = "not_supported"


    info["lte_qualcomn_band"] = wanInfo[1]
    if wanInfo[1] in BAND_ARR:
        info["lte_qualcomn_band_text"] = BAND_ARR[wanInfo[1]]
    else:
        info["lte_qualcomn_band_text"] = "not_supported"
    info["3g_uarfcn"] = wanInfo[1]
    info["2g_arfcn"] = wanInfo[1]
    info["lte_sequans_dl_frequency"] = wanInfo[2]
    info["lte_qualcomn_earfcn"] = wanInfo[2]
    info["3g_RSSI"] = wanInfo[2]
    info["2g_RSSI"] = wanInfo[2]
    info["lte_sequans_up_frequency"] = wanInfo[3]
    info["lte_qualcomn_RSSI"] = wanInfo[3]
    info["3g_ecio"] = wanInfo[3]
    info["2g_cell_id"] = wanInfo[3]
    info["wimax_RSSI"] = wanInfo[4]
    info["lte_qualcomn_RSRP"] = wanInfo[4]
    info["lte_sequans_bandwidth"] = wanInfo[4]
    info["3g_cell_id"] = wanInfo[4]
    info["2g_PLMN_id"] = wanInfo[4]
    info["lte_sequans_RSRP0"] = wanInfo[5]
    info["lte_qualcomn_RSRQ"] = wanInfo[5]
    info["lte_RSRP"] = wanInfo[5]
    info["3g_PLMN_id"] = wanInfo[5]
    info["2g_in_roaming"] = wanInfo[5]
    info["lte_sequans_RSRP1"] = wanInfo[6]
    info["lte_RSRP1"] = wanInfo[6]
    info["lte_qualcomn_SNR"] = wanInfo[6]
    info["3g_in_roaming"] = wanInfo[6]
    info["lte_sequans_RSRQ"] = wanInfo[7]
    info["lte_qualcomn_cellid"] = wanInfo[7]
    info["lte_RSRQ"] = wanInfo[7]
    info["3g_RSCP"] = wanInfo[7]
    info["lte_sequans_CINR0"] = wanInfo[8]
    info["lte_qualcomn_PLMNID"] = wanInfo[8]
    info["lte_CINR0"] = wanInfo[8]
    info["lte_sequans_CINR1"] = wanInfo[9]
    info["lte_qualcomn_in_roaming"] = wanInfo[9]
    info["lte_CINR1"] = wanInfo[9]
    info["lte_sequans_TX_power"] = wanInfo[10]
    info["lte_sequans_PCI"] = wanInfo[11]
    info["lte_sequans_cell_id"] = wanInfo[12]
    info["unknown7"] = wanInfo[13]
    info["unknown8"] = wanInfo[14]
    info["lte_sequans_RSRP"] = wanInfo[15]
    info["lte_sequans_SINR"] = wanInfo[16]
    info["lte_sequans_enodeb"] = wanInfo[17]
    info["lte_sequans_PLMN_ID"] = wanInfo[18]
    info["PLMN_ID"] = wanInfo[18]
    info["unknown13"] = wanInfo[19]
    info["lte_sequans_SINR0"] = wanInfo[20]
    info["lte_SINR0"] = wanInfo[20]
    info["lte_sequans_SINR1"] = wanInfo[21]
    info["lte_SINR1"] = wanInfo[21]
    info["lte_3g_2g_uplink_data_rate"] = updownLink[0]
    info["lte_3g_2g_uplink_txbytes"] = updownLink[1]
    info["lte_3g_2g_uplink_packets"] = updownLink[2]
    info["lte_3g_2g_downlink_data_rate"] = updownLink[3]
    info["lte_3g_2g_downlink_rxbytes"] = updownLink[4]
    info["lte_3g_2g_downlink_packets"] = updownLink[5]
    info["second_cells_info_length"] = secondCellInfo[0]
    info["second_cells_info"] = []
    for i in range(int(secondCellInfo[0])):
        raw = secondCellInfo[i+1].split(",")
        infos["second_cells_info"].append({
            "lte_plmn_index": i,
            "earfcn": raw[0],
            "PCI": raw[1],
            "RSRP_dBm": raw[2],
            "RSRQ_dB": raw[3],
            "CINR_dB": raw[4],
            "wmxch_active": raw[5],
        })
    info["wimax_CINR"] = "???"
    info["wimax_CINR1"] = "???"
    info["wimax_CINR3"] = "???"
    return info

def get_top_status_lte_wimax(s: requests.session):
    # Radio info
    r = get_sysconf_with_sid_header(s, "ajax.asp", "get_top_status_lte_wimax", {})
    # print(r.text)
    if r.status_code != 200:
        print("Failed top status lte wimax", file=sys.stderr)
        return {}
    dat = r.text.split("\t")
    info = {}
    info["raw"] = {
        "text": r.text,
        "splitted": dat,
    }
    info["lte_CINR"] = dat[1]
    info["cid"] = dat[2]
    info["cm_server_state"] = dat[3]
    info["sim_presence"] = dat[4]
    info["sim_pin_status"] = dat[5]
    info["current_scan_mode"] = dat[6]
    info["wimax_status_net_state"] = dat[7]
    info["wimax_cinr"] = dat[8]
    info["fw_version"] = dat[9] 

    return info

def get_signal_strength(s: requests.session):
    r = get_sysconf_with_sid_header(s, "ajax.asp", "status_Signal_Strength", {})
    if r.status_code != 200:
        print("Failed signal strength", file=sys.stderr)
        return {}
    dat = r.text.split("\t")
    info = {
        "raw": {
            "text": r.text,
            "splitted": dat,
        },
        "signal_strength_dBm": dat[1],
        "link_quality_dB": dat[2]
    }

    return info

def get_pdn_info(s: requests.session):
    r = get_sysconf_with_sid_header(s, "ajax.asp", "status_pdnInfor", {})
    if r.status_code != 200:
        print("Failed pdn info", file=sys.stderr)
        return {}
    dat = r.text.split("\t")
    default_pdn = dat[1].split(";")
    
    info = {}  
    info["raw"] = {
        "text": r.text,
        "splitted": dat,
    }
    info["default_apn_ipmode"] = default_pdn[4].split(",")[0]
    if info["default_apn_ipmode"] == "0":
        info["default_apn_ipmode_text"] = "none"
    elif info["default_apn_ipmode"] == "1":
        info["default_apn_ipmode_text"] = "ipv4"
    elif info["default_apn_ipmode"] == "2":
        info["default_apn_ipmode_text"] = "ipv6"
    elif info["default_apn_ipmode"] == "3":
        info["default_apn_ipmode_text"] = "ipv4+ipv6"
    info["default_apn_name"] = default_pdn[4].split(",")[1]
    info["default_apn_ipaddr4"] = default_pdn[4].split(",")[2]
    info["default_apn_ipaddr6"] = default_pdn[4].split(",")[3]
    info["default_pdn_type"] = default_pdn[0]
    if info["default_pdn_type"] == "0":
        info["default_pdn_type_text"] = "none"
    elif info["default_pdn_type"] == "1":
        info["default_pdn_type_text"] = "ipv4"
    elif info["default_pdn_type"] == "2":
        info["default_pdn_type_text"] = "ipv6"
    elif info["default_pdn_type"] == "3":
        info["default_pdn_type_text"] = "ipv4+ipv6"
    info["default_pdn_auth_type"] = default_pdn[2]
    info["default_pdn_auth_type_text"] = AUTH_TYPE[default_pdn[2]]
    info["default_pdn_connected"] = default_pdn[3]
    
    info["apn_name"] = default_pdn[4].split(",")[1]
    info["pdn_numbers"] = int(dat[2])
    list_pdn = dat[3].split(";")
    list_rule = dat[4].split(";")
    list_auth = dat[5].split(";")
    list_connect = dat[6].split(";")
    info["pdns"] = []
    for i in range(info["pdn_numbers"]):
        apn = {
            "apn_name": list_pdn[i].split(",")[1],
            "apn_ipv4": list_pdn[i].split(",")[2],
            "apn_ipv6": list_pdn[i].split(",")[3],
            "pdn_type": list_rule[i].split(",")[1],
            "auth_type": list_auth[i].split(",")[1],  
            "connected": list_connect[i]
        }
        apn["auth_type_text"] = AUTH_TYPE[apn["auth_type"]]
        if apn["pdn_type"] == "0":
            apn["pdn_type_text"] = "none"
        elif apn["pdn_type"] == "1":
            apn["pdn_type_text"] = "ipv4"
        elif apn["pdn_type"] == "2":
            apn["pdn_type_text"] = "ipv6"
        elif apn["pdn_type"] == "3":
            apn["pdn_type_text"] = "ipv4+ipv6"
        apn["pdns"].append(apn)


    #dat = r.text.split("\t")
    
    return info

def get_chip(s: requests.session):
    r = get_sysconf_with_sid_header(s, "ajax.asp", "get_chip", {})
    if r.status_code != 200:
        print("Failed radio info", file=sys.stderr)
        return {}
    return r.text

s = requests.Session()
login(s, username, password)

while True:
    info = {}
    time.sleep(0.5)
    print("Fetching data...", file=sys.stderr)
    info["time_epoch"] = time.time()
    info["status_wan_info"] = status_wan_info(s)
    info["top_status_lte_wimax"] = get_top_status_lte_wimax(s)
    info["signal_status"] = get_signal_strength(s)
    info["pdn_info"] = get_pdn_info(s)
    info["chip"] = get_chip(s)
    json.dump(info, sys.stdout)
    break
print("")
exit(0)