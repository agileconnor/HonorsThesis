#!/usr/bin/python
'''
Usage:
  convert_nessus.py
  convert_nessus.py --out=<target>
'''

from lxml import etree
import pprint
import sys
from docopt import docopt
import os

'''
Credit for this code below goes to Alexander Leonov from his
excellent Information Security Automation blog. The original
code can be found at this link:
https://avleonov.com/2020/03/09/parsing-nessus-v2-xml-reports-with-python/
This has been slightly modified for this project.
'''
def parse_xml(xml_content):
    vulnerabilities = dict()
    single_params = ["agent", "cvss3_base_score", "cvss3_temporal_score", "cvss3_temporal_vector", "cvss3_vector",
                     "cvss_base_score", "cvss_temporal_score", "cvss_temporal_vector", "cvss_vector", "description",
                     "exploit_available", "exploitability_ease", "exploited_by_nessus", "fname", "in_the_news",
                     "patch_publication_date", "plugin_modification_date", "plugin_name", "plugin_publication_date",
                     "plugin_type", "script_version", "see_also", "solution", "synopsis", "vuln_publication_date",
                     "compliance",
                     "{http://www.nessus.org/cm}compliance-check-id",
                     "{http://www.nessus.org/cm}compliance-check-name",
                     "{http://www.nessus.org/cm}audit-file",
                     "{http://www.nessus.org/cm}compliance-info",
                     "{http://www.nessus.org/cm}compliance-result",
                     "{http://www.nessus.org/cm}compliance-see-also"]
    p = etree.XMLParser(huge_tree=True)
    root = etree.fromstring(text=xml_content, parser=p)
    for block in root:
        if block.tag == "Report":
            for report_host in block:
                host_properties_dict = dict()
                for report_item in report_host:
                    if report_item.tag == "HostProperties":
                        for host_properties in report_item:
                            host_properties_dict[host_properties.attrib['name']] = host_properties.text
                for report_item in report_host:
                    if 'pluginName' in report_item.attrib:
                        vulner_struct = dict()
                        vulner_struct['port'] = report_item.attrib['port']
                        vulner_struct['pluginName'] = report_item.attrib['pluginName']
                        vulner_struct['pluginFamily'] = report_item.attrib['pluginFamily']
                        vulner_struct['pluginID'] = report_item.attrib['pluginID']
                        vulner_struct['svc_name'] = report_item.attrib['svc_name']
                        vulner_struct['protocol'] = report_item.attrib['protocol']
                        vulner_struct['severity'] = report_item.attrib['severity']
                        for param in report_item:
                            if param.tag == "risk_factor":
                                risk_factor = param.text
                                vulner_struct['host'] = report_host.attrib['name']
                                vulner_struct['riskFactor'] = risk_factor
                            elif param.tag == "plugin_output":
                                if not "plugin_output" in vulner_struct:
                                    vulner_struct["plugin_output"] = list()
                                if not param.text in vulner_struct["plugin_output"]:
                                    vulner_struct["plugin_output"].append(param.text)
                            else:
                                if not param.tag in single_params:
                                    if not param.tag in vulner_struct:
                                        vulner_struct[param.tag] = list()
                                    if not isinstance(vulner_struct[param.tag], list):
                                        vulner_struct[param.tag] = [vulner_struct[param.tag]]
                                    if not param.text in vulner_struct[param.tag]:
                                        vulner_struct[param.tag].append(param.text)
                                else:
                                    vulner_struct[param.tag] = param.text
                        for param in host_properties_dict:
                            vulner_struct[param] = host_properties_dict[param]
                        compliance_check_id = ""
                        if 'compliance' in vulner_struct:
                            if vulner_struct['compliance'] == 'true':
                                compliance_check_id = vulner_struct['{http://www.nessus.org/cm}compliance-check-id']
                        if compliance_check_id == "":
                            vulner_id = vulner_struct['host'] + "|" + vulner_struct['port'] + "|" + \
                                        vulner_struct['protocol'] + "|" + vulner_struct['pluginID']
                        else:
                            vulner_id = vulner_struct['host'] + "|" + vulner_struct['port'] + "|" + \
                                        vulner_struct['protocol'] + "|" + vulner_struct['pluginID'] + "|" + \
                                        compliance_check_id
                        if not vulner_id in vulnerabilities:
                            vulnerabilities[vulner_id] = vulner_struct
    return(vulnerabilities)

