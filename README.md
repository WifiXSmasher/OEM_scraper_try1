The code scrapes the oem site for cisco and gives the vulnerabilities of it
Used the explicit wait block the one in try and except to wait for the vulnerabilities to get updated from the database
it gives a lot of space between each vulnerability
fixing things - we need to clean the data a bit more 
                get more urls form different sites so that it can be scraped 
                scrape a url multiple times in a day





I am getting this output

AllAllCriticalHighMediumLowInformationalDone
Most Recent2024 Oct2024 Sep2024 Aug2024 Jul2024 Jun2024 May2024 Apr2024 Mar2024 Feb2024 Jan2023 Dec2023 Nov
Cisco Catalyst 9000 Series Switches Denial of Service VulnerabilityMediumCVE-2024-204342024 Oct 041.2CVE:CVE-2024-20434Publication ID:cisco-sa-vlan-dos-27Pur5RTVersion:1.2First Published:2024 Sep 25 16:00 GMTWorkaround:NoSummary:A vulnerability in Cisco IOS XE Software could allow an unauthenticated, adjacent attacker to cause a denial of service (DoS) condition on the control plane of an affected device.This vulnerability is due to improper handling of frames with VLAN tag information. An attacker couldRead More...
Cisco Catalyst 9000 Series Switches Denial of Service Vulnerability
Medium
CVE-2024-20434
2024 Oct 04
1.2
CVE:CVE-2024-20434Publication ID:cisco-sa-vlan-dos-27Pur5RTVersion:1.2First Published:2024 Sep 25 16:00 GMTWorkaround:NoSummary:A vulnerability in Cisco IOS XE Software could allow an unauthenticated, adjacent attacker to cause a denial of service (DoS) condition on the control plane of an affected device.This vulnerability is due to improper handling of frames with VLAN tag information. An attacker couldRead More...
Cisco Catalyst 9000 Series Switches Denial of Service Vulnerability
Medium
CVE-2024-20434
2024 Oct 04
1.2


this vulnerability is being displayed twice prefered output is this


CVE:CVE-2024-20434Publication ID:cisco-sa-vlan-dos-27Pur5RTVersion:1.2First Published:2024 Sep 25 16:00 GMTWorkaround:NoSummary:A vulnerability in Cisco IOS XE Software could allow an unauthenticated, adjacent attacker to cause a denial of service (DoS) condition on the control plane of an affected device.This vulnerability is due to improper handling of frames with VLAN tag information. An attacker couldRead More...
Cisco Catalyst 9000 Series Switches Denial of Service Vulnerability
Medium
CVE-2024-20434
2024 Oct 04
1.2



