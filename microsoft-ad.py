from ldap3 import Server, Connection, ALL, NTLM, MODIFY_ADD,MODIFY_DELETE
import yaml
import os
import logging

path = os.environ["WORKDIR"]

try:
    with open(path + "/trigger_plugins/microsoft-ad/dnifconfig.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    domain = cfg['trigger_plugin']['AD_DOMAIN']
    loginun = cfg['trigger_plugin']['AD_USER']
    user_pass = cfg['trigger_plugin']['AD_USER_PASS']
    server = cfg['trigger_plugin']['AD_SERVER']

    # user_cn = cfg['trigger_plugin']['AD_USER_CN']
    # ad_grp_cn= cfg['trigger_plugin']['AD_GROUP_CN']
except Exception, e:
    logging.error("AD plugin error in reading dnifconfig.yml: {}".format(e))


def add_to_group(inward_array, var_array):
    for i in inward_array:
        if var_array[0] in i:
            sr = Server(server, port=636, use_ssl=True,get_info=ALL)
            conn = Connection(sr, user='{}\{}'.format(domain, loginun), password=user_pass, authentication=NTLM)
            if not conn.bind():
                logging.error("error %s" % conn.result)
            else:
                usrstring = str(i[var_array[0]]).replace("/n","")
                ad_grp_cn = str(i[var_array[1]]).replace("/n","")
                # adresult = addUsersInGroups(conn, [usrstring], [ad_grp_cn])
                adresult = conn.modify(ad_grp_cn, {'member': (MODIFY_ADD, [usrstring])})
                # print adresult
            if adresult == True:
                i["$ADGrpStatus"] = "User added to group on AD"
            if adresult == False:
                i["$ADGrpStatus"] = "User already added to group on AD or Doesn't Exist"
            conn.unbind()
    return inward_array


def remove_from_group(inward_array, var_array):
    for i in inward_array:
        if var_array[0] in i:
            sr = Server(server, port=636, use_ssl=True,get_info=ALL)
            conn = Connection(sr, user='{}\{}'.format(domain, loginun), password=user_pass, authentication=NTLM)
            if not conn.bind():
                logging.error("error %s" % conn.result)
            else:
                usrstring = str(i[var_array[0]]).replace("/n", "")
                ad_grp_cn = str(i[var_array[1]]).replace("/n", "")
                adresult = conn.modify( ad_grp_cn, {'member': (MODIFY_DELETE, [usrstring])})
                # adresult = RemovefromGroups(conn, [usrstring], [ad_grp_cn],fix)
            if adresult == True:
                i["$ADGrpStatus"] = "User removed from  group on AD"
            if adresult == False:
                i["$ADGrpStatus"] = "User already removed from group or Doesn't Exist"
            conn.unbind()
    return inward_array


def enable_user(inward_array, var_array):
    for i in inward_array:
        if var_array[0] in i:
            sr = Server(server, port=636, use_ssl=True,get_info=ALL)
            conn = Connection(sr, user='{}\{}'.format(domain, loginun), password=user_pass, authentication=NTLM)
            if not conn.bind():
                logging.error("error %s" % conn.result)
            else:
                usrstring = str(i[var_array[0]]).replace("/n", "")
                conn.modify(usrstring, {'userAccountControl': [('MODIFY_REPLACE', 512)]})
                c = conn.result
                i['$ADUserStatus'] = c['description']
            conn.unbind()
    return inward_array


def disable_user(inward_array, var_array):
    for i in inward_array:
        if var_array[0] in i:
            sr = Server(server, port=636, use_ssl=True,get_info=ALL)
            conn = Connection(sr, user='{}\{}'.format(domain, loginun), password=user_pass, authentication=NTLM)
            if not conn.bind():
                logging.error("error %s" % conn.result)
            else:
                usrstring = str(i[var_array[0]]).replace("/n", "")
                conn.modify(usrstring, {'userAccountControl': [('MODIFY_REPLACE', 2)]})
                c = conn.result
                i['$ADUserStatus'] = c['description']
            conn.unbind()
    return inward_array