if __name__ == '__main__':
    args = docopt(__doc__)
    dst = None
    if not args['--out']:
        print('Using stdout')
    else:
        dst = True
        cwd = os.path.dirname(__file__)
        abs_file_path = os.path.join(cwd, str(args['--out']))
        if os.path.isfile(abs_file_path):
            print('The file you wish to write to already exists. Would you like to overwrite it? Y/N')
            choice = str(raw_input())
            if choice == 'Y' or choice == 'y':
                print('File overwrite confirmed. Continuing')
                os.remove(abs_file_path)
            elif choice == 'N' or choice == 'n':
                print('File will not be overwritten. Please rerun with a different input path.')
                sys.exit(0)
            else:
                print('Invalid response. Aborting')
                sys.exit(0)
    pp = pprint.PrettyPrinter(indent=4)
    # read in file path
    file_path = '/home/legion/Desktop/First_Scan_n6d9av.nessus'
    #file_path = '/'
    f = open(file_path, 'r')
    xml_content = f.read()
    f.close()
    vulns = parse_xml(xml_content)

    # sort vulnerabilities by device
    ids = vulns.keys()
    device_dict = dict()
    ip_vuln_dict = dict()
    for id in ids:
        ip, _, ptype, plugin = id.split('|')
        if ip not in device_dict.keys():
            device_dict[ip] = dict()
            ip_vuln_dict[ip] = []
        device_dict[ip][plugin] = vulns[id]
    
    # setup config file
    config = ''
    config += str(len(device_dict.keys()))+" 1\n"
    for ip in device_dict.keys():
        for plugin in device_dict[ip].keys():
            if int(device_dict[ip][plugin]['severity']) > 0:
                if 'SMTP' in device_dict[ip][plugin]['pluginFamily'] or 'SMTP' in device_dict[ip][plugin]['pluginName']:
                    if 'SMTP' not in ip_vuln_dict[ip]:
                        ip_vuln_dict[ip].append('SMTP')
                elif 'FTP' in device_dict[ip][plugin]['pluginFamily'] or 'FTP' in device_dict[ip][plugin]['pluginName']:
                    if 'FTP' not in ip_vuln_dict[ip]:
                        ip_vuln_dict[ip].append('FTP')
                elif 'SQL' in device_dict[ip][plugin]['pluginFamily'] or 'SQL' in device_dict[ip][plugin]['pluginName']:
                    if 'SQL' not in ip_vuln_dict[ip]:
                        ip_vuln_dict[ip].append('SQL')
                elif 'VNC' in device_dict[ip][plugin]['pluginFamily'] or 'VNC' in device_dict[ip][plugin]['pluginName']:
                    if 'VNC' not in ip_vuln_dict[ip]:
                        ip_vuln_dict[ip].append('VNC')
                '''
                print(str(ip)+'|'+str(plugin))
                print(device_dict[ip][plugin]['pluginFamily'])
                print(device_dict[ip][plugin]['pluginName'])
                print(device_dict[ip][plugin]['port'])
                print(device_dict[ip][plugin]['protocol'])
                print(device_dict[ip][plugin]['riskFactor'])
                print(device_dict[ip][plugin]['severity'])
                print('------------------------------')
                '''

    '''
    class NetNodeType:
        ACCESSIBLE = 0
        SQL_VULN = 1
        FTP_VULN = 2
        SMTP_VULN = 3
        VNC_VULN = 4
        SQL_FTP = 5
        SQL_SMTP = 6
        SQL_VNC = 7
        FTP_SMTP = 8
        FTP_VNC = 9
        SMTP_VNC = 10
        SQL_FTP_SMTP = 11
        SQL_FTP_VNC = 12
        SQL_SMTP_VNC = 13
        FTP_SMTP_VNC = 14
        SQL_FTP_SMTP_VNC = 15
        ROOT = 16
        GOAL = 17
    '''
    config += 'Node Type\n'
    for ip in ip_vuln_dict.keys():
        config += str(ip)
        if 'SQL' in ip_vuln_dict[ip]:
            if 'FTP' in ip_vuln_dict[ip]:
                if 'SMTP' in ip_vuln_dict[ip]:
                    if 'VNC' in ip_vuln_dict[ip]:
                        #SQL_FTP_SMTP_VNC
                        config += ':15\n'
                    else:
                        #SQL_FTP_SMTP
                        config += ':11\n'
                elif 'VNC' in ip_vuln_dict[ip]:
                    #SQL_FTP_VNC
                    config += ':12\n'
                else:
                    #SQL_FTP
                    config += ':5\n'
            elif 'SMTP' in ip_vuln_dict[ip]:
                if 'VNC' in ip_vuln_dict[ip]:
                    #SQL_SMTP_VNC
                    config += ':13\n'
                else:
                    #SQL_SMTP
                    config+= ':6\n'
            elif 'VNC' in ip_vuln_dict[ip]:
                #SQL_VNC
                config += ':7\n'
            else:
                #SQL_VULN
                config+= ':1\n'
        elif 'FTP' in ip_vuln_dict[ip]:
            if 'SMTP' in ip_vuln_dict[ip]:
                if 'VNC' in ip_vuln_dict[ip]:
                    #FTP_SMTP_VNC
                    config += ':14\n'
                else:
                    #FTP_SMTP
                    config += ':8\n'
            elif 'VNC' in ip_vuln_dict[ip]:
                #FTP_VNC
                config += ':9\n'
            else:
                #FTP_VULN
                config += ':2\n'
        elif 'SMTP' in ip_vuln_dict[ip]:
            if 'VNC' in ip_vuln_dict[ip]:
                #SMTP_VNC
                config += ':10\n'
            else:
                #SMTP_VULN
                config += ':3\n'
        elif 'VNC' in ip_vuln_dict[ip]:
            #VNC_VULN
            config += ':4\n'
        else:
            config += ':0\n'
        
        '''
        # potentially reusable code here from when
        # there were only 3 vulns (no VNC)
        if 'FTP' in ip_vuln_dict[ip]:
            if 'SMTP' in ip_vuln_dict[ip]:
                if 'SQL' in ip_vuln_dict[ip]:
                    config += ':7\n'
                else:
                    config += ':6\n'
            elif 'SQL' in ip_vuln_dict[ip]:
                config += ':4\n'
            else:
                config += ':2\n'
        elif 'SMTP' in ip_vuln_dict[ip]:
            if 'SQL' in ip_vuln_dict[ip]:
                config += ':5\n'
            else:
                config += ':3\n'
        elif 'SQL' in ip_vuln_dict[ip]:
            config += ':1\n'
        else:
            config += ':0\n'
        '''
        
    config += 'Adjacency\n'
    for ip in ip_vuln_dict.keys():
        config += str(ip)
        for ip2 in ip_vuln_dict.keys():
            if ip2 == ip:
                continue
            config += ' ' + str(ip2)
        config += '\n'
    config += 'end'
    if not dst:
        print(config)
    else:
        with open(abs_file_path, 'w') as f:
            f.write(config)
