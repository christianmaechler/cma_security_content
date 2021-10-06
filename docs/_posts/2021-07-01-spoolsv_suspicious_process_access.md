---
title: "Spoolsv Suspicious Process Access"
excerpt: "Exploitation for Privilege Escalation"
categories:
  - Endpoint
last_modified_at: 2021-07-01
toc: true
tags:
  - TTP
  - T1068
  - Exploitation for Privilege Escalation
  - Privilege Escalation
  - Splunk Enterprise
  - Splunk Enterprise Security
  - Splunk Cloud
  - Endpoint
  - Exploitation
---



[Try in Splunk Security Cloud](https://www.splunk.com/en_us/cyber-security.html){: .btn .btn--success}

#### Description

This analytic identifies a suspicious behavior related to PrintNightmare, or CVE-2021-34527 previously (CVE-2021-1675),  to gain privilege escalation on the vulnerable machine. This exploit attacks a critical Windows Print Spooler Vulnerability to elevate privilege. This detection is to look for suspicious process access made by the spoolsv.exe that may related to the attack.

- **Type**: TTP
- **Product**: Splunk Enterprise, Splunk Enterprise Security, Splunk Cloud
- **Datamodel**: [Endpoint](https://docs.splunk.com/Documentation/CIM/latest/User/Endpoint)
- **Last Updated**: 2021-07-01
- **Author**: Mauricio Velazco, Michael Haag, Teoderick Contreras, Splunk
- **ID**: 799b606e-da81-11eb-93f8-acde48001122


#### ATT&CK

| ID          | Technique   | Tactic       |
| ----------- | ----------- |--------------|
| [T1068](https://attack.mitre.org/techniques/T1068/) | Exploitation for Privilege Escalation | Privilege Escalation |



#### Search

```
`sysmon` EventCode=10 SourceImage = "*\\spoolsv.exe" CallTrace = "*\\Windows\\system32\\spool\\DRIVERS\\x64\\*" TargetImage IN ("*\\rundll32.exe", "*\\spoolsv.exe") GrantedAccess = 0x1fffff 
| stats  count min(_time) as firstTime max(_time) as lastTime by Computer SourceImage TargetImage GrantedAccess CallTrace  EventCode ProcessID
| `security_content_ctime(firstTime)` 
| `security_content_ctime(lastTime)` 
| `spoolsv_suspicious_process_access_filter`
```

#### Associated Analytic Story
* [PrintNightmare CVE-2021-34527](/stories/printnightmare_cve-2021-34527)


#### How To Implement
To successfully implement this search, you need to be ingesting logs with process access event where SourceImage, TargetImage, GrantedAccess and CallTrace executions from your endpoints. If you are using Sysmon, you must have at least version 6.0.4 of the Sysmon TA. Tune and filter known instances of spoolsv.exe.

#### Required field
* _time
* SourceImage
* TargetImage
* GrantedAccess
* CallTrace
* EventCode


#### Kill Chain Phase
* Exploitation


#### Known False Positives
Unknown. Filter as needed.



#### RBA

| Risk Score  | Impact      | Confidence   | Message      |
| ----------- | ----------- |--------------|--------------|
| 72.0 | 80 | 90 | $SourceImage$ was GrantedAccess open access to $TargetImage$ on endpoint $Computer$. This behavior is suspicious and related to PrintNightmare. |



#### Reference

* [https://github.com/cube0x0/impacket/commit/73b9466c17761384ece11e1028ec6689abad6818](https://github.com/cube0x0/impacket/commit/73b9466c17761384ece11e1028ec6689abad6818)
* [https://blog.truesec.com/2021/06/30/fix-for-printnightmare-cve-2021-1675-exploit-to-keep-your-print-servers-running-while-a-patch-is-not-available/](https://blog.truesec.com/2021/06/30/fix-for-printnightmare-cve-2021-1675-exploit-to-keep-your-print-servers-running-while-a-patch-is-not-available/)
* [https://blog.truesec.com/2021/06/30/exploitable-critical-rce-vulnerability-allows-regular-users-to-fully-compromise-active-directory-printnightmare-cve-2021-1675/](https://blog.truesec.com/2021/06/30/exploitable-critical-rce-vulnerability-allows-regular-users-to-fully-compromise-active-directory-printnightmare-cve-2021-1675/)
* [https://www.reddit.com/r/msp/comments/ob6y02/critical_vulnerability_printnightmare_exposes](https://www.reddit.com/r/msp/comments/ob6y02/critical_vulnerability_printnightmare_exposes)



#### Test Dataset
Replay any dataset to Splunk Enterprise by using our [`replay.py`](https://github.com/splunk/attack_data#using-replaypy) tool or the [UI](https://github.com/splunk/attack_data#using-ui).
Alternatively you can replay a dataset into a [Splunk Attack Range](https://github.com/splunk/attack_range#replay-dumps-into-attack-range-splunk-server)

* [https://media.githubusercontent.com/media/splunk/attack_data/master/datasets/attack_techniques/T1547.012/printnightmare/windows-sysmon.log](https://media.githubusercontent.com/media/splunk/attack_data/master/datasets/attack_techniques/T1547.012/printnightmare/windows-sysmon.log)



[*source*](https://github.com/splunk/security_content/tree/develop/detections/endpoint/spoolsv_suspicious_process_access.yml) \| *version*: **1**