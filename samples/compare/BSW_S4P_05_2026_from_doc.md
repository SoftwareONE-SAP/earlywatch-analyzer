[IMAGE]
[SEPARATOR]
[SEPARATOR]
[IMAGE]
[IMAGE]
[SEPARATOR]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]
[IMAGE]

# 1 Service Summary

| [IMAGE] | This EarlyWatch Alert session detected issues that could potentially affect your system. Please evaluate the recommendations. |
| --- | --- |

Alert Overview

| [RED] | SAP HANA database: User SYSTEM is active and valid. |
| --- | --- |
| [RED] | Users with critical authorizations, which allow to do anything in client 000 |
| [RED] | Users with critical authorizations, which allow to do anything in other client(s) than 000 |
| [RED] | Users with critical authorizations, which should not be used in production in other client(s) than 000 |
| [YELLOW] | We found more than 30 ABAP dumps in your system. |
| [YELLOW] | SAP HANA database: Parameters are not set in accordance with the recommendation. |
| [YELLOW] | SAP HANA database: Consistency checks are scheduled without the global consistency check. |
| [YELLOW] | Readiness of your system for SAP Remote Service has not been verified by running report RTCCTOOL. |
| [YELLOW] | Secure password policy is not sufficiently enforced. |
| [YELLOW] | SAP HANA database: Users with critical privilege DATA ADMIN. |

**Hide and Snooze EarlyWatch Alerts:** To provide feedback on the alerts, please use the 'Hide and Snooze Alert' functionality in the [Solution Finder](https://me.sap.com/ewa/solutionfinder) . You can hide alerts if you consider them irrelevant or snooze them if the recommendations are already in implementation. The blog [Hide and Snooze SAP EarlyWatch Alerts](https://community.sap.com/t5/technology-blogs-by-sap/hide-snooze-sap-earlywatch-alerts/ba-p/13567920) explains how to use it and the required authorization "Manage Alert(s)" in SAP EarlyWatch Alert.

Note: If you send SAP EarlyWatch Alert data to SAP, this report can be viewed in ["SAP for Me"](https://me.sap.com/home) . One of the benefits of using [SAP EarlyWatch Alert Workspace](https://me.sap.com/ewa/workspace) is receiving proactive alerts that are calculated in the workspace only and are not available in a Solution Manager Do not miss any important findings: subscribe to notifications with just a few clicks on [Notification Activation](https://me.sap.com/ewa/notifications/subscribe) . For detailed configuration options, read this [Best Practices](https://blogs.sap.com/2022/11/29/best-practice-sap-earlywatch-alert/) blog.

How to get access to the SAP EarlyWatch Alert apps is explained in [SAP Note 2520319](https://me.sap.com/notes/2520319) . The following link to the [SAP EarlyWatch Alert Reports](https://me.sap.com/ewa/report/System/0021220331/S4P/000000000800631194) app always opens up the latest report for this system. Similarly, this link to the [SAP EarlyWatch Alert Dashboard](https://me.sap.com/ewa/dashboard/soopDetail/000000000800631194/0021220331/S4P) shows you the analytical dashboard for this system. Specific links to analytical detail pages in [SAP EarlyWatch Alert Workspace](https://me.sap.com/ewa/workspace) are included in the respective sections in this report.

The [SAP EarlyWatch Alert Status App](https://me.sap.com/ewa/status) is your entry point for analysis if you are missing the current data in SAP EarlyWatch Alert apps.

Based on these findings, it is recommended that you perform the following Guided Self-Services.

| Guided Self Service | FAQ SAP Note |
| --- | --- |
| Security Optimization Service | 1484124 |

For more information about Guided Self-Services, see [SAP Enterprise Support Academy](https://support.sap.com/support-programs-services/programs/enterprise-support/academy.html) . Academy -

Check Overview

| Topic Rating | Topic | Subtopic Rating | Subtopic |
| --- | --- | --- | --- |
| [YELLOW] | Service Data Quality and Service Readiness |  |  |
|  |  | [GREEN] | Sending EarlyWatch Alert of S4P to SAP Backbone |
|  |  | [GREEN] | Configuring S4P for SAP Note Assistant |
|  |  | [YELLOW] | Service Preparation of S4P |
| [YELLOW] | Software Configuration for S4P |  |  |
|  |  | [GREEN] | SAP Application Release - Maintenance Phases |
|  |  | [GREEN] | Maintenance and Update Strategy for SAP Fiori Front-End Server |
|  |  | [GREEN] | Security Risk Due to Outdated Support Packages * |
|  |  | [GREEN] | Database - Maintenance Phases |
|  |  | [GREEN] | Operating System(s) - Maintenance Phases |
|  |  | [YELLOW] | SAP Kernel Release |
|  |  | [GREEN] | HANA Database Version for H4P |
| [GREEN] | Hardware Capacity |  |  |
| [GREEN] | Workload Distribution S4P |  |  |
|  |  | [GREEN] | Workload by Application Module |
|  |  | [GREEN] | DB Load Profile |
| [GREEN] | Performance Overview S4P |  |  |
| [YELLOW] | SAP System Operating S4P |  |  |
|  |  | [GREEN] | Availability based on Collector Protocols |
|  |  | [YELLOW] | Program Errors (ABAP Dumps) |
|  |  | [GREEN] | Update Errors |
|  |  | [YELLOW] | Table Reorganization |
|  |  | [GREEN] | Critical Number Ranges |
| [RED] | Security |  |  |
|  |  | [GREEN] | System Recommendations (HANA) * |
|  |  | [GREEN] | Maintenance Status of current SAP HANA Database Revision * |
|  |  | [YELLOW] | SAP HANA System Privilege DATA ADMIN |
|  |  | [GREEN] | SAP HANA Password Policy * |
|  |  | [GREEN] | SAP HANA Audit Trail * |
|  |  | [GREEN] | SAP HANA SQL Trace Level * |
|  |  | [GREEN] | SAP HANA Network Settings for Internal Services * |
|  |  | [RED] | Activation Status and Validity of User SYSTEM |
|  |  | [GREEN] | System Recommendations (ABAP) * |
|  |  | [GREEN] | Age of Support Packages * |
|  |  | [GREEN] | Default Passwords of Standard Users * |
|  |  | [GREEN] | Control of the Automatic Login User SAP* * |
|  |  | [GREEN] | Protection of Passwords in Database Connections * |
|  |  | [YELLOW] | ABAP Password Policy |
|  |  | [GREEN] | RFC Gateway Security * |
|  |  | [GREEN] | Message Server Security * |
|  |  | [RED] | Critical authorizations, which allow to do anything |
|  |  | [RED] | Critical authorizations, which should not be used in production |
|  |  | [YELLOW] | Critical authorizations, which should only see very limited use in production |
| [YELLOW] | Software Change and Transport Management of S4P |  |  |
|  |  | [GREEN] | Number of Changes |
|  |  | [YELLOW] | Emergency Changes |
|  |  | [GREEN] | Failed Changes |
| [YELLOW] | Upgrade Planning |  |  |
|  |  | [YELLOW] | Compatibility Scope information in EarlyWatch Alert has been suspended |
| [YELLOW] | SAP HANA Database H4P |  |  |
|  |  | [YELLOW] | SAP HANA Stability and Alerts |
|  |  | [YELLOW] | SAP HANA Database Configuration |
|  |  | [GREEN] | SAP HANA Resource Consumption |
|  |  | [GREEN] | SAP HANA Workload and Performance |
|  |  | [GREEN] | Size and Growth |
|  |  | [YELLOW] | Administration |
| [YELLOW] | SAP NetWeaver Gateway |  |  |
|  |  | [GREEN] | MetaData Cache Activation |
|  |  | [GREEN] | Logging Configuration |
|  |  | [YELLOW] | Gateway Error Logs |
|  |  | [YELLOW] | Important Periodic Jobs |
| [YELLOW] | Fiori Checks for S4P |  |  |
|  |  | [GREEN] | SAP Fiori Cache Buster Activation |
|  |  | [GREEN] | HTTP/2 Support |
|  |  | [GREEN] | SAP Fiori Launchpad Performance - Home Page Mode |
|  |  | [YELLOW] | SAP Fiori Launchpad - Spaces and Pages adoption |
|  |  | [GREEN] | Activated but unused ICF services in UI5 apps |

*** Remark:** The check overview includes checks executed with a green result, which do not appear in the report.

**Note:** All recommendations in this report are based on our general experience. Test them before using them in your production system. Note that EarlyWatch Alert is an automatic service.

**Note:** If you have any questions</B> about the accuracy of the checks in this report or the correct configuration of the SAP EarlyWatch Alert service, create a customer case under component SV-SMG-SER-EWA.

**Note:** If you require any assistance in resolving concerns about your system performance or if you require a technical analysis of other aspects of your system as highlighted in the report, please follow the instructions below:

Create a case using the [Get Support application](https://me.sap.com/createIssue/0) in [SAP for Me](https://me.sap.com) ( [KBA 1296527](https://me.sap.com/notes/1296527) ). Contact one of the [administrators](https://me.sap.com/userscontacts/impcont) in your company if your S-user ID does not have the required authorizations.

Within case creation, select the system. From the menu, choose:

- *Product* : Customer Project-Based Solution

- *Component* : insert required component (for example, if you wish to open a case on the topic 'performance', please use component SV-PERF.)

If you need assistance, contact your local Customer Interaction Center (CIC) or SAP representative. Please refer to [SAP Note 560499](https://me.sap.com/notes/560499) . For information about how to set the appropriate priority level, see [SAP Note 67739](https://me.sap.com/notes/67739) .

## Performance Indicators for S4P

The following table shows the relevant performance indicators in various system areas.

| Area | Indicators | Value | Trend |
| --- | --- | --- | --- |
| System Performance | Active Users (>400 steps) | 167 | [GRAY] |
|  | Fiori Users | 25 | [GRAY] |
|  | Avg. Availability per Week | 100 % | [GRAY] |
|  | Avg. Response Time in Dialog Task | 438 ms | [GRAY] |
|  | Max. Dialog Steps per Hour | 6523 | [GRAY] |
|  | Avg. Response Time at Peak Dialog Hour | 341 ms | [GRAY] |
|  | Avg. Response Time in RFC Task | 362 ms | [GRAY] |
|  | Max. Number of RFCs per Hour | 3468 | [GRAY] |
|  | Avg. RFC Response Time at Peak Hour | 216 ms | [GRAY] |
| Hardware Capacity | Max. CPU Utilization on Appl. Server | 32 % | [GRAY] |
| Database Performance | Avg. DB Request Time in Dialog Task | 105 ms | [GRAY] |
|  | Avg. DB Request Time for RFC | 67 ms | [GRAY] |
|  | Avg. DB Request Time in Update Task | 64 ms | [GRAY] |
| Database Space Management | DB Size | 398.86 GB | [GRAY] |
|  | DB Growth Last Month | 4.97 GB | [GRAY] |

# 2 Landscape

## 2.1 Products and Components in current Landscape

Product

| System | SAP Product | Product Version |
| --- | --- | --- |
| S4P~ABAP | SAP S/4HANA | 2023 |

Main Instances

| Related System | Main Instance |
| --- | --- |
| S4P~ABAP | SAP S/4HANA Server |

SAP Fiori Add-Ons

| SAP Fiori Add-On | SAP Fiori Add-On Version |
| --- | --- |
| SAP FIORI FES FOR S/4HANA | 2023 |
| SAP FIORI FOR S4HANA | 2023 |

Databases

| Related System | Database System | Database Version | DB ID |
| --- | --- | --- | --- |
| S4P~ABAP | SAP HANA Database | 2.00.079.05 | H4P |

## 2.2 Servers in current Landscape

SAP Application Servers

| System | Host | Instance Name | Logical Host | ABAP | JAVA |
| --- | --- | --- | --- | --- | --- |
| S4P~ABAP | bswprdap01 | bsws4pap01_S4P_00 | bsws4pap01 | [GRAY] |  |

DB Servers

| Related System | Host | Logical Host (SAPDBHOST) |
| --- | --- | --- |
| S4P~ABAP | bswprddb01 | bswprddb01 |

Components

| Related System | Component | Host | Instance Name | Logical Host |
| --- | --- | --- | --- | --- |
| S4P~ABAP | ABAP SCS | bswprdap01 | bsws4pap01_S4P_10 | bsws4pap01 |

## 2.3 Hardware Configuration

Host Overview

| Host | Hardware Manufacturer | Model | CPU Type | CPU MHz | Virtualization | Operating System | CPUs | Cores | Memory in MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bswprdap01 | Microsoft Corporation | Virtual Machine[7.0] | Xeon Platinum 8272CL | 2600 | HYPER-V | SUSE Linux Enterprise Server 15 (x86_64) | 16 | 8 | 64294 |
| bswprddb01 | Microsoft Corporation | Virtual Machine[7.0] | Xeon Platinum 8280L | 2700 | HYPER-V | SUSE Linux Enterprise Server 15 (x86_64) | 64 | 32 | 515946 |

## 2.4 Transport Landscape

The information is extracted from the transport management system of S4P

Note: only real systems are considered, other systems are excluded.

The system role is determined based on the position of the system in the transport track. The first system with a consolidation transport route assigned is considered to be the development system. The system(s) with the longest transport track with no systems in line behind it is (are) considered to be the productive system(s). All systems in between and on parallel, but shorter, tracks are considered to be test systems. Systems in which no transport connections were detected are considered standalone systems.

The column "Detected By" denotes whether the system role was determined using the rules (R) or master data (M).

The system number and link to the SAP EarlyWatch Alert Dashboard can be determined only for systems sending data to SAP.

| Transport Track | Position | System Role | System ID | Installation Number | System Number | Detected By |
| --- | --- | --- | --- | --- | --- | --- |
| S4TS4P | 1 | Test | S4T | 0021220333 |  | R |
| S4TS4P | 2 | Production | S4P | 0021220331 | 000000000800631194 | R |

# 3 Service Data Quality and Service Readiness

| [IMAGE] | Configuration hints for optional service data are provided. The SAP S/4HANA system S4P is not fully prepared for delivery of future remote services . |
| --- | --- |

| Rating | Check Performed |
| --- | --- |
| [GREEN] | Sending EarlyWatch Alert of S4P to SAP Backbone |
| [GREEN] | Configuring S4P for SAP Note Assistant |
| [YELLOW] | Service Preparation of S4P |

## 3.1 Mainstream Maintenance for SAP Solution Manager

SAP Solution Manager is in mainstream maintenance until the **end of 2027** . SAP Cloud ALM is the go-to ALM platform for all SAP customers. It is recommended that you start the transition to SAP Cloud ALM now and complete it before 2028.

To build your roadmap for moving from SAP Solution Manager to SAP Cloud ALM, visit the transition center on [SAP Support Portal](https://support.sap.com/en/alm/sap-cloud-alm/transition-to-sap-cloud-alm.html) .

The recommended starting point for the transition is the [SAP Readiness Check for SAP Cloud ALM](https://support.sap.com/en/alm/sap-cloud-alm/transition-to-sap-cloud-alm.html?anchorId=section_1466687074) .

## 3.2 Sending EarlyWatch Alert of S4P to SAP Backbone

| [GREEN] | System S4P is prepared for SAP Support Backbone update sending EWA data on HTTPS through Solution Manager 7.2 DSA |
| --- | --- |

All connections to SAP Support Backbone use https protocol only. For a how to, refer to [Connectivity to SAP](https://support.sap.com/backbone-update) .

The following table shows the latest data transmissions for system S4P:

Latest Service Data for System S4P Sent to SAP

| Date (collected) | System | Sends EWA? | Kernel | Kernel | ST-PI | ST-PI | Destination | User | Ready for 2020 | Date (last sent) | Dest. Functional? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 04.05.2026 | Solution Manager 7.2 DSA | yes | 753_REL 800 | [GREEN] | 740 22 | [GREEN] | HTTPS -> SAP | S-user | [GREEN] | 27.04.2026 | [GREEN] |

### 3.2.1 Configuring S4P for SAP Note Assistant

Configuration and Usage of Digitally Signed SAP Notes

| Type | Finding | Further Information |
| --- | --- | --- |
| [BLUE] | SNOTE is configured to connect with HTTPS to SAP using destination SAP-SUPPORT_PORTAL to SAP's Service market place and destination SAP-SUPPORT_NOTE_DOWNLOAD to SAP's File content management system | Guided Answer 'Options for Downloading Digitally Signed SAP Notes' |

## 3.3 Service Data Quality

The service data is collected by the Service Data Control Center (SDCCN) or read from the Solution Manager's BW or Configuration and Change Database (CCDB) .

Recommendation: To resolve issues with the service data quality, follow the hints and SAP Notes provided below.

### 3.3.1 Quality of Service Data in Solution Manager Diagonstics - BW

| Prio. | Report Area affected | Details and Related Infocube | SAP Note |
| --- | --- | --- | --- |
| [BLUE] | Workload of ABAP System S4P | No performance data is returned from BW InfoCube. Infocube: 0CCMSMTPH used in section ' Workload Overview S4P ' | 1840395 |

### 3.3.2 Managed System Setup In Solution Manager

| Prio. | Report Area affected | Details | SAP Note |
| --- | --- | --- | --- |
| [BLUE] | Configuration of ABAP System S4P | Collector job DSWP_GET_PPMS_DATA_AUS_OSS for retrieval of the latest available SAP support packages is not running. Information about the latest available SAP support packages was omitted from this report due to unavailable data. Please ensure daily scheduling of this job in your SAP Solution Manager system. used in check ' Support Package Maintenance - ABAP ' | 894279 |

Legend for 'Priority' Column Above

| Prio. | Explanation: Impact of Missing or Erroneous Data |
| --- | --- |
| [BLUE] | An optional check was skipped. |

## 3.4 Service Preparation of S4P

| Rating | Check Performed |
| --- | --- |
| [YELLOW] | Service Preparation Check (RTCCTOOL) |
| [YELLOW] | Service Data Control Center of S4P |
| [GREEN] | Hardware Utilization Data |

In preparation for SAP services, ensure that connections, collectors, and service tools are up to date. These functionalities are explained in SAP Notes [91488](https://launchpad.support.sap.com/#/notes/91488) and [2253047](https://launchpad.support.sap.com/#/notes/2253047) .

### 3.4.1 Service Preparation Check (RTCCTOOL)

Report RTCCTOOL was last run on 04.05.2026. During the check, the tool detected issues for which a YELLOW rating was set.

| Overall Status | SAP Note | Topic | Tool Status | Manual Status |
| --- | --- | --- | --- | --- |
| [YELLOW] | 69455 | Addon ST-A/PI 01X_731 | [YELLOW] | [GRAY] |
| [YELLOW] | 69455 | Proc. after addon impl. | [YELLOW] | [GRAY] |
| [YELLOW] | 539977 | Addon ST-PI 758 | [YELLOW] | [GRAY] |
| [YELLOW] | 539977 | ST-PI 758 Support Package 1 | [YELLOW] | [GRAY] |
| [GREEN] | 69455 | Switch on digital content verification | [GREEN] | [GRAY] |
| [GREEN] | 69455 | Allow Online data collectors | [GREEN] | [GRAY] |
| [GREEN] | 12103 | Collectors and TCOLL | [GREEN] | [GREEN] |
| [GREEN] | 207223 | EWAlert setup | [GREEN] | [GRAY] |

**Recommendation:** 
 Addon ST-A/PI 01X_731 
 *"Servicetools for Applications Plug-In" for NetWeaver as of 7.31* *[your current version is one or two* *levels lower than the latest available]* 
 From [http://support.sap.com/supporttools](http://support.sap.com/supporttools) ->ST-A/PI->Installations&Upgrades download the installation ST-A/PI 01X_731. Upload to tx SAINT and install as per note 69455. Then restart report RTCCTOOL and choose 'List->Refresh from SAPNet'. 
 
 Proc. after addon impl. 
 *Procedure after implementation of Addon ST-A/PI* *[the addon contains specific analysis coding that is uncommented (*) if* *certain s/w components exist or supportpackage levels are met]* 
 In the Service preparation check, click on the button 'Addons&Upgr.' above and then press the button 'Procedure after addon implementation'. Afterwards click on the 'Refresh Status' button above. 
 
 Addon ST-PI 758 
 *Addon ST-PI 758 for SAP basis as of 758* *[your current ST-PI level is one to four lower than the latest* *available]* 
 From [http://support.sap.com/supporttools](http://support.sap.com/supporttools) -> ST-PI -> Installations&Upgrades -> download the addon file ST-PI 758. Upload the file to transaction SAINT 'Installation package > Load packages > From Frontend' and install as per note 3705970. Then restart report RTCCTOOL from SE38. 
 
 ST-PI 758 Support Package 1 
 *Addon supportpackage level 1 for ST-PI 758 for basis as of 758* *[your current patch is one to four levels lower than the latest* *available]* 
 Open [http://support.sap.com/supporttools](http://support.sap.com/supporttools) ->ST-PI Supportpck.-> ST-PI 758. Add patch SAPK-75801INSTPI (and predecessors if not yet implemented) to download basket. Release basket via Maintenance optimizer. Upload from frontend into transaction SPAM, define a queue and import the queue.

### 3.4.2 SDCC Destination Table

The table below summarizes the destinations configured in Service Data Control Center.

| Finding | Details | Rating |
| --- | --- | --- |
| There exists RFC destination SDCC_OSS to SAP Support Backbone. | Calls on RFC protocol to SAP Support Backbone are no more supported. You may delete destination SDCC_OSS | [YELLOW] |
| There is no destination to SAP Support Backbone. | The connection to SAP can be established trough a Solution Manager or Focused Run. | [BLUE] |
| On this SAP S/4HANA system a Source System for Service Definitions is defined. | The Focused Run is defined as Source System for Service Definitions. Find information about the Source System for Service Definitions flag in SAP Note SAP Note 1075827 . | [GREEN] |
| A Solution Manager ('BACK') destination exists. | This destination can establish a connection to SAP Support Backbone. | [GREEN] |

Recommendation: Resolve the issue reported in the table.

# 4 Software Configuration for S4P

| [IMAGE] | We have listed recommendations concerning the current software configuration on your system. |
| --- | --- |

Your system's software versions are checked. If known issues with the software versions installed are identified, they are highlighted.

## 4.1 SAP Application Release - Maintenance Phases

| SAP Product Version | End of Mainstream Maintenance | Status |
| --- | --- | --- |
| SAP S/4HANA 2023 | 31.12.2030 | [GREEN] |

Rating Legend

| Rating | Description |
| --- | --- |
| [GREEN] | Mainstream / Extended maintenance offered by SAP is available for the next 18 months or longer. |
| [YELLOW] | Mainstream / Extended maintenance offered by SAP will end in 6 to 18 months. |
| [RED] | Mainstream / Extended maintenance offered by SAP has expired or will expire in the next 6 months. |

Your main product version runs under SAP mainstream maintenance until 31.12.2030.

Please note that this check, if created on your on-premise SAP Solution Manager, does not take account of extended maintenance options. In this case, **your main product version is checked for SAP mainstream maintenance only** , which might lead to invalid ratings, especially for SAP S/4HANA 1709, SAP S/4HANA 1809, and SAP S/4HANA 1909.

A complete verification, including your individual extended maintenance contracts, is only available via the SAP EarlyWatch Alert Workspace in [SAP for Me](https://me.sap.com/home) .

For general information about the SAP EarlyWatch Alert Workspace, read the SAP Knowledge Base Article [2520319](https://me.sap.com/notes/2520319) : How to access the SAP EarlyWatch Alert apps in SAP for Me.

Refer to the tab 'Maintenance' on the [Customer Insights Dashboard](https://me.sap.com/reporting/maintenance) for further information on the maintenance status of any additional add-on product versions in your system. To find more details and resources, navigate to the Product Availability Matrix by clicking on the add-on product version name here.

## 4.2 Maintenance and Update Strategy for SAP Fiori Front-End Server

### 4.2.1 SAP Fiori Front-End Server Version

| Software Product | SAP_UI Release | End of Maintenance | Rating |
| --- | --- | --- | --- |
| SAP Fiori FES 2023 for S/4HANA | 758 | 31.12.2030 | [GREEN] |

Your version of the SAP Fiori Front-End Server (SAP_UI) is still in maintenance by SAP. For further information on the SAP Fiori Front-End Server maintenance and upgrade strategy, refer to SAP Note [2217489](https://launchpad.support.sap.com/#/notes/2217489) .

### 4.2.2 SAPUI5 Version

| SAPUI5 | Installed | End Date | Rating |
| --- | --- | --- | --- |
| Version | 1.120 | 31.12.2030 (EoM) | [GREEN] |
| Patch Level | 23 | 31.12.2025 (EoCP) | [BLUE] |

Your SAPUI5 Library version is up to date as recommended. The planned end of maintenance (EoM) for your SAPUI5 Library version is in more than 6 months. Furthermore, no SAP Fiori Launchpad content is exposed or used by services on the SAP Business Technology Platform (BTP). In this case reaching the end of cloud provisioning (EoPC) is not critical for your system. Nevertheless, it is still important to keep the patch level up to date to avoid bugs and security risks. The maintenance status of all SAPUI5 versions and patch levels can be found in the [SAPUI5 Version Overview](https://sapui5.hana.ondemand.com/versionoverview.html) .

## 4.3 Support Package Maintenance - ABAP

The following table shows an overview of currently installed software components.

Support Packages

| Software Component | Version | Patch Level | Latest Avail. Patch Level | Support Package | Component Description |
| --- | --- | --- | --- | --- | --- |
| CLOUDLM | 100 | 24 |  | SAPK-10024INCLOUDLM |  |
| EA-DFPS | 808 | 3 |  | SAPK-80803INEADFPS |  |
| EA-PS | 808 | 3 |  | SAPK-80803INEAPS |  |
| FI-CAX | 808 | 3 |  | SAPK-80803INFICAX |  |
| GBX01HR5 | 605 | 32 |  | SAPK-60532INGBX01HR5 |  |
| HOME | DEV | 0 |  |  |  |
| IS-OIL | 808 | 3 |  | SAPK-80803INISOIL |  |
| IS-PRA | 808 | 3 |  | SAPK-80803INISPRA |  |
| IS-PS-CA | 808 | 3 |  | SAPK-80803INISPSCA |  |
| IS-UT | 808 | 3 |  | SAPK-80803INISUT |  |
| LOCAL | DEV | 0 |  |  |  |
| MDG_APPL | 808 | 3 |  | SAPK-80803INMDGAPPL |  |
| MDG_FND | 808 | 3 |  | SAPK-80803INMDGFND |  |
| PCAI_ENT | 100 | 0 |  |  |  |
| PERSONAS | 300 | 19 |  | SAPK-30019INPERSONAS |  |
| S4CEXT | 108 | 3 |  | SAPK-10803INS4CEXT |  |
| S4CORE | 108 | 3 |  | SAPK-10803INS4CORE |  |
| S4COREOP | 108 | 3 |  | SAPK-10803INS4COREOP |  |
| S4DEPREC | 108 | 3 |  | SAPK-10803INS4DEPREC |  |
| S4FND | 108 | 3 |  | SAPK-10803INS4FND |  |
| S4HCM | 101 | 16 |  | SAPK-10116INS4HCM |  |
| S4HCMCAE | 101 | 16 |  | SAPK-10116INS4HCMCAE |  |
| S4HCMCAR | 101 | 16 |  | SAPK-10116INS4HCMCAR |  |
| S4HCMCAT | 101 | 16 |  | SAPK-10116INS4HCMCAT |  |
| S4HCMCAU | 101 | 16 |  | SAPK-10116INS4HCMCAU |  |
| S4HCMCBE | 101 | 16 |  | SAPK-10116INS4HCMCBE |  |
| S4HCMCBG | 101 | 16 |  | SAPK-10116INS4HCMCBG |  |
| S4HCMCBR | 101 | 16 |  | SAPK-10116INS4HCMCBR |  |
| S4HCMCCA | 101 | 16 |  | SAPK-10116INS4HCMCCA |  |
| S4HCMCCH | 101 | 16 |  | SAPK-10116INS4HCMCCH |  |
| S4HCMCCL | 101 | 16 |  | SAPK-10116INS4HCMCCL |  |
| S4HCMCCN | 101 | 16 |  | SAPK-10116INS4HCMCCN |  |
| S4HCMCCO | 101 | 16 |  | SAPK-10116INS4HCMCCO |  |
| S4HCMCCZ | 101 | 16 |  | SAPK-10116INS4HCMCCZ |  |
| S4HCMCDE | 101 | 16 |  | SAPK-10116INS4HCMCDE |  |
| S4HCMCDK | 101 | 16 |  | SAPK-10116INS4HCMCDK |  |
| S4HCMCEG | 101 | 16 |  | SAPK-10116INS4HCMCEG |  |
| S4HCMCES | 101 | 16 |  | SAPK-10116INS4HCMCES |  |
| S4HCMCFI | 101 | 16 |  | SAPK-10116INS4HCMCFI |  |
| S4HCMCFR | 101 | 16 |  | SAPK-10116INS4HCMCFR |  |
| S4HCMCGB | 101 | 16 |  | SAPK-10116INS4HCMCGB |  |
| S4HCMCGR | 101 | 16 |  | SAPK-10116INS4HCMCGR |  |
| S4HCMCHK | 101 | 16 |  | SAPK-10116INS4HCMCHK |  |
| S4HCMCHR | 101 | 16 |  | SAPK-10116INS4HCMCHR |  |
| S4HCMCHU | 101 | 16 |  | SAPK-10116INS4HCMCHU |  |
| S4HCMCID | 101 | 16 |  | SAPK-10116INS4HCMCID |  |
| S4HCMCIE | 101 | 16 |  | SAPK-10116INS4HCMCIE |  |
| S4HCMCIN | 101 | 16 |  | SAPK-10116INS4HCMCIN |  |
| S4HCMCIT | 101 | 16 |  | SAPK-10116INS4HCMCIT |  |
| S4HCMCJP | 101 | 16 |  | SAPK-10116INS4HCMCJP |  |
| S4HCMCKR | 101 | 16 |  | SAPK-10116INS4HCMCKR |  |
| S4HCMCKW | 101 | 16 |  | SAPK-10116INS4HCMCKW |  |
| S4HCMCKZ | 101 | 16 |  | SAPK-10116INS4HCMCKZ |  |
| S4HCMCMX | 101 | 16 |  | SAPK-10116INS4HCMCMX |  |
| S4HCMCMY | 101 | 16 |  | SAPK-10116INS4HCMCMY |  |
| S4HCMCNL | 101 | 16 |  | SAPK-10116INS4HCMCNL |  |
| S4HCMCNO | 101 | 16 |  | SAPK-10116INS4HCMCNO |  |
| S4HCMCNZ | 101 | 16 |  | SAPK-10116INS4HCMCNZ |  |
| S4HCMCOM | 101 | 16 |  | SAPK-10116INS4HCMCOM |  |
| S4HCMCPH | 101 | 16 |  | SAPK-10116INS4HCMCPH |  |
| S4HCMCPL | 101 | 16 |  | SAPK-10116INS4HCMCPL |  |
| S4HCMCPT | 101 | 16 |  | SAPK-10116INS4HCMCPT |  |
| S4HCMCQA | 101 | 16 |  | SAPK-10116INS4HCMCQA |  |
| S4HCMCRO | 101 | 16 |  | SAPK-10116INS4HCMCRO |  |
| S4HCMCRU | 101 | 16 |  | SAPK-10116INS4HCMCRU |  |
| S4HCMCSA | 101 | 16 |  | SAPK-10116INS4HCMCSA |  |
| S4HCMCSE | 101 | 16 |  | SAPK-10116INS4HCMCSE |  |
| S4HCMCSG | 101 | 16 |  | SAPK-10116INS4HCMCSG |  |
| S4HCMCSI | 101 | 16 |  | SAPK-10116INS4HCMCSI |  |
| S4HCMCSK | 101 | 16 |  | SAPK-10116INS4HCMCSK |  |
| S4HCMCTH | 101 | 16 |  | SAPK-10116INS4HCMCTH |  |
| S4HCMCTR | 101 | 16 |  | SAPK-10116INS4HCMCTR |  |
| S4HCMCTW | 101 | 16 |  | SAPK-10116INS4HCMCTW |  |
| S4HCMCUA | 101 | 16 |  | SAPK-10116INS4HCMCUA |  |
| S4HCMCUN | 101 | 16 |  | SAPK-10116INS4HCMCUN |  |
| S4HCMCUS | 101 | 16 |  | SAPK-10116INS4HCMCUS |  |
| S4HCMCVE | 101 | 16 |  | SAPK-10116INS4HCMCVE |  |
| S4HCMCZA | 101 | 16 |  | SAPK-10116INS4HCMCZA |  |
| S4HCMGXX | 101 | 16 |  | SAPK-10116INS4HCMGXX |  |
| S4HCMRXX | 101 | 16 |  | SAPK-10116INS4HCMRXX |  |
| SAP_ABA | 75I | 3 |  | SAPK-75I03INSAPABA |  |
| SAP_BASIS | 758 | 3 |  | SAPK-75803INSAPBASIS |  |
| SAP_BW | 758 | 3 |  | SAPK-75803INSAPBW |  |
| SAP_GWFND | 758 | 3 |  | SAPK-75803INSAPGWFND |  |
| SAP_UI | 758 | 3 |  | SAPK-75803INSAPUI |  |
| ST-A/PI | 01W_731 | 2 |  | SAPKITABC9 |  |
| ST-PI | 740 | 32 |  | SAPK-74032INSTPI |  |
| UIAPFI70 | 902 | 3 |  | SAPK-90203INUIAPFI70 |  |
| UIBAS001 | 758 | 1 |  | SAPK-75801INUIBAS001 |  |
| UIS4HOP1 | 900 | 3 |  | SAPK-90003INUIS4HOP1 |  |

## 4.4 Database - Maintenance Phases

| Database Version | End of Standard Vendor Support* | Comment | Status | SAP Note |
| --- | --- | --- | --- | --- |
| SAP HANA Database 2.0 |  | Follows Application | [GREEN] | 2378962 |

* Maintenance phases and duration for the DB version are defined by the vendor. Naming of the phases and required additional support contracts differ depending on the vendor. Support can be restricted to specific patch levels by the vendor or by SAP. Check in the referenced SAP Note(s) whether your SAP system requires a specific patch release to guarantee support for your database version.

## 4.5 Operating System(s) - Maintenance Phases

| Host | Operating System | End of Standard Vendor Support* | End of Extended Vendor Support* | Comment | Status | SAP Note |
| --- | --- | --- | --- | --- | --- | --- |
| 2 Hosts | SUSE Linux Enterprise Server 15 (x86_64) | 31.07.2028 | 31.07.2031 | Limited (LTSS) | [GREEN] | 936887 |

* Maintenance phases and duration for the operating system version are defined by the vendor. Naming of the phases and required additional support contracts differ depending on the vendor. Support can be restricted to specific patch levels by the vendor or by SAP. Check in the referenced SAP Note(s) whether your SAP system requires a specific patch release to guarantee support for your operating system version.

## 4.6 HANA Database Version for H4P

The following table shows your current/planned SAP HANA database version.

**Please Note:** There are different kinds of support packages:

S: Standard HANA support package

LTS: Long-term support package version

V: Last support package for a HANA version

HANA Database Version

| SID | SPS Stack | SP Revision | Maintenance Revision | In Maintenance ? | SAP Notes | Upgrade Information | Support Package Kind |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H4P | 2.00 SP 07 | 2.00.079.005 | yes | [GREEN] | 2378962 | [GREEN] | S |

## 4.7 SAP HANA: SQLDBC Version

### 4.7.1 SAP HANA: Installed SQLDBC Version

The following table shows your currently installed SAP HANA database client component version.

| Instance Name | SQLDBC Version | Rating |
| --- | --- | --- |
| bsws4pap01 00 | 2.08.022 | [GREEN] |

| SAP Note | Description |
| --- | --- |
| 1906576 | HANA client and server cross-version compatibility |
| 2339267 | The SAP HANA client version and installation manifest file doesn't match currently available SAP HANA server version information |

## 4.8 SAP HANA: Installed DBSL Version

The following table shows the DBSL version currently installed.

| Instance | Current DBSL Release | Current DBSL Patch | Recommended DBSL Release | Recommended DBSL Patch | Rating |
| --- | --- | --- | --- | --- | --- |
| bsws4pap01_S4P_00 | 793 | 300 | 793 |  | [GREEN] |

Your installed SAP HANA DBSL meets the recommended requirement to access the SAP HANA database.

## 4.9 SAP Kernel Release

The following table lists all information about your SAP kernel(s) currently in use.

| Instance(s) | SAP Kernel Release | Patch Level | Age in Months | OS Family |
| --- | --- | --- | --- | --- |
| bsws4pap01_S4P_00 | 793 | 300 | 13 | Linux (x86_64) |

### 4.9.1 Newer SP Stack Kernel Available

Your current SAP kernel patch level is not up to date.

**Recommendation:** Consider updating to the latest SP Stack Kernel. For details see SAP Note [2083594](https://me.sap.com/notes/2083594) , [3116151](https://me.sap.com/notes/3116151) , and [19466](https://me.sap.com/notes/19466) .

### 4.9.2 Additional Remarks

SAP releases Support Package stacks (including SAP kernel patches) on a regular basis for most products (generally 2–4 times a year). We recommend that you base your software maintenance strategy on these stacks.

You should only consider using a more recent SAP kernel patch than that shipped with the latest Support Package Stack for your product if specific errors occur.

For more information, see SAP Service Marketplace at [https://support.sap.com/software/patches/stacks.html](https://support.sap.com/software/patches/stacks.html) (SAP Support Package Stack information) and [https://me.sap.com/softwarecenter/support/index](https://me.sap.com/softwarecenter/support/index) (Support Packages & patch information).

For each patch there is an SAP Note in which all known regressions for this level are listed. Find it using the keyword [KRNL793PL300](https://me.sap.com/servicessupport/search/%7B%22q%22%3A%22=KRNL793PL300%22%2C%22tab%22%3A%22All%22%7D) in the SAP Note search. For detailed information, see SAP Note [1802333](https://me.sap.com/notes/1802333) – Finding information about regressions in the SAP kernel.

# 5 Hardware Capacity

| [IMAGE] | We have checked your system for potential CPU or memory bottlenecks and found that the hardware is sufficient for the current workload. |
| --- | --- |

**Note:** Hardware capacity evaluation is based on hosts for which data is at least partially available.

## 5.1 Overview System S4P

**General** 
 This analysis focuses on the workload during the peak working hours **(9-11, 13)** and is based on the hourly averages collected by SAPOSCOL. For information about the definition of peak working hours, see SAP Note [1251291](https://launchpad.support.sap.com/#/notes/1251291) .

**CPU** 
 If the average CPU load exceeds **75%** , temporary CPU bottlenecks are likely to occur. An average CPU load of more than **90%** is a strong indicator of a CPU bottleneck.

**Memory** 
 If your hardware cannot handle the maximum memory consumption, this causes a memory bottleneck in your SAP system that can impair performance. The paging rating depends on the ratio of paging activity to physical memory. A ratio exceeding **25%** indicates high memory usage (if Java has been detected **0%** ) and values above **50%** (Java **10%** ) demonstrate a main memory bottleneck.

| Server | Max. CPU load [%] | Date | Rating | RAM [MB] | Max. Paging [% of RAM] | Date | Rating | Analysis Start | Analysis End |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bswprdap01 | 32 | 03.05.2026 | [GREEN] | 64.294 | 0 |  | [GREEN] | 27.04.2026 | 03.05.2026 |
| bswprddb01 | 0 |  | [GREEN] | 515.946 | 0 |  | [GREEN] | 27.04.2026 | 03.05.2026 |

**Note:** For virtualization or IaaS scenarios (for example, IBM PowerVM, VMware, Amazon AWS, ...) it is possible that the CPU rating for some hosts is YELLOW or RED, even though the utilization value is quite low. In this case, the relevant host could not use maximum usable capacity due to a resource shortage within the virtualized infrastructure (for example, IBM PowerVM: Shared Pool CPU utilization).

# 6 Business Key Figures

System errors or business exceptions can be a reason for open, overdue, or unprocessed business documents or long-lasting processes. SAP Business Process Analysis, Stabilization and Improvement offerings focus on helping you to find these documents (as it may directly or indirectly negatively impact business). 
 This section provides an example of indicators, and its findings are a basis of further SAP offerings. In the example below, the backlog of business documents is compared to daily or weekly throughput or set in relation to absolute threshold numbers.

It provides business information to discuss possible technical or core business improvement process potential. 
 SAP tools and methods can help to monitor and analyze business processes in more detail. 
 Find more information, see [here](http://discover.sap.com/germany-business-process-improvement#section_0) .

**NOTE:** Overdue or exceptional business documents are often caused by system errors, *such as user handling issues, configuration or master data issues, or open documents on inactive organizational units or document types* that can be included in the measurements. These documents are rarely processed further by the business departments and often do not have a direct impact on customer satisfaction, revenue stream, or working capital. Nevertheless, these documents can have negative impacts on other areas such as supply chain planning accuracy, performance (of other transactions, reports, or processes), and reporting quality. 
 
 For more information about this section, see [here](https://support.sap.com/support-programs-services/services/earlywatch-alert/documentation.html) . See "Which optional content can be activated in SAP EarlyWatch Alert?".

## 6.1 Reference Key Figures Measured Value Summary

The below values originate from reference key figures executed in your back-end system. A rating is given as the first criticality indicator for each value that may represent open, overdue, or exception documents. The rating can be based on the absolute number of references or relate to a certain business throughput. Note that a rating can be assigned only if a reference value is available (in the case of relative evaluation) or if the evaluation is based on an absolute number.

The following general rule of thumb applies to most ratings of application-related backlog key figures: 
 GREEN – the backlog is smaller than one day of typical daily throughput 
 YELLOW – the backlog is between one and five days of typical daily throughput 
 RED – the backlog is above five days of typical daily throughput 
 GRAY – standard evaluation is not possible due to missing reference value

Bear in mind that all assumptions and ratings in this presentation are based on our general experience with other customers and that the findings are not necessarily business-critical in your particular case. The key figures are further described in the [KPI Cloud Catalog](https://zkpicatalog-supportportal.dispatcher.hana.ondemand.com/?sap-language=EN) . 
 
 Data collection status:

Data collection frequency (in months): 1

| Rating | Business Area: Key Figure Short Name | Finding | # |
| --- | --- | --- | --- |
| [YELLOW] | Finance: Overdue vendor payments (actual fiscal year) [K20] | 174 open vendor items in Accounts Payable in the current were identified, whereby the due date for payment is .. (31 less than three months &#038; 0 older than twelve months). Based on absolute numbers (GREEN[<100]; RED[>1000]). |  |
| [YELLOW] | Finance: Overdue customer payments (actual fiscal year) [K15] | 220 open customer items in Accounts Receivable in the current were identified, whereby the due date for payment is .. (20 less than three months &#038; 7 older than twelve months). Based on absolute numbers (GREEN[<100]; RED[>1000]). |  |
| [YELLOW] | Finance: Bank Statement Items not completed [K16] | 98 bank statement items were identified that have not been fully posted (0 less than three months &#038; 86 older than twelve months). Based on absolute numbers (GREEN[<10]; RED[>100]). |  |
| [YELLOW] | Finance: LT: Invoice Item -> Clearing [K18] | 51 days of average lead time were identified for all invoice items that were cleared in the analyzed reference per... Based on absolute numbers (GREEN[<30]; RED[>60]). |  |
| [GREEN] | Order To Cash: Overdue Outbound Deliveries [K11] | 37 outbound deliveries that are overdue by more than one day and that do not have goods issue po.. (0 less than three months &#038; 4 older than twelve months). Based on 254 created (max per week) (GREEN[<254]; RED[>762]). |  |
| [YELLOW] | Order To Cash: Deliveries with overdue invoices [K12] | 142 deliveries with overdue Invoices were identified (0 less than three months &#038; 6 older than twelve months). Based on absolute numbers (GREEN[<100]; RED[>1000]). |  |
| [YELLOW] | Order To Cash: Orders not billed (Order related billing) [K06] | 32 open sales orders were identified that have not yet been billed or have only been partially billed (0 less than three months &#038; 28 older than twelve months). Based on absolute numbers (GREEN[<10]; RED[>100]). |  |
| [RED] | Order To Cash: Orders billed not delivered [K07] | 213 open sales orders were identified that have not been delivered but have already been billed (5 less than three months &#038; 205 older than twelve months). Based on absolute numbers (GREEN[<1]; RED[>10]). |  |
| [YELLOW] | Order To Cash: Invoices not posted to FI [K14] | 17 invoices that have not been posted to FI and that are older than one day were identified (0 less than three months &#038; 17 older than twelve months). Based on absolute numbers (GREEN[<10]; RED[>100]). |  |
| [RED] | Order To Cash: Sales Order Schedule Line Items overdue [K04] | 1.213 open sales order schedule line items were found that were not delivered or only partially delivered with at le.. (43 less than three months &#038; 945 older than twelve months). Based on 221 created (max per week) (GREEN[<221]; RED[>1105]). |  |
| [GRAY] | Procure To Pay: Overdue Inbound Deliveries [K29] | 350 overdue inbound deliveries were identified for which the delivery date is more than one day ago and no or only .. (0 less than three months & 349 older than twelve months). Based on 0 created (max per week). |  |
| [GRAY] | Procure To Pay: Planned Orders with Planned Opening Date in the past (ext.) [K32] | 17.485 planned orders (external procurement) were identified for which the planned opening date is in the past (3.316 less than three months & 4.432 older than twelve months). Based on 0 created (max per week). |  |
| [GRAY] | Procure To Pay: Overdue PO items [K28] | 1.595 purchase order items were identified that are overdue by more than 10 days and that are not yet completely deli.. (239 less than three months & 170 older than twelve months). Based on 0 PO items created (max per week). |  |
| [GREEN] | Procure To Pay: Overdue Purchase Requisition Items [K27] | 737 purchase requisition items were identified that are open and overdue by more than 10 days (22 less than three months &#038; 493 older than twelve months). Based on 30187 created (max per week) (GREEN[<30187]; RED[>150935]). |  |
| [RED] | Procure To Pay: Blocked invoices for payment [K30] | 22.968 vendor invoices items were identified which were created more than 30 days ago and still have not been released.. (0 less than three months &#038; 22.968 older than twelve months). Based on absolute numbers (GREEN[<100]; RED[>1000]). |  |
| [YELLOW] | Plan To Produce: Failed goods movements: Process Orders [K56] | 12 failed goods movements were identified that are more than one day old. Based on absolute numbers (GREEN[<10]; RED[>100]). |  |
| [GRAY] | Plan To Produce: Planned Orders with Planned Opening Date in the past [K44] | 17.596 planned orders were identified for which the planned opening date is in the past (1.803 less than three months & 1.872 older than twelve months). Based on 0 Planned orders (inhouse) created (max per week). |  |
| [GREEN] | Plan To Produce: Process Orders overdue for release [K54] | 7 process orders that are overdue for release by more than five days were identified. Based on absolute numbers (GREEN[<10]; RED[>100]). |  |
| [GREEN] | Plan To Produce: Process Orders overdue for Delivery Completed [K59] | 4 process orders were identified that have been overdue for delivery completed for seven days. Based on 4854 created (max per week) (GREEN[<1618]; RED[>4854]). |  |
| [RED] | Plan To Produce: Process Orders overdue for Del. Ind. and not Closed [K55] | 157.388 process orders have been identified for which the deletion status was not yet active more than 30 days ago (5.045 less than three months &#038; 140.563 older than twelve months). Based on absolute numbers (GREEN[<20000]; RED[>100000]). |  |
| [GRAY] | Replenishment: Overdue Stock Transport Order Items w/o Outb. Del. Compl. [K35] | 10 STO items were identified that are more than 10 days overdue and that have not yet been completely delivered (2 less than three months & 0 older than twelve months). Based on 0 created (max per week). |  |
| [GRAY] | Replenishment: Overdue Stock Transport Order Schedule Lines [K34] | 305 STO schedule lines were identified that are overdue by more than 10 days and that have not yet been completely .. (81 less than three months & 138 older than twelve months). Based on 0 created (max per week). |  |
| [GREEN] | Warehouse Management: Outbound Transfer Order Items open [K39] | 1.233 open picking transfer order (TO) items were found that were created more than three days ago but that still hav.. (1 less than three months &#038; 0 older than twelve months). Based on 3931 created (max per week) (GREEN[<3931]; RED[>19655]). |  |
| [RED] | Warehouse Management: Transfer Requirement Items open [K41] | 93.785 open transfer requirement items (TR items) were identified that were created over three days ago and that still.. (25.015 less than three months &#038; 20.739 older than twelve months). Based on 1215 created (max per week) (GREEN[<1215]; RED[>6075]). |  |

SAP Active Global Support provides several self-assessments or guided services to encourage customers to benefit from an SAP Business Process Analysis, Stabilization, or Improvement project.

## 6.2 SAP Business Process Analytics

With SAP Business Process Analytics in SAP Solution Manager, you can continuously analyze the above key figures and more than 750 additional out-of-the-box key figures for continuous improvement potential in your SAP business processes.

With SAP Business Process Analytics, you can perform the following functions:

**(1)** Internal business process benchmarking (across organizational units, document types, customers, materials, and so on) for a number of exceptional business documents and/or for the cumulated monetary value of these documents.

**(2)** Age analysis to measure how many open documents you have from the previous years or months.

**(3)** Trend analysis for these business documents over a certain time period.

**(4)** Create a detailed list for all of these exceptional business documents in the managed system, enabling a root cause analysis to find reasons why these documents are open, overdue, or erroneous.

SAP Business Process Analytics can help you to achieve the following main goals:

- Gain global transparency of business-relevant exceptions to control template adherence

- Improve process efficiency and reduce process costs by reducing system issues and eliminating waste (for example, user handling, configuration issues, and master data issues)

- Improve working capital (increase revenue, reduce liabilities and inventory levels)

- Ensure process compliance (support internal auditing)

- Improve supply chain planning (better planning results and fewer planning exceptions)

- Improve closing (fewer exceptions and less postprocessing during period-end closing)

SAP also provides business process improvement methodology to help you identify and analyze improvement potential within your business processes using Business Process Analytics in SAP Solution Manager and visualize it for your senior management.

For more information, navigate to the following link: [here](http://wiki.scn.sap.com/wiki/display/SM/Business+Process+Improvement) .

In general, SAP Active Global Support provides several self-assessments or guided services to encourage customers to benefit from an SAP Business Process Stabilization and/or Business Process Improvement project.

# 7 Workload of System S4P

This chart displays the main task types and indicates how their workload is distributed in the system. The table below lists the detailed KPIs.
[IMAGE]

Response Time Components In Hours

| Task Type | Response Time | Wait Time | CPU Time | DB Time | GUI Time |
| --- | --- | --- | --- | --- | --- |
| BATCH | 70,7 | 0,0 | 10,9 | 11,1 | 0,0 |
| DIALOG | 40,7 | 0,0 | 11,0 | 9,7 | 8,8 |
| RFC | 37,8 | 0,0 | 5,8 | 5,3 | 0,0 |
| SPOOL | 12,3 | 4,0 | 0,5 | 0,2 | 0,0 |
| Others | 3,1 | 0,3 | 1,4 | 1,4 | 0,0 |

## 7.1 Workload By Users

User activity is measured in the workload monitor. Only users of at least medium activity are counted as 'active users'.

| Users | Low Activity | Medium Activity | High Activity | Total Users |
| --- | --- | --- | --- | --- |
| dialog steps per week | 1 to 399 | 400 to 4799 | 4800 or more |  |
| measured in system | 56 | 134 | 33 | 223 |

## 7.2 Workload Distribution S4P

The performance of your system was analyzed with respect to the workload distribution. We did not detect any major problems that could affect the performance of your SAP system.

### 7.2.1 Workload by Application Module

The following diagrams show how each application module contributes to the total system workload. Two workload aspects are shown: 
 - CPU time: total CPU load on all servers in the system 
 - Database time: total database load generated by the application

All programs that are not classified in the Application Hierarchy are summarized in the "Unassigned" category. Customer programs, industry solutions, and third-party add-on developments may fall into this category.

The Application Hierarchy can be found in the Repository Browser (transaction SE80): in the "Object Category" selection field choose "Application Hierarchy".
[IMAGE]
[IMAGE]

### 7.2.2 DB Load Profile

| [GREEN] | The number of work processes creating database load in parallel is not significantly high. |
| --- | --- |

The following diagram shows the DB load caused by dialog, RFC, HTTP(S), and background tasks, over different time frames.

The data provided in the diagram represents the average number of database processes occupied by each task type in the database during the specified time frames.

These statistics are calculated as a weekly average, the average values over six working days with a unit of one hour. Periods between 00:00-06:00 and 21:00-24:00 contain an average value per hour, as these are not core business hours.

You can enable 24-hour monitoring by implementing SAP Note 910897. With 24-hour monitoring, the time profile returns the workload of the system or application server on an hourly basis rather than returning an average value per hour for the periods 00:00–06:00 and 21:00–24:00.

By comparing the load profiles for dialog and background activity, you can get an overview of the volume of background activity during online working hours.
[IMAGE]

# 8 Performance Overview S4P

| [IMAGE] | The performance of your system was analyzed with respect to the average response times and total workload. We did not detect any major problems that could affect the performance of your system. |
| --- | --- |

Note: To access the response time statistics in SAP EarlyWatch Alert Workspace, click [system response time](https://me.sap.com/ewa/dashboard/sysResTimeFlex/S4P_0021220331_000000000800631194)

The following table shows the average response times for various task types:

Averages of Response Time Components in ms

| Task type | Dialog Steps | Response Time | CPU Time | Wait Time | Load Time | DB Time | GUI Time |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DIALOG | 335.412 | 438,2 | 118,2 | 0,1 | 3,0 | 104,6 | 94,7 |
| RFC | 329.363 | 414,2 | 63,6 | 0,2 | 1,7 | 58,2 | 0,0 |
| UPDATE | 48.334 | 146,0 | 53,0 | 25,6 | 5,5 | 64,2 | 0,0 |
| UPDATE2 | 55.597 | 54,3 | 23,1 | 3,0 | 1,2 | 28,6 | 0,0 |
| BATCH | 319.841 | 796,0 | 122,3 | 0,0 | 1,6 | 125,2 | 0,0 |
| SPOOL | 36.006 | 1.225,2 | 53,5 | 395,0 | 0,1 | 21,0 | 0,0 |
| HTTP | 48.425 | 4,8 | 4,3 | 0,0 | 0,5 | 0,5 | 0,0 |
| HTTPS | 5.665 | 230,5 | 125,8 | 0,1 | 1,9 | 81,0 | 0,0 |

## 8.1 Performance Evaluation

The measured times are compared against reference times to provide a rating.

- If the number of dialog steps in an hour is less than 1000, this hour is not considered.

- If the total number of transaction steps is less than 20000, the rating for the task is not performed (indicated by a gray icon in the table).

- RED if at least three time ranges are rated RED.

- YELLOW if two time ranges are rated RED or at least three time ranges are rated YELLOW.

The table below shows that no problem is expected on the application or database servers.

| Task | Steps | Application Server Performance | Database Server Performance |
| --- | --- | --- | --- |
| Dia | 335.404 | [GREEN] | [GREEN] |
| Upd | 48.334 | [GREEN] | [GREEN] |
| HTTP | 48.425 | [GREEN] | [GREEN] |
| HTTPS | 5.665 | [GRAY] | [GRAY] |

The ratings in the table above are determined by comparisons against the reference table below.

If the dialog response times are very poor, it will cause a RED rating for the entire check.

| Task | Reference for Avg. Response Time (ms) Yellow Rating | Reference for Avg. Response Time (ms) Red Rating | Reference for Avg. DB time (ms) Yellow Rating | Reference for Avg. DB time (ms) Red Rating |
| --- | --- | --- | --- | --- |
| Dia | 1.200 | 3.600 | 600 | 1.800 |
| Upd | 2.400 | 3.600 | 1.200 | 1.800 |
| HTTP | 1.200 | 3.600 | 600 | 1.800 |
| HTTPS | 1.200 | 3.600 | 600 | 1.800 |

## 8.2 Transaction Profile Check

The following tables show the response times and the number of dialog steps for the transactions that cause the heaviest workload in your system.

### 8.2.1 Transactions by Total Workload

To access the transaction response time in SAP EarlyWatch Alert Workspace, click [here](https://me.sap.com/ewa/dashboard/serverTopTransDetail/S4P_0021220331_000000000800631194) .

The following tables list the activities with the highest contribution to the total workload.

To view the workload of all transactions/programs, you can use the Workload Monitor in your SAP system. You can refer to this [Guided Answer](https://ga.support.sap.com/dtp/viewer/#/tree/650/actions/6868) to diagnose a general performance problem in Workload Analysis.

Workload by Transaction (Dialog/HTTP(S)/WS-HTTP )

| Transaction | Type | Dialog Steps | Total Resp. Time in % | Avg. Resp. Time in ms | Avg. CPU Time in ms | Avg. DB Time in ms | Avg. GUI Time in ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ZAT6A | DIA | 16.523 | 3,6 | 978,9 | 94,6 | 758,2 | 34,8 |
| ZST11 | DIA | 10.846 | 3,0 | 1.252,7 | 329,6 | 22,8 | 5,2 |
| ZU22_1 | DIA | 6.163 | 3,0 | 2.185,7 | 511,4 | 80,2 | 35,3 |
| SESSION_MANAGER | DIA | 19.004 | 1,8 | 433,5 | 115,2 | 104,6 | 221,5 |
| ZTCT_SCA_RF_PICK_AU | DIA | 13.778 | 1,7 | 570,3 | 76,3 | 69,8 | 0,8 |
| ZPACK_LABEL | DIA | 3.634 | 1,2 | 1.481,4 | 837,4 | 99,7 | 517,3 |
| ZR26B | DIA | 8.236 | 1,1 | 618,5 | 245,6 | 151,6 | 233,4 |
| ZR26A | DIA | 8.133 | 1,1 | 620,2 | 238,5 | 154,0 | 249,4 |
| VL06O | DIA | 6.944 | 1,1 | 709,6 | 283,9 | 285,2 | 26,2 |
| VL06F | DIA | 4.331 | 1,0 | 1.082,9 | 126,9 | 75,6 | 59,5 |

14.7% of the total response time in the above table is caused by customer transactions.

Workload by Transaction (Batch)

| Transaction | Dialog Steps | Total Resp. Time in % | Total Resp. Time in s | Total CPU Time in s | Total DB Time in s |
| --- | --- | --- | --- | --- | --- |
| R_JR_BTCJOBS_GENERATOR | 336 | 32,9 | 149.309,0 | 339,0 | 1.108,2 |
| ZRA00010 | 105 | 4,9 | 22.371,0 | 7.818,0 | 16.679,6 |
| ESH_EX_FU_DEMON | 1.941 | 3,2 | 14.730,0 | 903,0 | 625,3 |
| /BDL/TASK_SCHEDULER | 168 | 1,2 | 5.552,0 | 3,0 | 6,6 |
| RSCONN01 | 2.016 | 1,1 | 4.990,0 | 2.908,0 | 792,2 |
| ZR260002 | 23 | 1,1 | 4.980,0 | 4.091,0 | 1.065,6 |
| RMMRP000 | 60 | 0,9 | 4.204,0 | 185,0 | 430,5 |
| AQA00-BSW=======BSW_ORDERS==== | 343 | 0,9 | 4.099,0 | 3.547,0 | 675,4 |
| /UI5/APP_INDEX_CALCULATE | 678 | 0,8 | 3.848,0 | 1.579,0 | 1.821,8 |
| (BATCH) | 96.644 | 0,7 | 3.040,0 | 1.049,0 | 1.800,9 |

6.0% of the total response time in the above table is caused by customer transactions.

If response times are outside acceptable boundaries and you are unhappy with the performance of a transaction, contact your in-house developers about possible optimization potential and create a case using the

['Get Support' application](https://me.sap.com/getsupport) in SAP for Me ( [KBA 1296527](https://me.sap.com/notes/1296527) ). Within case creation, select Product: Customer Project Based Solution, and enter component SV-PERF.

### 8.2.2 Transactions by DB Load

The following transaction profiles list the transactions that have the greatest share in the database load, sorted by percentage of total database access times.

Database Load by Transactions (Dialog/HTTP(S) )

| Transaction | Type | Dialog Steps | Total DB Time in % | Avg. DB Time in ms |
| --- | --- | --- | --- | --- |
| ZAT6A | DIA | 16.523 | 15,8 | 758,2 |
| SESSION_MANAGER | DIA | 19.004 | 2,5 | 104,6 |
| VL06O | DIA | 6.944 | 2,5 | 285,2 |
| ZR26A | DIA | 8.133 | 1,6 | 154,0 |
| ZR26B | DIA | 8.236 | 1,6 | 151,6 |
| ZTCT_SCA_RF_PICK_AU | DIA | 13.778 | 1,2 | 69,8 |
| ZPICK627 | DIA | 105 | 1,0 | 7.377,8 |
| SQ00 | DIA | 6.275 | 0,9 | 115,8 |
| ZVL06P | DIA | 2.066 | 0,9 | 336,4 |
| ZT09 | DIA | 221 | 0,8 | 2.822,5 |

22.9% of the total database time in the above table is caused by customer transactions.

Database Load by Transactions (Batch)

| Transaction | Dialog Steps | Total DB Time in % | Total DB Time in s |
| --- | --- | --- | --- |
| ZRA00010 | 105 | 21,0 | 16.680,0 |
| /UI5/APP_INDEX_CALCULATE | 678 | 2,3 | 1.822,0 |
| (BATCH) | 96.644 | 2,3 | 1.801,0 |
| Z_CA_ARCH_SD_VBRK | 168 | 2,3 | 1.791,0 |
| RSBTCRTE | 84.950 | 1,4 | 1.119,0 |
| R_JR_BTCJOBS_GENERATOR | 336 | 1,4 | 1.108,0 |
| ZR260002 | 23 | 1,3 | 1.066,0 |
| AQA0TS-PLANNING=PLANNED_ORD=== | 20 | 1,1 | 836,0 |
| PPIO_ENTRY | 10 | 1,0 | 824,0 |
| RSCONN01 | 2.016 | 1,0 | 792,0 |

24.6% of the total database time in the above table is caused by customer transactions.

# 9 RFC Load by Initiating Action

The load in task type RFC is shown. In the workload monitor, this information is shown as 'Load from External Systems'. The calling system can be an application server of the system itself or any external system using the RFC interface. The 'Initial Action' is the calling program initiating the RFC. The total response time for each initial action is shown as an absolute value and as a percentage compared to the total RFC load considered in this table. The average times (per dialog step) are shown in milliseconds [ms].

Calls from external systems are shown if they account for at least 8h or 5% of the total RFC load. Local calls are shown if they account for at least 24h or 20% of the total RFC load.

Please refer to this [Guided Answer](https://ga.support.sap.com/dtp/viewer/#/tree/1412/actions/17616) on how to analyze RFC performance issues.

Load Overview

| Initial System | Load [s] | Load % |
| --- | --- | --- |
| Local system S4P | 106.052 | 96,66 |
| Sum of external systems | 3.665 | 3,34 |
| RFC load (sum of above) | 109.717 | 100,00 |
| RFC load in Performance Overview | 136.438 | 124,35 |
| Load of all task types in Performance Overview | 615.244 | 560,75 |

[IMAGE]

Top 20 RFC Calls From Local System - Average Times [ms]

| Initial System | Initial Action | Total Resp. Time in s | % of RFC Load | Avg. Response Time | Avg. CPU Time | Avg. DB Time | Avg. Roll Wait Time |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | SAPMSSY1 | 32.818 | 29,91 | 568,5 | 74,7 | 4,3 | 0,1 |
| S4P | /SDF/SMON_SCHEDULER | 31.959 | 29,13 | 4.565.575,9 | 169.055,7 | 85.849,0 | 3.744,7 |
| S4P | /BDL/TASK_PROCESSOR | 12.911 | 11,77 | 57.382,8 | 3.252,9 | 18.252,1 | 0,9 |
| S4P | MRP_NETCH_UK | 5.973 | 5,44 | 12.521,5 | 3.868,9 | 8.130,7 | 0,3 |
| S4P | /UI5/UPD_ODATA_METADATA_CACHE | 2.057 | 1,87 | 12.171,3 | 7.477,8 | 4.540,0 | 0,1 |
| S4P | R_JR_BTCJOBS_GENERATOR | 2.035 | 1,86 | 525,3 | 3,5 | 6,6 | 0,0 |
| S4P | ZSIT_POS_UPDATE_LOAD | 1.657 | 1,51 | 327,1 | 48,6 | 36,4 | 2,5 |
| S4P | LM01 | 1.404 | 1,28 | 105,2 | 11,8 | 11,1 | 0,1 |
| S4P | VL06O | 1.388 | 1,27 | 120,9 | 5,5 | 3,1 | 0,1 |
| S4P | VA01 | 1.013 | 0,92 | 494,2 | 18,1 | 35,1 | 0,1 |
| S4P | /UI5/APP_INDEX_CALCULATE | 1.002 | 0,91 | 292,6 | 101,1 | 88,9 | 0,2 |
| S4P | SAP_COLLECTOR_PERFMON_SWNCCOLL | 965 | 0,88 | 1.914,4 | 1.615,5 | 102,3 | 0,4 |
| S4P | TMS_0000000001TMS_TP_REFRESH_QUE | 937 | 0,85 | 173,9 | 25,4 | 22,9 | 0,5 |
| S4P | ZST11 | 696 | 0,63 | 81,8 | 13,5 | 16,2 | 0,1 |
| S4P | <BGRFC WATCHDOG> | 685 | 0,62 | 9,2 | 3,6 | 3,0 | 0,1 |
| S4P | RVV50R10C | 672 | 0,61 | 195,9 | 44,2 | 17,7 | 0,2 |
| S4P | ME22N | 642 | 0,59 | 645,3 | 38,9 | 32,8 | 0,1 |
| S4P | VA02 | 618 | 0,56 | 514,6 | 30,8 | 115,1 | 0,1 |
| S4P | VL01N | 603 | 0,55 | 183,5 | 31,6 | 20,8 | 0,1 |
| S4P | ZAT6A | 593 | 0,54 | 111,2 | 20,7 | 13,5 | 0,1 |

# 10 SAP System Operating S4P

| [IMAGE] | The daily operation of your system was analyzed. We detected some problems that may impair system operation and stability. |
| --- | --- |

| Rating | Check |
| --- | --- |
| [GREEN] | Availability based on Collector Protocols |
| [YELLOW] | Program Errors (ABAP Dumps) |
| [GREEN] | Update Errors |
| [YELLOW] | Table Reorganization |
| [GREEN] | Critical Number Ranges |

## 10.1 Availability based on Collector Protocols

[IMAGE]

A value of 100% means that the collector was available all day. "Available" in the context of this report means that at least one SAP instance was running. If the SAP collector was not running correctly, the values in the table and graphics may be incorrect.

To check these logs, call transaction ST03N (expert mode) and choose "Collector and Performance DB -> Performance Monitor Collector -> Log".

This check is based on the logs for job COLLECTOR_FOR_PERFORMANCEMONITOR that runs every hour.

The job does NOT check availability; it carries out only general system tasks such as collecting and aggregating SAP performance data for all servers/instances. The log does not contain any direct information about availability; it contains only information about the status of the hourly statistical data collection.

As of SAP Basis 6.40, system availability information is available in the CCMS (Computing Center Management System) of an SAP System, in Service Level Reporting of SAP Solution Manager.

This function is provided by the relevant Solution Manager Support Packages as an advanced development. For more information, refer to SAP Note 944496, which also lists the prerequisites that must be fulfilled before implementation can take place."

## 10.2 Update Errors

In a system running under normal conditions, only a small number of update errors should occur. To set the rating for this check, the number of active users is also taken into consideration. The following table contains the number of update errors detected.
[IMAGE]

We did not detect any problems.

## 10.3 Table Reorganization

When analyzing your database, we detected large or rapidly growing tables or indexes. 
 **Recommendation:** Implement the SAP Notes listed below to reduce the size of some of these tables or indexes. 
 **Background:** For more information about SAP Data Volume Management, see

[SAP DVM Community](https://pages.community.sap.com/topics/data-volume-management) .

| Table / Index Name | Size of Table / Index [MByte] | Recommended SAP Note |
| --- | --- | --- |
| TST03 | 10.380,0 | 48400, 130978, 16083 |

## 10.4 Program Errors (ABAP Dumps)

46 ABAP dumps have been recorded in your system in the period 27.04.2026 to 01.05.2026. ABAP dumps are generally deleted after 7 days by default. To view the ABAP dumps in your system, call transaction ST22 and choose Selection. Then select a timeframe.

| Date | Number of Dumps |
| --- | --- |
| 27.04.2026 | 3 |
| 28.04.2026 | 1 |
| 29.04.2026 | 3 |
| 30.04.2026 | 24 |
| 01.05.2026 | 15 |

| Name of Runtime Error | Dumps | Server (e.g.) | Date (e.g.) | Time (e.g.) |
| --- | --- | --- | --- | --- |
| UNCAUGHT_EXCEPTION | 1 | bsws4pap01_S4P_00 | 27.04.2026 | 07:58:51 |
| CALL_FUNCTION_CONFLICT_LENG | 2 | bsws4pap01_S4P_00 | 27.04.2026 | 08:55:18 |
| ASSERTION_FAILED | 2 | bsws4pap01_S4P_00 | 29.04.2026 | 09:40:58 |
| SESSIONMEM_QUOTA_WARNING | 4 | bsws4pap01_S4P_00 | 30.04.2026 | 11:47:44 |
| TSV_TNEW_PAGE_ALLOC_FAILED | 5 | bsws4pap01_S4P_00 | 30.04.2026 | 11:47:53 |
| SYNTAX_ERROR | 3 | bsws4pap01_S4P_00 | 01.05.2026 | 15:26:56 |
| CONVT_NO_NUMBER | 23 | bsws4pap01_S4P_00 | 01.05.2026 | 15:58:17 |
| RAISE_EXCEPTION | 6 | bsws4pap01_S4P_00 | 01.05.2026 | 16:53:51 |

It is important that you monitor ABAP dumps using transaction ST22 on a regular basis. If ABAP dumps occur, you should determine the cause as soon as possible.

**Based on our analysis, we found several ABAP dumps that need your attention. Evaluate and resolve the above dumps. If you cannot find a solution, create a case using the** [Get Support application](https://me.sap.com/getsupport) **in SAP for Me (** [KBA 1296527](https://me.sap.com/notes/1296527/E) **).**

## 10.5 Critical Number Ranges

We have checked the usage of valid ABAP number ranges and found no issues.

# 11 Security

| [IMAGE] | Critical security issues were found in your system. See the information in the following sections. |
| --- | --- |

| Rating | Check | System ID |
| --- | --- | --- |
| [GREEN] | System Recommendations (HANA) | H4P |
| [GREEN] | Maintenance Status of current SAP HANA Database Revision | H4P |
| [YELLOW] | SAP HANA System Privilege DATA ADMIN | H4P |
| [GREEN] | SAP HANA Password Policy | H4P |
| [GREEN] | SAP HANA Audit Trail | H4P |
| [GREEN] | SAP HANA SQL Trace Level | H4P |
| [GREEN] | SAP HANA Network Settings for Internal Services | H4P |
| [RED] | Activation Status and Validity of User SYSTEM | H4P |
| [GREEN] | System Recommendations (ABAP) | S4P |
| [GREEN] | Age of Support Packages | S4P |
| [GREEN] | Default Passwords of Standard Users | S4P |
| [GREEN] | Control of the Automatic Login User SAP* | S4P |
| [GREEN] | Protection of Passwords in Database Connections | S4P |
| [YELLOW] | ABAP Password Policy | S4P |
| [GREEN] | RFC Gateway Security | S4P |
| [GREEN] | Message Server Security | S4P |
| [RED] | Critical authorizations, which allow to do anything | S4P |
| [RED] | Critical authorizations, which should not be used in production | S4P |
| [YELLOW] | Critical authorizations, which should only see very limited use in production | S4P |

## 11.1 SAP HANA Database H4P

### 11.1.1 SAP HANA System Privilege DATA ADMIN

#### 11.1.1.1 Users with DATA ADMIN Privilege

Users in your SAP HANA database have the DATA ADMIN system privilege. 
 The count considers direct grants to the users as well as indirect grants using roles. Users are counted as activated if the validity time range matches the time of the evaluation and the user is not deactivated. 
 The SYSTEM and _SYS_REPO users are not considered, because these users have the DATA ADMIN privilege by design and the privilege cannot be revoked from these users.

| Number of Additional Users with DATA ADMIN Privilege | 1 |
| --- | --- |

DATA ADMIN provides the authorization to modify and delete every object in every schema.

**Recommendation:** Remove the DATA ADMIN privilege from all user accounts except the SYSTEM und _SYS_REPO users.

### 11.1.2 Activation Status and Validity of User SYSTEM

The activation status and validity dates (VALID FROM and VALID TO) of user SYSTEM have been checked in system table USERS.

| Rating | Check |
| --- | --- |
| [RED] | User SYSTEM is currently active and valid. |

Active standard users are an easy and widely used target for hacking attacks since they are available in every system. Furthermore, the user SYSTEM is like a super user with very powerful user authorizations that cannot be revoked.

**Recommendation:** Review the current usage of user SYSTEM and set up and test a user and role concept, so that the use of user SYSTEM becomes obsolete.

Deactivate the user account with the SQL statement: 
 ALTER USER SYSTEM DEACTIVATE USER NOW.

To prevent misuse of user SYSTEM, activate related audit policies in your SAP HANA system as described in the SAP HANA Administration Guide.

## 11.2 ABAP Stack of S4P

### 11.2.1 ABAP Password Policy

If password login is allowed for specific instances only, the password policy is checked only for these instances.

#### 11.2.1.1 Validity of Initial Passwords

| Rating | Parameter | Instance | Current Value(s) |
| --- | --- | --- | --- |
| [YELLOW] | login/password_max_idle_initial | bsws4pap01_S4P_00 | 0 |

Initial passwords are valid for more than 14 days.

**Recommendation:** Proceed as follows: 
 -- Handle users of type C (Communication) with initial passwords because they will be locked if the above profile parameter is set. 
 Use transaction SUIM/report RSUSR200 in each client to find users of type C (Communication). 
 If these users are active and in use, switch the user type to B (System). This has no negative effect. 
 – Restrict the password validity to 14 days or less. Note that the value 0 grants unlimited validity. 
 - For more information, see SAP Note [862989](https://launchpad.support.sap.com/#/notes/862989) and the [Profile Parameters for Logon and Password (Login Parameters)](http://help.sap.com/saphelp_nw70/helpdata/en/22/41c43ac23cef2fe10000000a114084/frameset.htm) section, either on SAP Help Portal or in the SAP NetWeaver AS ABAP Security Guide.

### 11.2.2 Users with Critical Authorizations

For more information about the following check results, see SAP Note [863362](https://launchpad.support.sap.com/#/notes/863362) .

**Recommendation:** Depending on your environment, review your authorization concept and use the Profile Generator (transaction PFCG) to correct roles and authorizations. You can use the User Information System (transaction SUIM) to check the results. For each check, you can review the roles or profiles that include the authorization objects listed in the corresponding section.

#### 11.2.2.1 Critical authorizations, which allow to do anything

##### 11.2.2.1.1 Super User Accounts

Users with authorization profile SAP_ALL have full access to the system. There should be a minimum of such users. The number of users with this authorization profile is stated for each client.

| Client | No. of Users Having This Authorization | No. of Valid Users | Rating |
| --- | --- | --- | --- |
| 000 | 9 | 11 | [RED] |
| 100 | 15 | 413 | [RED] |

**Authorization profile:** 
 SAP_ALL

##### 11.2.2.1.2 Users Authorized to Debug / Replace

This authorization provides access to data and functions, since any authorization check that is built in ABAP can be bypassed. In addition, you can change data during processing, which may lead to inconsistent results. The specified number of users for each client have the checked authorization.

**Caution:** As of ABAP Release 7.57, the additional authorization object S_DBG is available that you can use to fine-tune the change authorizations in the debugger. If both authorization objects are configured for a user, the user receives the broader authorization from both authorization objects. This new authorization object is not yet checked in this report.

| Client | No. of Users Having This Authorization | No. of Valid Users | Rating |
| --- | --- | --- | --- |
| 100 | 17 | 413 | [RED] |

**Authorization objects:** 
 Object 1: S_DEVELOP with ACTVT=02 (change) and OBJTYPE=DEBUG

Note: If you do not want to disable development in your system, you have to exclude the authorization for OBJTYPE=DEBUG with ACTVT=02 from roles and only allow any other object type for S_DEVELOP. This means that development and debugging with visualization is still possible. 
 You can achieve this by adding two authorizations to the object S_DEVELOP: one with all object types except for DEBUG and all activities, and another for the object type DEBUG only and all activities except for 02.

#### 11.2.2.2 Critical authorizations, which should not be used in production

##### 11.2.2.2.1 Users Authorized to Change or Display all Tables

Unauthorized access to sensitive data is possible if too many users have this authorization. The specified number of users for each client have the checked authorization.

| Client | No. of Users Having This Authorization | No. of Valid Users | Rating |
| --- | --- | --- | --- |
| 100 | 64 | 413 | [RED] |

**Authorization objects:** 
 Object 1: S_TCODE with TCD=SE16, TCD=SE16N, TCD=SE17, TCD=SM30, or TCD=SM31 
 Object 2: S_TABU_DIS with ACTVT = 03 or 02 and DICBERCLS = *

#### 11.2.2.3 Critical authorizations, which should only see very limited use in production

##### 11.2.2.3.1 Users Authorized to Reset/Change User Passwords

The following users are allowed to change and reset the passwords of users. This is very risky because any of these users could change the password and log on themselves with another user. The only consequence is that the "real user" would no longer be able to log on because the password would have been changed. However, this normally results in the password being reset, because there is a chance that the "real user" might have forgotten the correct password.

| Client | No. of Users Having This Authorization | No. of Valid Users | Rating |
| --- | --- | --- | --- |
| 100 | 61 | 413 | [YELLOW] |

**Authorization objects:** 
 Object 1: S_TCODE with TCD=SU01 or TCD=OIBB or TCD=OOUS or TCD=OPF0 or TCD=OPJ0 or TCD=OVZ5 
 Object 2: S_USER_GRP with ACTVT=05

# 12 Software Change and Transport Management of S4P

| [IMAGE] | Software change management issues were found in your system. See the information in the following sections. |
| --- | --- |

## 12.1 SAP Netweaver Application Server ABAP of S4P

| Rating | Check Performed |
| --- | --- |
| [GREEN] | Number of Changes |
| [YELLOW] | Emergency Changes |
| [GREEN] | Failed Changes |

### 12.1.1 Number of Changes

Performing changes is an important cost driver for the IT department. It is only acceptable to make a large number of software and configuration changes in exceptional situations, such as during go-live for an implementation project.

The following diagram shows the number of changes per day that were performed in the SAP system in the last week. The data is extracted from the Change Diagnostics application in SAP Solution Manager. The changes are grouped into "Software Maintenance" (such as support or enhancement packages), "Parameter" (instance, database, operating system), "Transport Requests", "SAP Notes", and "Miscellaneous" (such as security settings).
[IMAGE]

| Date | Security | Software Maintenance | Parameter | Transport Requests | SAP Notes | Miscellaneous |
| --- | --- | --- | --- | --- | --- | --- |
| 28.04.2026 | 0 | 0 | 0 | 3 | 0 | 0 |
| 29.04.2026 | 0 | 0 | 0 | 2 | 2 | 0 |
| 30.04.2026 | 1 | 0 | 0 | 0 | 0 | 0 |
| 01.05.2026 | 0 | 0 | 0 | 1 | 0 | 0 |

### 12.1.2 Number of Transport Requests

The following diagram contains information about the number of transport requests per day that were imported into the SAP system in the last week.
[IMAGE]

| Date | Workbench and Relocation Requests | Customizing Requests | Transport of Copies |
| --- | --- | --- | --- |
| 28.04.2026 | 3 | 0 | 0 |
| 29.04.2026 | 2 | 0 | 0 |
| 01.05.2026 | 1 | 0 | 0 |

### 12.1.3 Number of Transported Objects

The following diagram contains information about the number of objects per day that was imported into the SAP system in the last week.
[IMAGE]

| Date | Objects in Workbench and Relocation Requests | Objects in Customizing Requests | Objects in Transport of Copies |
| --- | --- | --- | --- |
| 28.04.2026 | 6 | 0 | 0 |
| 29.04.2026 | 91 | 0 | 0 |
| 01.05.2026 | 1 | 0 | 0 |

### 12.1.4 Emergency Changes

We analyzed the number of emergency changes in system S4P in the last week.

| Rating | Item | Value | Explanation |
| --- | --- | --- | --- |
| [GREEN] | Transport requests created in production | 0 | Number of transport requests; created or released in production. |
| [YELLOW] | Transport requests with short transition time | 6 | The duration between the export from the development system and the import into the production system was shorter than one day. |
| [GRAY] | Total number of transport requests | 6 | Total number of transport requests in production. |

#### Transport Requests with a short Transition Time

| Request | Export from DEV | Import in PRD |
| --- | --- | --- |
| S4DK902937 | 28.04.2026 12:31:32 | 28.04.2026 12:37:34 |
| S4DK902939 | 28.04.2026 10:19:54 | 28.04.2026 10:22:47 |
| S4DK902946 | 28.04.2026 11:29:26 | 28.04.2026 11:45:48 |
| S4DK902950 | 29.04.2026 10:35:32 | 29.04.2026 10:38:58 |
| S4DK902952 | 29.04.2026 11:08:12 | 29.04.2026 11:10:41 |
| S4DK902960 | 01.05.2026 11:42:06 | 01.05.2026 11:46:10 |

**Recommendation:** Transport requests with a short transition time of less than one day have occurred in the last week. These transports may not have been tested sufficiently. 
 Make sure that they did not cause problems in production.

### 12.1.5 Failed Changes

In this check, we analyzed the number of failed changes in system S4P during the last week.

| Rating | Item | Value | Explanation |
| --- | --- | --- | --- |
| [GREEN] | Transport requests with import errors | 0 | Number of transport requests with import errors that were not resolved within one hour. |
| [GREEN] | Overtakers and bypassed transport requests | 63 | If an old object version overwrites a newer one we count this as a transport sequence error. We count both the overtaker transport and the bypassed transport. Each transport is only counted once. |
| [GRAY] | Total number of transport requests | 6 | Total number of transport requests that were imported or released in production within the last week. |

# 13 Financial Data Quality

| [IMAGE] | After execution of the “quick” consistency checks and execution of the main reconciliation report, issues were identified that require your attention. |
| --- | --- |

The current Financial Data Quality chapter contains essential information about the quality and consistency of your financial data.

This chapter is structured with three subchapters: “Financial Data Integrity”, “Financial Data Management”, “Reconciliation for S/4HANA”. The first two chapters are based on “quick” checks of different financial modules. The latter chapter displays the status and results of the main reconciliation checks.

It is important to understand that, due to the technical limitation of the automated data collection, we can cover only a limited result list in your system using the “quick” consistency checks. The reconciliation checks are the main sources of data for our financial data quality analysis and should be executed. These checks ensure full transparency at the consistency level of your financial data.

## 13.1 Financial Data Integrity

Our “quick” checks identified no inconsistencies in the area of Financial Data Integrity that require your attention.

## 13.2 Financial Data Management

Our “quick” checks identified no inconsistencies in the area of Financial Data Management that require your attention.

## 13.3 Reconciliation for S/4HANA

This section displays data from the reconciliation checks in the area of Finance.

# 14 Data Volume Management (DVM)

Data relevant for Data Volume Management was collected on system S4P and stored in the SDCCN download. If you gave your consent, this data has been sent to SAP for further analysis. After the analysis has finished, you can find the analysis result in [SAP for Me](https://me.sap.com/) via the link shown in the respective column in the table below. 
 
 Note: 
 For more information about DVM cloud-based service delivery, see [Knowledge Base Article 2716655](https://me.sap.com/notes/2716655) .

| Link to SAP Support Launchpad |
| --- |
| https://launchpad.support.sap.com/#/dataoverview |

# 15 Upgrade Planning

| [IMAGE] | We have checked your system for topics related to upgrades. The topics below may need your attention. |
| --- | --- |

| Rating | Check |
| --- | --- |
| [YELLOW] | Compatibility Scope information in EarlyWatch Alert has been suspended |

## 15.1 Compatibility Scope information in EarlyWatch Alert has been suspended

The compatibility scope analysis has been modernised into a single report which is part of the simplification item check report. Details to run the report and check your current usage of compatibility packs which come with limited use rights, can be found in [SAP note 2399707](https://me.sap.com/notes/2399707) .

Refer to [SAP Note 2269324](https://me.sap.com/notes/2269324) for more information on compatibility packages and their expiry dates.

# 16 SAP HANA Database H4P

| [IMAGE] | We have checked your SAP HANA environment and found some issues that might have a negative impact on your overall system stability and performance. Review the report carefully and implement our recommendations. |
| --- | --- |

| Rating | Check |
| --- | --- |
| [YELLOW] | SAP HANA Stability and Alerts |
| [YELLOW] | SAP HANA Database Configuration |
| [GREEN] | SAP HANA Resource Consumption |
| [GREEN] | SAP HANA Workload and Performance |
| [GREEN] | Size and Growth |
| [YELLOW] | Administration |

## 16.1 Overview

The tables below provide an overview of your current SAP HANA database configuration.

DB Version / Start Time

| Current SAP HANA DB Version | Build Branch | Start Time | Usage |
| --- | --- | --- | --- |
| 2.00.079.05 | fa/hana2sp07 | 07.03.2026 16:47:19 | CUSTOM |

Technical Instances

| Host | Database Name | System ID | Instance | Active | Daemon | Start Time | Time Zone | Nameserver Role | Indexserver Role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bswprddb01 | H4P | H4P | 00 | yes | yes | 2026-03-07 16:47:00.827 | BST | MASTER | MASTER |

Hardware Settings - General Data

| Host | Physical Hostname | Manufacturer | Model |
| --- | --- | --- | --- |
| bswprddb01 | bswprddb01 | Microsoft Corporation | Virtual Machine |

Hardware Settings - CPU and Memory Data

| Host | CPU Type | CPU Frequency | CPU Cores | Threads | Sockets | NUMA Nodes | Physical Memory [GB] | Allocation Limit [GB] | Swap Space [GB] |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bswprddb01 | Intel(R) Xeon(R) Platinum 8280L CPU @ 2.70GHz | 2.693 | 32 | 64 | 2 | 2 | 503,9 | 484,1 | 2,0 |

Operating System Details

| Host | Operating System PPMS Name | Operating System Version | Operating System Kernel | NOFILES Limit | OPEN_FILE Limit |
| --- | --- | --- | --- | --- | --- |
| bswprddb01 | LINUX_X86_64 | SUSE Linux Enterprise Server 15 SP5 | 5.14.21-150500.55.136-default | 1.048.576 | 9.223.372.036.854.775.800 |

HANA Feature Usage

| Usage | Installed / used | Additional data | SAP Note |
| --- | --- | --- | --- |
| Multitenant Database Containers (MDC) | Yes | System ID: H4P | 2101244 |
| Dynamic Tiering | No |  | 2140959 |
| Enterprise Performance Management Add-On (EPM MDS) | No |  | 2456225 |
| Embedded liveCache | No |  | 2593571 |
| Streaming Server | No |  |  |
| Advanced Function Libraries | No |  |  |
| XS Advanced | No |  |  |
| Embedded Statisticsserver active | Yes |  | 2147247 |
| System Replication | No |  | 1999880 |
| Smart Data Access (SDA) | No |  | 2180119 |
| Smart Data Integration (SDI) | No |  | 2400022 |
| Smart Data Streaming (SDS) | No |  | 2367236 |
| Persistent Memory | No |  | 2700084 |
| Fast Restart Option | No |  | 2700084 |
| Data Aging | No |  | 2416490 |
| Extension Node | No |  | 2741690 |
| Workload Classes | Yes |  | 2222250 |
| Native Storage Extension (NSE) | Yes |  | 2775588 |
| Multi Dimensional Expressions (MDX) | No |  |  |
| Multi Dimensional Services (MDS) | No |  | 2670064 |
| Activated Audit Policies | Yes | 29 | 2159014 |
| Sequences | Yes | 11 | 2600095 |
| Triggers | Yes | 22 (22 internal) | 2800020 |
| Fulltext Indexes | Yes | 499 | 2800008 |
| Fuzzy Search Indexes | Yes | 557 | 2800008 |
| Document Store Collections | No |  | 2477204 |
| Text Analysis Tables | Yes | 1 | 2800008 |
| Text Mining Tables | No |  | 2800008 |
| Series Tables | No |  |  |
| Table Replicas | No |  | 2340450 |
| Volume Encryption | No |  | 2159014 |
| Incremental Data Backup | No |  | 1642148 |
| Differential Data Backup | No |  | 1642148 |
| Data Snapshot Backup | No |  | 1642148 |

HANA System Settings

| Name | Value | SAP Note |
| --- | --- | --- |
| Users with individual Statement Memory Limit | 29 | 1999997 |
| Statement Hints | 2 | 2400006 |
| Database Log Mode | normal (DEFAULT) | 1642148 |
| Automatic Log Backup | yes (DATABASE) | 1642148 |
| Query Result Cache | no (DEFAULT) | 2014148 |
| Global Auditing State | true (DATABASE) | 1991634 |
| Parallelism of Table Preload | 6 (DEFAULT) | 2127458 |
| Table Preload during Startup | true (DEFAULT) | 2127458 |

HANA Update Information

| Date | Version |
| --- | --- |
| 30.11.2021 | 2.00.055.00.1615413201 |
| 21.10.2023 | 2.00.073.00.1695288802 |
| 31.08.2025 | 2.00.079.05.1749057886 |

## 16.2 SAP HANA Stability and Alerts

### 16.2.1 SAP HANA Alerts

| [GRAY] | SAP HANA alerts have been issued for the monitored timeframe. |
| --- | --- |

SAP HANA collects system information periodically and issues alerts of different priority levels according to predefined thresholds. These alerts can be used to monitor the performance and stability of the SAP HANA database. Possible alert priorities are: 
 1 – Information 
 2 – Low 
 3 – Medium 
 4 – High 
 5 – Statistics Server Alert

The following "Alerts" table shows SAP HANA alerts that reached at least medium priority during the monitored timeframe. It also shows how often an alert was created and the highest priority for this particular alert.

The "Recommendations" table lists recommendations for the alerts found and refers to SAP KBA Notes if available. Further details and recommendations for SAP HANA alerts are available in the relevant sections of the report.

Alerts

| Alert ID | Alert | No. of Occurrences | Highest Rating |
| --- | --- | --- | --- |
| 65 | Determines whether or not the most recent log backup terminates in the given time. | 11 | 3 |

Recommendations

| Alert ID | General Recommendation | KBA |
| --- | --- | --- |
| 65 | Investigate why the log backup runs for too long, and resolve the issue. See SAP Note 2081845. | 2081845 |

**Recommendation:** Monitor SAP HANA alerts in the system closely to get an overview of the SAP HANA system status. React to warnings and problems visible in the alerts in due time. If you require support, create a case using the Get Support application in SAP for Me ( [KBA 1296527](https://me.sap.com/notes/1296527) ). Within case creation, select Product: Customer Project-Based Solution, and enter the component HAN-DB*. 
 For details, refer to the [SAP HANA Administration Guide](https://help.sap.com/viewer/6b94445c94ae495c83a19646e7c3fd56/2.0.05/en-US) and to the SAP Note [2445867 How-To: Interpreting and Resolving SAP HANA Alerts](https://me.sap.com/notes/2445867) .

### 16.2.2 SAP HANA Service Restarts

| [GREEN] | No critical issues with SAP HANA service restarts were detected. |
| --- | --- |

We did not find critical issues with SAP HANA service restarts.

### 16.2.3 SAP HANA DB Availability

The SAP HANA DB availability was based on the availability of the index server as logged in the daemon trace file.

No critical problems occurred regarding the availability of SAP HANA services.

## 16.3 SAP HANA Database Configuration

### 16.3.1 Parameter Recommendation

| [GRAY] | Check parameter settings |
| --- | --- |

Some parameters are not set as recommended, or there are parameters deviating from default values.

This table highlights the parameters that were checked with regard to their impact on system performance and stability.

Important SAP HANA Parameters

| Location | Parameter | Layername | Current Value | Recommended Value | Rating | SAP Note |
| --- | --- | --- | --- | --- | --- | --- |
| global.ini [memorymanager] | disable_16kb_ha_defrag |  |  | true | [YELLOW] | 1999997 |
| global.ini [memorymanager] | min_segment_size | DEFAULT | 0 | 4 | [YELLOW] | 3680406 |
| indexserver.ini [memorymanager] | min_segment_size |  |  | 0 | [YELLOW] | 3680406 |
| indexserver.ini [sql] | max_table_count_in_statement | DATABASE | 4095 | <restore default> | [YELLOW] | 1969700 |
| indexserver.ini [transaction] | suspended_cursor_lifetime | DEFAULT | 720 | <between 1440 and 14400> [4320] | [YELLOW] | 2800055 |
| scriptserver.ini [memorymanager] | min_segment_size |  |  | 0 | [YELLOW] | 3680406 |

**Recommendation:** Set the SAP HANA parameters to the recommended value in the table.

**Note:** The recommendation "<restore default>" is assigned if a custom parameter value is equal to the SAP HANA default and therefore not explicitly required. In that case the default should be restored. Use the SQL command "ALTER SYSTEM ALTER CONFIGURATION ( '<filename>', '<layername>' ) UNSET ( '<section>', '<parameter name>' )". See SAP Note [2186744](https://launchpad.support.sap.com/#/notes/2186744) for details.

Be aware that for a proper tenant DB parameter setting, the parameters configured on the system DB side must also be double-checked. Otherwise, critical parameters can be set in the system DB that appear as default values on the tenant side. Default values are only reported by the parameter check if an explicit recommendation exists, therefore, critical settings can be missed by focusing only on the tenant DB parameter check.

The table "SAP HANA Parameters deviating from default" lists parameters deviating from default. These parameters do not belong to the set of recommended parameters, they represent parameters that are not set to DEFAULT value. 
 In the list below, there might be parameters that needed to be changed, but also parameters that were supposed to be set back to their default values (as for special settings only in certain SAP HANA revisions) but were forgotten. The purpose of this output is only to report those parameters to bring them to your attention so you can check them.

SAP HANA Parameters deviating from default

| Location | Parameter | Layername | Current Value |
| --- | --- | --- | --- |
| global.ini [backup] | enable_log_backup_compression | DATABASE | true |
| global.ini [persistence] | stop_async_gc_in_shutdown | DATABASE | FALSE |
| global.ini [sql] | hex_enable_distributed_query_processing | DATABASE | FALSE |
| indexserver.ini [lobhandling] | garbage_collect_interval_s | DATABASE | 0 |

### 16.3.2 SAP HANA Workload Management

| [GRAY] | SAP HANA workload parameters need to be adjusted. |
| --- | --- |

Workload management in SAP HANA allows you to balance and manage all workload types for optimal throughput and response times. The available workload management parameters limit resource consumption (e.g. CPU, threads, memory) for certain operations. The recommended values depend on available memory resources and on the number of CPU threads of the database server (also referred to as number of logical CPUs). For general information, refer to SAP Note [2222250](https://launchpad.support.sap.com/#/notes/2222250) (FAQ: SAP HANA Workload Management).

If the current value deviates from the default, we check whether the current value is within the interval specified by the minimum and maximum formula.

The recommendations below are only valid if you have one tenant. In case of several tenants adjust the parameters accordingly with the help of the parameter script "HANA_Configuration_Parameters_*" of SAP Note [1969700](https://me.sap.com/notes/1969700) . It allows to simulate the workload parameters for specific tenants (based on 'reserved' CPU Threads for a tenant).

| Location | Parameter | Layername | Current Value | Recommended Value | Rating |
| --- | --- | --- | --- | --- | --- |
| indexserver.ini [metadata] | max_num_recompile_threads | DEFAULT | <HANA kernel> | <between 6 and 32> | [YELLOW] |

Some workload parameters are not set correctly.

**Recommendation:** We generally recommend setting the minimum value for initial setup. However, depending on the overall load situation, customer-specific settings may lead to better results and need to be evaluated.

### 16.3.3 Disk Configuration

| [GREEN] | There are no disk configuration issues. |
| --- | --- |

| Disk ID | Device ID | File system | Host | Path | Usage |
| --- | --- | --- | --- | --- | --- |
| 1 | 630585 | xfs | bswprddb01 | /hana/data/H4P/ | DATA |
| 2 | 362856 | xfs | bswprddb01 | /usr/sap/H4P/HDB00/backup/data/ | DATA_BACKUP |
| 3 | 72881 | xfs | bswprddb01 | /hana/log/H4P/ | LOG |
| 4 | 362856 | xfs | bswprddb01 | /usr/sap/H4P/HDB00/backup/log/ | LOG_BACKUP+CATALOG_BACKUP |
| 5 | 362856 | xfs | bswprddb01 | /usr/sap/H4P/HDB00/bswprddb01/ | TRACE |

There are no disk configuration issues. Data and log data is stored on separate physical devices.

## 16.4 Size and Growth

Monitoring the size and growth of the HANA database is crucial for system stability and performance. In terms of stability, the growth on disk is shown. In terms of performance, the size of row and column tables as well as the size of delta areas in column tables are analyzed.

### 16.4.1 Disk Usage

| [GREEN] | Percentage of free disk space > 20% |
| --- | --- |

The table below shows the disk occupancy with respect to the partitions and their usage types. If the percentage of free disk space falls below 10%, an intermediate action has to be performed. Otherwise, there is a risk of standstill in the SAP HANA database.

Disk Space

| Host | Available Disk Space [GB] | Used Disk Space [GB] | Percentage of free Disk Space | Usage Types | File system | Rating |
| --- | --- | --- | --- | --- | --- | --- |
| bswprddb01 | 511,75 | 40,99 | 92,0 | CATALOG_BACKUP+DATA_BACKUP+LOG_BACKUP+TRACE | xfs | [GREEN] |
| bswprddb01 | 1.023,48 | 574,50 | 43,9 | DATA | xfs | [GREEN] |
| bswprddb01 | 383,80 | 85,05 | 77,8 | LOG | xfs | [GREEN] |

The graph shows the history of disk space usage.
[IMAGE]

### 16.4.2 Database Growth

The graph shows the database size and growth based on the size of data volumes. 
 Total Size: Amount of data allocated by SAP HANA database on data volumes. 
 Used Size: Amount of used data by SAP HANA database on data volumes.
[IMAGE]

To access the database growth chart in SAP EarlyWatch Alert Workspace, click [here](https://me.sap.com/ewa/dashboard/dbSizeDetail/S4P_0021220331_000000000800631194) .

### 16.4.3 Tables and Indexes

The table below displays the number of column and row tables together with their indexes.

Tables and Indexes

| Objects | Number |
| --- | --- |
| Column Tables | 159.251 |
| Indexes of Column Tables | 164.984 |
| Row Tables | 21.042 |
| Indexes of Row Tables | 923 |

### 16.4.4 Size of Database Schemas

The following table lists the size of schemas in the SAP HANA database.

Size of SAP HANA Schemas

| Host | Schema Name | Memory Size [MB] | Disk Size [MB] | LOB Size [MB] | Store Type |
| --- | --- | --- | --- | --- | --- |
| bswprddb01 | SAPSP4 | 126.458 | 374.116 | 217.456 | Column store |
| bswprddb01 | _SYS_REPO | 996 | 5.855 | 4.933 | Column store |
| bswprddb01 | SAPSP4 | 2.901 | 18.630 | 15.730 | Row store |

### 16.4.5 SAP HANA Row Store

#### Row Store Size

| [GREEN] | The allocated row store size is below the technical limit. |
| --- | --- |

The table below shows the size of the SAP HANA row store. The row store contains mainly SAP Basis and application statistics tables. The rating indicates whether the technical size limit will be reached in the near future.

The size of the row store generally has a direct impact on the start-up time of the SAP HANA database. This is relevant for system start-up and for recovery. We recommend that you keep the row store at an optimum size by performing housekeeping for large Basis tables (SAP Note 2388483) and, where feasible, moving large application tables from row store to column store.

Row Store Size (MB)

| Host | Port | Allocated Size (MB) | Rating |
| --- | --- | --- | --- |
| bswprddb01 | 30003 | 3.584 | [GREEN] |

#### Largest Row Store Tables

The table lists the largest tables according to total disk size. The size of the memory and the number and type of LoBs are also shown. The LOBs are marked with either "H" (Hybrid) or "M" (Memory) and the number of the existing LoB columns.

| Schema Name | Table Name | Total Disk Size (MB) | Size in Memory (MB) | Max Size in Memory (MB) | Nr. of Records | LOB Size (MB) | LOB Details |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SAPSP4 | TST03 | 10.380 | 83 | 97 | 925.792 | 10.282 | H1 |
| SAPSP4 | FPLAYOUTT | 3.272 | 1 | 1 | 12.102 | 3.271 | H2 |
| SAPSP4 | FPCONTEXT | 905 | 2 | 2 | 6.471 | 902 | H1 |
| SYS | RS_COLUMNS_ | 807 | 781 | 807 | 2.801.232 | 0 | 0 |
| SAPSP4 | ENHHEADER | 738 | 3 | 4 | 27.091 | 735 | H1 |
| SYS | CS_COLUMNS_ | 705 | 619 | 705 | 2.278.841 | 0 | 0 |
| SAPSP4 | ENHOBJCONTRACT | 300 | 0 | 0 | 69 | 300 | H1 |
| SYS | P_OBJECTDEPENDENCY_ | 244 | 239 | 244 | 1.960.561 | 0 | 0 |
| SAPSP4 | ENHSPOTHEADER | 212 | 2 | 3 | 17.934 | 209 | H1 |
| SAPSP4 | TBTCJOBLOG7 | 198 | 177 | 198 | 1.095.986 | 0 | 0 |

For large SAP Basis tables, remove obsolete data regularly according to SAP Note [2388483](https://launchpad.support.sap.com/#/notes/2388483) .

### 16.4.6 SAP HANA Column Store

#### Largest Column Tables (Size)

The table lists the largest tables according to total disk size. The size of the memory and the number and type of LoBs are also shown. The LOBs are marked with either "H" (Hybrid) or "M" (Memory) and the number of the existing LoB columns.

| Schema Name | Table Name | Nr. of Partitions | Total Disk Size (MB) | Size in Memory (MB) | Max. Size in Memory (MB) | LOB Size (MB) | LOB Details |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SAPSP4 | SOFFCONT1 | 1 | 139.370 | 600 | 600 | 138.766 | H1 |
| SAPSP4 | REPOLOAD | 1 | 33.686 | 175 | 175 | 33.508 | H2 |
| SAPSP4 | REPOSRC | 1 | 11.998 | 2.586 | 2.586 | 9.403 | H1 |
| SAPSP4 | ECTD_XML_STR | 1 | 10.895 | 22 | 22 | 10.873 | H1 |
| SAPSP4 | WBCROSSGT | 1 | 9.681 | 9.765 | 9.765 | 0 | 0 |
| SAPSP4 | CDPOS | 1 | 9.389 | 9.491 | 9.491 | 0 | 0 |
| SAPSP4 | SWWCNTP0 | 1 | 8.609 | 8.657 | 8.656 | 0 | 0 |
| SAPSP4 | ZI47 | 1 | 6.180 | 7.049 | 7.051 | 0 | 0 |
| SAPSP4 | DDNTT | 1 | 5.834 | 535 | 535 | 5.286 | H1 |
| SAPSP4 | BALDAT | 1 | 5.332 | 5.342 | 5.342 | 0 | 0 |

For large SAP Basis tables, remove obsolete data regularly according to SAP Note [2388483](https://launchpad.support.sap.com/#/notes/2388483) .

#### Largest Non-partitioned Column Tables (Records)

| [GREEN] | The number of records in column-based table partitions is not critical. |
| --- | --- |

The table below shows the largest non-partitioned column tables in terms of the number of records.

Largest Non-partitioned Column Tables According To Records

| Schema Name | Table Name | Records (Total) | Weekly Record Growth [%] | Load Status | Rating |
| --- | --- | --- | --- | --- | --- |
| SAPSP4 | WBCROSSGT | 211.656.973 | 0,00 | PARTIALLY | [GREEN] |
| SAPSP4 | ZI47 | 167.206.689 | 0,00 | PARTIALLY | [GREEN] |
| SAPSP4 | EDID4 | 151.852.482 | 0,53 | PARTIALLY | [GREEN] |
| SAPSP4 | D010TAB | 138.639.338 | 0,00 | PARTIALLY | [GREEN] |
| SAPSP4 | CDPOS | 136.285.673 | 0,19 | PARTIALLY | [GREEN] |
| SAPSP4 | PRCD_ELEMENTS | 114.482.635 | 0,26 | PARTIALLY | [GREEN] |
| SAPSP4 | ACDOCA | 78.680.556 | 0,16 | PARTIALLY | [GREEN] |
| SAPSP4 | KONV | 59.237.825 | 0,00 | PARTIALLY | [GREEN] |
| SAPSP4 | ACCTCR | 58.633.686 | 0,24 | FULL | [GREEN] |
| SAPSP4 | ZI40_ARKIV | 57.941.191 | 0,00 | NO | [GREEN] |

The table partitions can handle the number of the records.

### 16.4.7 Native Storage Extension

The table below lists tables for which Native Storage Extension or Data Aging is configured. It also lists on which layer (table, partition, column) the page loadable is defined. 
 If the loadable page is enabled at column level, the corresponding column names are listed. If a table is listed multiple times, the configuration was performed on multiple layers (for example, column and partition).

| Schema Name | Table Name | Partitions | Column | Definition of Loadable Page |
| --- | --- | --- | --- | --- |
| SAPSP4 | AAB_ID_PROPT | 0 |  | TABLE |
| SAPSP4 | ACLPERMIS | 0 |  | TABLE |
| SAPSP4 | ACMDCLSRC | 0 |  | TABLE |
| SAPSP4 | ACMDCLSRCT | 0 |  | TABLE |
| SAPSP4 | ACM_DTLOG | 0 |  | TABLE |
| SAPSP4 | APJ_W_JCE_GR_T | 0 |  | TABLE |
| SAPSP4 | APJ_W_JCE_PAR | 0 |  | TABLE |
| SAPSP4 | APJ_W_JCE_RO_T | 0 |  | TABLE |
| SAPSP4 | APJ_W_JCE_SCT_T | 0 |  | TABLE |
| SAPSP4 | APJ_W_JT_RO_T | 0 |  | TABLE |
| SAPSP4 | ARS_W_API | 0 |  | TABLE |
| SAPSP4 | ARS_W_API_SCCSSR | 0 |  | TABLE |
| SAPSP4 | ARS_W_API_STATE | 0 |  | TABLE |
| SAPSP4 | BADIIMPL_ENH | 0 |  | TABLE |
| SAPSP4 | BADI_CHAR_COND | 0 |  | TABLE |
| SAPSP4 | BADI_IMPL | 0 |  | TABLE |
| SAPSP4 | BADI_MAIN | 0 |  | TABLE |
| SAPSP4 | BADI_SPOT | 0 |  | TABLE |
| SAPSP4 | BEL_D_EVENT | 0 |  | TABLE |
| SAPSP4 | BEL_D_EVENT_SEQ | 0 |  | TABLE |
|  | The output is cut off because of too many entries. |  |  |  |

The largest tables according to the disk size of the loadable page are shown in the table below. 
 It lists the total number of partitions, the number of partitions for NSE, the total memory size (memory size in DRAM and persistent memory), the total memory size in DRAM (heap also including the loadable size of the table), the persistent memory size, the loadable size in memory, and the loadable size on disk of the tables.

| Schema Name | Table Name | Total Number of Partitions | Number Partitions in NSE | Total Memory Size (MB) | Total Memory Size in DRAM (MB) | Memory Size in Persistent Memory (MB) | Memory Size of Loadable Page (MB) | Disk Size of Loadable Page (MB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SAPSP4 | DOKTL | 1 | 1 | 899 | 899 | 0 | 884 | 2.356,23 |
| SAPSP4 | D010TAB | 1 | 1 | 1.452 | 1.452 | 0 | 1.421 | 1.422,38 |
| SAPSP4 | DD03L | 1 | 1 | 1.332 | 1.332 | 0 | 1.325 | 1.327,75 |
| SAPSP4 | D010INC | 1 | 1 | 708 | 708 | 0 | 695 | 695,85 |
| SAPSP4 | DD04T | 1 | 1 | 244 | 244 | 0 | 231 | 231,00 |
| SAPSP4 | DYNPSOURCE | 1 | 1 | 200 | 200 | 0 | 199 | 198,71 |
| SAPSP4 | COV_GENDATA | 1 | 1 | 166 | 166 | 0 | 162 | 162,02 |
| SAPSP4 | DOKHL | 1 | 1 | 161 | 161 | 0 | 145 | 145,62 |
| SAPSP4 | DDFIELDANNO | 1 | 1 | 154 | 154 | 0 | 141 | 141,29 |
| SAPSP4 | DD03ND | 1 | 1 | 148 | 148 | 0 | 140 | 140,97 |
| SAPSP4 | DDCDS_CONDITION | 1 | 1 | 143 | 143 | 0 | 130 | 130,60 |
| SAPSP4 | TADIR | 1 | 1 | 156 | 156 | 0 | 129 | 129,68 |
| SAPSP4 | SPROXDAT | 1 | 1 | 38 | 38 | 0 | 33 | 119,38 |
| SAPSP4 | DOKIL | 1 | 1 | 122 | 122 | 0 | 108 | 108,36 |
| SAPSP4 | D021T | 1 | 1 | 114 | 114 | 0 | 107 | 107,32 |
| SAPSP4 | DDCDS_SELECTLIST | 1 | 1 | 118 | 118 | 0 | 105 | 105,64 |
| SAPSP4 | DD27S | 1 | 1 | 85 | 85 | 0 | 77 | 102,17 |
| SAPSP4 | DD02T | 1 | 1 | 110 | 110 | 0 | 102 | 102,07 |
| SAPSP4 | DD05S | 1 | 1 | 81 | 81 | 0 | 71 | 96,63 |
| SAPSP4 | DDHEADANNO | 1 | 1 | 100 | 100 | 0 | 91 | 91,27 |
|  | The output is cut off because of too many entries. |  |  |  |  |  |  |  |

#### SAP HANA NSE Buffer Cache

The table below lists information regarding the SAP HANA NSE Buffer Cache.

| Host | Port | Cache Name | State | Replacement Policy | Max. Size (GB) | Used Size (GB) | Hit Ratio (%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bswprddb01 | 30003 | CS | ENABLED | IMPROVED LRU | 48,41 | 7,10 | 99,99 |

The table below shows the page behavior of the Buffer Cache.

| Host | Port | Cache Name | State | Replacement Policy | Page Size (kB) | Total Size (GB) | Hot Page Size (GB) | Out of Buffer Page Size (GB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bswprddb01 | 30003 | CS | ENABLED | IMPROVED LRU | 4 | 0,01 | 0,00 | 0,00 |
|  |  |  |  |  | 16 | 0,00 | 0,00 | 0,00 |
|  |  |  |  |  | 64 | 0,04 | 0,03 | 0,00 |
|  |  |  |  |  | 256 | 3,02 | 2,86 | 0,00 |
|  |  |  |  |  | 1.024 | 5,72 | 2,36 | 0,00 |

## 16.5 SAP HANA Resource Consumption

The following table shows an overview of the resource consumption of the SAP HANA instances in the monitored timeframe.

HANA Instances Overview

| HANA Instance | Role | CPU Usage | Memory Usage of HANA server | Memory Usage of SAP HANA Instance | Memory Allocation of Tables | Memory Consumption Indexserver |
| --- | --- | --- | --- | --- | --- | --- |
| bswprddb01_H4P_00 | MASTER | [GREEN] | [GREEN] | [GREEN] | [GREEN] | [GREEN] |

The SAP HANA hardware resources are sufficient for the current workload.

### 16.5.1 Memory Utilization Overview for SAP HANA Instances

The following table shows the memory usage of the SAP HANA database. The table displays weekly average values for the SAP HANA memory areas:

**'Memory usage of the HANA database'** corresponds to the memory used by the entire SAP HANA database (comparable to 'DB used memory' in SAP HANA studio).

**'Global allocation limit'** is the limit for the overall memory usage of the SAP HANA instance defined by the global_allocation_limit parameter.

**'Row store size'** shows the average size of row store tables in SAP HANA memory.

**'Column store size'** shows the average size of column store tables in SAP HANA memory.

The main SAP HANA workload is handled by the SAP HANA index server. The weekly average of the hourly maximum values of the **'Memory usage of the index server'** and the **'Effective allocation limit'** of the index server are listed.

More detailed information about memory shortage on an SAP HANA instance is provided in the sections below.

Avg. memory usage by SAP HANA Instances

| HANA instance | Memory usage of SAP HANA [GB] | Global allocation limit [GB] | Row store size [GB] | Column store size [GB] | Memory usage of indexserver [GB] | Effective allocation limit of indexserver [GB] |
| --- | --- | --- | --- | --- | --- | --- |
| bswprddb01_H4P_00 | 241 | 484 | 8 | 124 | 215 | 457 |

### 16.5.2 SAP HANA Instance bswprddb01_H4P_00

#### CPU Usage of SAP HANA Server

| [GREEN] | No CPU bottlenecks were detected. |
| --- | --- |

To access the CPU usage charts in SAP EarlyWatch Alert Workspace, click [here](https://me.sap.com/ewa/dashboard/cpuUtilizationDetail/S4P_0021220331_000000000800631194/bswprddb01_H4P_00) .

The graphics below show the average and maximum CPU consumption per hour. 
 The data is obtained from the statistics tables of the SAP HANA database. 
 
 If the average CPU consumption exceeds 75%, a YELLOW rating is assigned. If it exceeds the threshold of 90%, a RED rating is assigned.
[IMAGE]
[IMAGE]

We did not find any critical issues in this area.

#### Memory Usage of SAP HANA Server

| [GREEN] | No memory bottlenecks were detected. |
| --- | --- |

To access the memory usage chart in SAP EarlyWatch Alert Workspace, click [here](https://me.sap.com/ewa/dashboard/memoUtilizationDetail/S4P_0021220331_000000000800631194/bswprddb01_H4P_00/HanaSer) .

The following graph shows the physical memory usage during the monitored timeframe. The average and maximum memory used by SAP HANA (and possibly other processes) is compared with the available physical memory of the SAP HANA server.
[IMAGE]

No critical issues were detected in this area.

#### Memory Usage of SAP HANA Instance

| [GREEN] | The memory consumption of the SAP HANA instance is not critical. |
| --- | --- |

To access the memory usage chart in SAP EarlyWatch Alert Workspace, click [here](https://me.sap.com/ewa/dashboard/memoUtilizationDetail/S4P_0021220331_000000000800631194/bswprddb01_H4P_00/HanaIns) .

The following graph shows the memory usage of the SAP HANA database instance during the monitored timeframe. The memory used by SAP HANA on the SAP HANA host is compared with the global allocation limit of the SAP HANA instance. 
 If the "Used SAP HANA Instance Memory" approaches the "Global Allocation Limit", data has to be unloaded from SAP HANA memory. This may affect the overall performance and stability of the SAP HANA database. 
 The SAP HANA memory usage should not exceed 90% of the "Global Allocation Limit".
[IMAGE]

The memory consumption of the SAP HANA instance is not critical.

#### Memory Allocation of Tables

| [GREEN] | The memory consumption of tables is below any critical threshold. |
| --- | --- |

This graphic shows the average memory consumption for storing row and column tables, and the memory available for temporary calculations and other operations.
[IMAGE]

From a SAP HANA sizing perspective, it is recommended that the memory usage for SAP HANA tables remains below 50% of the global allocation limit.

If the memory usage for SAP HANA tables reaches 70% of the global allocation limit, the remaining memory resources for temporary calculations may be too small.

#### Memory Consumption of Indexserver

| [GREEN] | The memory consumption of the index server was not critical. |
| --- | --- |

To access the memory usage chart in SAP EarlyWatch Alert Workspace, click [here](https://me.sap.com/ewa/dashboard/memoUtilizationDetail/S4P_0021220331_000000000800631194/bswprddb01_H4P_00/IndSer) .

The index server is the most critical component with regard to SAP HANA memory consumption and must be monitored regularly. If the memory consumption of the index server approaches the effective allocation limit, table unloads or even out-of-memory dumps may occur. 
 The following graph shows the memory consumption of the index server in relation to its effective allocation limit.
[IMAGE]

The memory consumption of the index server was not critical.

#### Main Memory Areas of SAP HANA

The following graph shows the top 5 consumers of SAP HANA memory. Additional allocators are summed up in the "Others" category. Refer to SAP Note [1999997](https://launchpad.support.sap.com/#/notes/1999997) - FAQ: SAP HANA Memory for a more detailed explanation of SAP HANA memory allocation.
[IMAGE]

To access the memory usage chart in SAP EarlyWatch Alert Workspace, click [here](https://me.sap.com/ewa/dashboard/memAreaFlex/S4P_0021220331_000000000800631194/bswprddb01_H4P) .

## 16.6 SAP HANA Workload and Performance

### 16.6.1 SAP HANA Load History

With the load history of the SAP HANA database important key figures can be obtained, which give further insights of the health state of the SAP HANA database.

#### SAP HANA Instance bswprddb01_H4P_00

##### CPU and SQL Statement Load

The following chart shows the comparison of the CPU load and the number of SQL statements per second of the corresponding service. 
 The number of SQL statements per second and the CPU utilization should correlate. In a well-balanced system the CPU consumption should be dominated by the number of SQL statements per second. Deviations of this behavior point e.g. to expensive SQL statements and should be investigated. High resource intensive SQL statements can be found in the SAP EarlyWatch Alert Workspace. To do so, use this link to the [SAP EarlyWatch Alert Workspace](https://me.sap.com/ewa/dashboard/cpuUtilizationDetail/S4P_0021220331_000000000800631194/bswprddb01_H4P_00) and press the button "Analyze CPU Utilization".
[IMAGE]

##### Threads and SQL Executors

The table below shows the most important KPIs regarding the thread- and SQL executor throughput.

Summary of Important Thread KPIs

| Service Name | Average Number of Active Threads | Maximum Number of Active Threads | Average Number of Waiting Threads | Maximum Number of Waiting Threads |
| --- | --- | --- | --- | --- |
| Indexserver | 2,43 | 9,66 | 0,90 | 7,48 |
| Xsengine | 0,00 | 0,00 | 0,00 | 0,00 |

Summary of Important SQL Executor KPIs

| Service Name | Average Number of Active SQL Executors | Maximum Number of Active SQL Executors | Average Number of Waiting SQL Executors | Maximum Number of Waiting SQL Executors |
| --- | --- | --- | --- | --- |
| Indexserver | 0,16 | 0,87 | 0,03 | 0,60 |
| Xsengine | 0,00 | 0,00 | 0,00 | 0,00 |

The chart below shows active and waiting threads and active and waiting SQL executors. A high amount of those waiting key figures in comparison to the corresponding active key figures might point to a problem during this time interval.
[IMAGE]

##### Connections and Transactions

The chart below shows the connections, transactions and blocked transactions.
[IMAGE]

##### Number of MVCC Versions

The Row Store Multiversion Concurrency Control (MVCC) indicates if long running not committed transactions were running leading to a high number of versions and may result in performance problems.

The table below shows the average and maximum number of the MVCC versions during the previous week.

| Service Name | Average Number of MVCC Versions | Maximum Number of MVCC Versions |
| --- | --- | --- |
| Indexserver | 109,8 | 1.196 |

The chart below shows the evolution of the number of MVCC versions per service.
[IMAGE]

### 16.6.2 SAP HANA Workload

The table shows the number of SQL requests executed per second and per node (maximum 23 nodes) in your SAP HANA system in the monitored timeframe.
[IMAGE]

### 16.6.3 SAP HANA Response Times

The following graph shows the execution times of the SAP HANA system in the monitored timeframe aggregated from all SAP HANA nodes. The displayed "Execution Time" is the hourly average execution time obtained by the historized SQL Plan Cache.

Since the "Execution Time" in the SQL Plan Cache does not contain all response time parts, we also show in the graph below the "Sum Execution Time", which is the sum of the "Execution Time" plus preparation time and table load time. For more information, see [SAP Note 2000002](https://launchpad.support.sap.com/#/notes/2000002) .
[IMAGE]

The following graph shows the response time distribution of the SAP HANA system. The data is collected from the history data of the SQL Plan Cache.
[IMAGE]

Explanation of the SAP HANA response time shares: 
 - Preparation time – time share for plan preparation 
 - Open time – time share for cursor open and select 
 - Fetch time – time share for cursor fetch 
 - Lock wait time - lock wait time share for the plan 
 - Table load time – time share for loading tables during plan preparation (available as of SAP HANA rev. 50)

### 16.6.4 Delta Merges

#### Column Tables with Largest Delta Stores

| [GREEN] | No problems with the delta size of column store tables were detected. |
| --- | --- |

The separation into main and delta storage allows high compression and high write performance at the same time. Write operations are performed on the delta store and changes are transferred from the delta store to the main store asynchronously during delta merge. 
 The column store automatically performs a delta merge according to several technical limits that are defined by parameters. 
 If applications require more direct control over the merge process, the smart merge function can be used for certain tables (for example, BW prevents delta merges during data loading for performance reasons).

Largest Column Tables in terms of Delta size

| Schema Name | Table Name | Partition ID | Memorysize in Main Store [MB] | Memorysize in Delta Store [MB] | Records in Delta Store | Sum of Records | Days since last Merge | Auto Merge On |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SAPSP4 | CDPOS | 0 | 9.418,0 | 73,0 | 255.143 | 136.285.556 | 7 | TRUE |
| SAPSP4 | BALDAT | 0 | 5.310,1 | 28,7 | 50.143 | 13.020.366 | 1 | TRUE |
| SAPSP4 | /SDF/SMON_WPINFO | 0 | 42,0 | 26,8 | 113.733 | 1.114.326 | 0 | TRUE |
| SAPSP4 | VBAP | 0 | 1.266,7 | 24,1 | 42.938 | 7.222.253 | 5 | TRUE |
| SAPSP4 | EDID4 | 0 | 4.643,9 | 21,3 | 139.061 | 151.852.482 | 3 | TRUE |
| SAPSP4 | SWWCNTP0 | 0 | 8.635,6 | 21,0 | 36.506 | 25.936.967 | 3 | TRUE |
| SAPSP4 | LIPS | 0 | 1.325,0 | 20,8 | 54.868 | 9.116.136 | 4 | TRUE |
| SAPSP4 | S650 | 0 | 448,3 | 19,3 | 60.506 | 9.765.555 | 6 | TRUE |
| SAPSP4 | VBRP | 0 | 968,4 | 18,4 | 45.718 | 6.904.548 | 4 | TRUE |
| SAPSP4 | GLPCA | 0 | 1.813,4 | 18,4 | 59.740 | 28.865.278 | 7 | TRUE |

#### Delta Merge Statistics

The SAP HANA database column store uses efficient compression algorithms to keep relevant application data in memory. Write operations on the compressed data are costly since they require the storage structure to be reorganized and the compression to be recalculated. Therefore, write operations in the column store do not directly modify the compressed data structure in the "main storage". 
 Instead, all changes are first written into a separate data structure called "delta storage" and synchronized with the main storage at a later point in time. This synchronization operation is called a delta merge. 
 Performance issues may occur in SAP HANA if there is a large amount of data in the delta storage, because read times from delta storage are considerably slower than reads from main storage. 
 In addition, the merge operation on a large data volume may cause bottleneck situations, since the data to be merged is held in memory twice during the merge operation. 
 
 The following graph shows the number of successful and failed delta merges in the monitored timeframe.
[IMAGE]

The following graph shows the delta merge volume from all merge types and the average delta merge time per record in the monitored timeframe:
[IMAGE]

Note: High merge duration can be a result of a high number of records to be merged or of a high-load situation in the system.

## 16.7 Administration

### 16.7.1 Diagnosis Files

| [GREEN] | The number and size of diagnosis files is uncritical. |
| --- | --- |

During operation, the SAP HANA database service writes messages and information to log files in its trace directory. The system administrator should check these files regularly and react to error messages accordingly. A large number of files may be generated, which can take up a lot of disk space and impair performance. The following table shows the number of files contained in the trace directory.

Diagnosis Files

| Server | Measured Time Period | Type | Number of Files | Total Size in MB |
| --- | --- | --- | --- | --- |
| bswprddb01 | Weekly | Log | 2 | 805,16 |
| bswprddb01 | Weekly | Trace | 17 | 119,73 |
| bswprddb01 | Unlimited | TOTAL | 79 | 1.361,67 |

We did not detect any issues with the number or size of these files.

Nevertheless, we recommend that you check the content of the trace folder in the SAP HANA database installation directory on a regular basis and delete any files that are no longer required.

### 16.7.2 Backup and Recovery

| [GREEN] | No issues for operating or administration in terms of backup/recovery have been detected. |
| --- | --- |

#### Log Backup

| Date | Weekday | Successful Log Backups | Unsuccessful Log Backups |
| --- | --- | --- | --- |
| 27.04.2026 | Monday | 385 | 0 |
| 28.04.2026 | Tuesday | 385 | 0 |
| 29.04.2026 | Wednesday | 385 | 0 |
| 30.04.2026 | Thursday | 385 | 0 |
| 01.05.2026 | Friday | 385 | 0 |
| 02.05.2026 | Saturday | 385 | 0 |
| 03.05.2026 | Sunday | 385 | 0 |

#### Data Backup

| Date | Weekday | Successful Data Backups | Unsuccessful Data Backups |
| --- | --- | --- | --- |
| 27.04.2026 | Monday | 1 | 0 |
| 28.04.2026 | Tuesday | 1 | 0 |
| 29.04.2026 | Wednesday | 1 | 0 |
| 30.04.2026 | Thursday | 1 | 0 |
| 01.05.2026 | Friday | 1 | 0 |
| 02.05.2026 | Saturday | 1 | 0 |
| 03.05.2026 | Sunday | 1 | 0 |

#### Number of Log Segments

This graph shows the number of log segments residing on your log volume.
[IMAGE]

We found no issues related to log segments.

### 16.7.3 Global Consistency Check Run

| [GRAY] | Only a lightweight consistency check is scheduled. |
| --- | --- |

The tables below show your setup of the consistency check runs. We differentiate between consistency check runs executed on all levels (CHECK_TABLE_CONSISTENCY('CHECK',NULL,NULL)) and consistency check runs executed on table level (CHECK_TABLE_CONSISTENCY('CHECK',<SCHEMA_NAME>,<TABLE_NAME>)) or executed by the statistics server.

Consistency Check Runs on all Levels with Action 'CHECK'

| Number of successful Executions | Last Start Date |
| --- | --- |
| 0 |  |

Consistency Check Runs on Table Level with Action 'CHECK'

| Number of checked Tables | Number of not verified Tables | Last Start Date |
| --- | --- | --- |
| 0 | 45064 |  |

Table Consistency Check by Statisticsserver

| Action | Time since last Run |
| --- | --- |
| check_delta_log, check_variable_part_sanity, check_data_container, check_variable_part_double_reference_global, check_partitioning, check_replication, check_table_container_no_load | 19 Hours |

A lightweight consistency check was scheduled by the statistics server or with the global consistency check on table level but only 50 - 80% of the tables were checked.

**Recommendation:** Set up the consistency check according to SAP's recommendation. Further information can be found in SAP Note [2116157](https://launchpad.support.sap.com/#/notes/2116157) and in the SAP HANA Admin Guide -> Managing Tables -> Table and Catalog Consistency Check. Please note that the consistency check should be performed at times when there is a low load on your system.

### 16.7.4 License Information

| [GREEN] | Your license is valid and permanent or it will remain for at least 30 days until it expires. |
| --- | --- |

The following table shows information about the validity of your license. The license should be permanent and valid.

License Information

| System ID | Installation Number | Expiration Date | Permanent | Valid | Product Name | Product Limit |
| --- | --- | --- | --- | --- | --- | --- |
| H4P | 0021220333 |  | TRUE | TRUE | SAP-HANA | 1024 |

### 16.7.5 Statisticsserver and Monitoring

| [GREEN] | No issues with the statistics server were detected. |
| --- | --- |

The table below shows KPIs relevant for monitoring stability with the embedded statistics server.

| KPI | Current value | Rating |
| --- | --- | --- |
| Status of the embedded Statisticsserver | Okay | [GREEN] |
| Alerts in the Statisticsserver are not scheduled in the expected timeframe. | 0 | [GREEN] |
| Number of tables not located on the master server | 0 | [GREEN] |
| Number of disabled alert collectors | 0 | [GREEN] |
| Number of disabled statistic collectors | 0 | [GREEN] |
| Collector_Global_Table_Persistence_Statistics idle | Idle | [GREEN] |
| Number of collectors with retention times < 42 days | 0 | [GREEN] |
| High number of unprocessed e-Mails | 114 | [GREEN] |
| Status of Collector HOST_CS_UNLOADS | Inactive | [GREEN] |
| Number of relevant inactive actions | 0 | [GREEN] |
| Number of actions with unknown state | 0 | [GREEN] |
| Number of Statisticsserver worker threads | 5 | [GREEN] |
| Historic thread samples save interval (s) | 600 | [GREEN] |
| History of M_RECORD_LOCKS collected | no | [GREEN] |
| Historic thread call stacks interval (s) | 299 | [GREEN] |
| Retention time for the table disk size history | 365 | [GREEN] |

## 16.8 Important SAP Notes for SAP HANA

| [GREEN] | Important information is available in the SAP Notes below. |
| --- | --- |

The following tables list important SAP Notes for SAP HANA.

SAP Notes for SAP HANA

| SAP Note | Description |
| --- | --- |
| 1514967 | SAP HANA: Central Note |
| 2380229 | SAP HANA Platform 2.0 - Central Note |
| 2091951 | Best Practice: SAP HANA Database Backup & Restore |
| 2021789 | SAP HANA Revision and Maintenance Strategy |
| 2000003 | FAQ: SAP HANA |
| 2600030 | Parameter Recommendations in SAP HANA Environments |
| 1911180 | HANA EarlyWatch Alerts (EWA) Issues |
| 1592925 | SAP HANA Database service connections |
| 1642148 | FAQ: SAP HANA Database Backup & Recovery |
| 1664432 | DBA Cockpit: SAP HANA database as remote database |
| 1681092 | Multiple SAP HANA databases on one appliance |
| 1661202 | Support for multiple applications on SAP HANA |
| 1650394 | SAP HANA DB: Partitioning and Distribution of Large Tables |
| 1953429 | SAP HANA and SAP NetWeaver AS ABAP on one Server |
| 1761546 | SAP ERP powered by SAP HANA - Optimizations |
| 1872170 | Suite on HANA and S/4 HANA sizing report |
| 1794297 | Secondary Indexes for the business suite on HANA |

SAP Notes for operating system

| SAP Note | Description |
| --- | --- |
| 2684254 | SAP HANA DB: Recommended OS settings for SLES 15 / SLES for SAP Applications 15 |

# 17 SAP HANA SQL Statements in H4P

This section provides an overview of the "most expensive SQL statements". When possible, a recommendation is provided.

A more detailed analysis of the SQL statements (including the possibility to choose different time windows) is supported by the "Self-Service SQL Statement Tuning" (see [SAP Note 1601951](https://launchpad.support.sap.com/#/notes/1601951) ). For general information on dealing with expensive SQL statements in SAP HANA, see [SAP Note 2000002](https://launchpad.support.sap.com/#/notes/2000002) .

## Data Quality

A download-based SQL statement analysis can be performed.

The following table provides information about the data in the SDCC download. For details, see [SAP Note 2344673](https://launchpad.support.sap.com/#/notes/2344673) and its successor note [SAP Note 3347789](https://launchpad.support.sap.com/#/notes/3347789) .

| Observation | Comment | Rating |
| --- | --- | --- |
| Version of ST-PI function module: 40 | This is the most recent version | [GREEN] |

## 17.1 Top Statements (Elapsed Time)

This section shows the top non-internal statements according to "Total Elapsed Time". The "Total Elapsed Time" is the sum of the "Total Execution Time" and the "Total Preparation Time" from the SQL PLAN CACHE. It has a direct impact on the response time of the application calling the statement.

See the following table for details of the selection:

| Database Start | 07.03.2026 -- 16:47:19 |
| --- | --- |
| Data Collection | 04.05.2026 -- 05:18:09 |
| Analysis Type | Analysis of Plan Cache |
| Data Source | HOST_SQL_PLAN_CACHE |
| Begin of Time Interval | 26.04.2026 -- 23:08:21 |
| End of Time Interval | 04.05.2026 -- 00:08:21 |

The selected statements - identified by their "Statement Hash" - are listed in the following table. Further details of these statements can be found in the subsections.

| Statement Hash | Total Elapsed Time [s] | Number of Executions | Time / Execution [us] | Records / Execution | Time / Record [us] |
| --- | --- | --- | --- | --- | --- |
| 237f7f6ff65013fa3016a8b40d6e4772 | 11.928,9 | 6.727 | 1.773.289,9 | 738.710,2 | 2,4 |
| 19fe2aafe10c86dc0e73e98322daaab9 | 4.002,1 | 49.979 | 80.076,6 | 1,9 | 41.075,9 |
| 1fa05502938f0afe1a4a782b6b9bd775 | 3.392,1 | 1.014 | 3.345.235,1 | 1,0 | 3.345.235,1 |
| b61a4a7ff31225a908196ac2ff49392b | 2.827,0 | 169 | 16.727.653,8 | 3,0 | 5.631.421,3 |
| dc718a097243ad453d8133c7742ba743 | 2.814,4 | 1.014 | 2.775.533,5 | 1,0 | 2.775.533,5 |

### 17.1.1 SQL Statement 237f7f6ff65013fa3016a8b40d6e4772

SELECT

/* FDA READ */ "MSEG" . "MBLNR" , "MSEG" . "MJAHR" , "MSEG" . "ZEILE" , "MSEG" . "CHARG"

FROM

/* Redirected table: MSEG */ "NSDM_V_MSEG" "MSEG" INNER JOIN /* Redirected table: MKPF */ "NSDM_V_MKPF" "MKPF" ON "MSEG"

. "MANDT" = "MKPF" . "MANDT" AND "MSEG" . "MBLNR" = "MKPF" . "MBLNR" AND "MSEG" . "MJAHR" = "MKPF" . "MJAHR"

WHERE

"MSEG" . "MANDT" = ? AND "MSEG" . "CHARG" = ?

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 3,79 |
| Contribution to Total Execution Time [%] | 10,42 |
| Maximal CPU Consumption per Hour [%] ( 01.05.2026 between 13:00 and 14:00 ) | 0,29 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top MATDOC Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top Statements (Total Memory) |
| SAP HANA SQL Statements in H4P -> Top Statements (Thread Samples) |
| SAP HANA SQL Statements in H4P -> Statements on Top Scanned Table |

#### 17.1.1.1 Analysis of Where Clause

| Table | Field | Operator |
| --- | --- | --- |
| ? | CHARG | = |
| ? | MANDT | = |

#### 17.1.1.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 11.929 | 1.773.290 | 1.730.541 | 1.961.674 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.1.1.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.1.1.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| MATDOC | SAPSP4 | COLUMN | Table not partitioned | 14.064.414 | bswprddb01 |

#### 17.1.1.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding |
| --- | --- | --- | --- | --- | --- |
| S4P | LM01 | ZST60000A_P01 | 47 | 25.12.2025 |  |
| S4P | ZAT6A | ZST60000A_P01 | 47 | 25.12.2025 |  |

### 17.1.2 SQL Statement 19fe2aafe10c86dc0e73e98322daaab9

SELECT

/* FDA READ */ "DEBTOR" "PARTNER" , "COMPANYCODE" "BUKRS" , "CREDITCONTROLAREA" "KKBER" , "DEBITCREDITCODE" "SHKZG" , "TRANSACTIONCURRENCY" "CURRENCY" , "GLACCOUNT" "HKONT" , "PAYMENTDIFFERENCEREASON" "RSTGR" , SUM( "AMOUNTINTRANSACTIONCURRENCY" ) "AMOUNT" , SUM( "HEDGEDAMOUNTINTRANSACTIONCRCY" ) "AMOUNT_SEC" , "SPECIALGLCODE" "UMSKZ"

FROM

/* Entity name: P_RECEIVABLESITEMHEDGEDAMOUNT WITH PRIVILEGED ACCESS */ "PRBLSHEDGEDAMT" "P_RECEIVABLESITEMHEDGEDAMOUNT"

WHERE

"MANDT" = ? AND ( "CLEARINGDATE" = N'-GDPR-' OR "CLEARINGDATE" > ? ) AND "NETDUEDATE" <= ? AND "DEBTOR" = ? AND "FINANCIALACCOUNTTYPE" = N'-GDPR-' AND "CREDITCONTROLAREA" = ? AND "SPECIALGLCODE" IN ( ? , ? , ? , ? , ? , ? , ? , ? ) AND NOT

"ACCOUNTINGDOCUMENTCATEGORY" IN ( ? , ? )

GROUP BY

"DEBTOR" , "COMPANYCODE" , "CREDITCONTROLAREA" , "DEBITCREDITCODE" , "TRANSACTIONCURRENCY" , "GLACCOUNT" , "PAYMENTDIFFERENCEREASON" , "SPECIALGLCODE"

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 2,01 |
| Contribution to Total Execution Time [%] | 3,50 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 16:00 and 17:00 ) | 1,27 |

#### 17.1.2.1 Analysis of Where Clause

| Table | Field | Operator |
| --- | --- | --- |
| ? | ACCOUNTINGDOCUMENTCATEGORY | IN |
| ? | CLEARINGDATE | = |
| ? | CLEARINGDATE | > |
| ? | CREDITCONTROLAREA | = |
| ? | DEBTOR | = |
| ? | FINANCIALACCOUNTTYPE | = |
| ? | MANDT | = |
| ? | NETDUEDATE | <= |
| ? | SPECIALGLCODE | IN |

#### 17.1.2.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 4.002 | 80.077 | 7.520 | 159.988 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.1.2.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.1.2.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| BSEG | SAPSP4 | COLUMN | Table not partitioned | 33.005.275 | bswprddb01 |
| BKPF | SAPSP4 | COLUMN | Table not partitioned | 6.016.771 | bswprddb01 |
| T014 | SAPSP4 | COLUMN | Table not partitioned | 39 | bswprddb01 |

#### 17.1.2.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- |
| S4P | CL_UKM_FACADE_LOCAL_CLIENT====CM005 | 100 | 22.12.2025 | [GRAY] | FIN-FSCM-CR | Credit Management |

### 17.1.3 SQL Statement 1fa05502938f0afe1a4a782b6b9bd775

SELECT ROUND(SUM(MEMORY_SIZE_IN_TOTAL)/(1024*1024*1024),3) AS "Column memory in use (Loaded) GB", ROUND(SUM(MEMORY_SIZE_IN_DELTA)/(1024*1024*1024),3) AS "Memory Size in delta GB", ROUND(SUM(MEMORY_SIZE_IN_HISTORY_MAIN + MEMORY_SIZE_IN_HISTORY_DELTA) / (1024*1024*1024),3) AS "Memory size in history GB", ROUND(SUM( CASE WHEN LOADED = '-GDPR-' THEN '-GDPR-' WHEN ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL < 0 THEN '-GDPR-' ELSE ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL END)/(1024*1024*1024),3) AS "Column memory Unloaded GB"

FROM

M_CS_TABLES

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 2,85 |
| Contribution to Total Execution Time [%] | 2,96 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 14:00 and 15:00 ) | 0,36 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Total Memory) |
| SAP HANA SQL Statements in H4P -> Top Statements (Thread Samples) |

#### 17.1.3.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 3.392 | 3.345.235 | 2.900.383 | 60.919.628 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.1.3.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.1.3.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| P_PROCEDURES_ | SYS | ROW | Table not partitioned | 22.261 | bswprddb01 |
| P_GRANTEDPRIVS_ | SYS | ROW | Table not partitioned | 4.022 | bswprddb01 |
| P_PRINCIPALS_ | SYS | ROW | Table not partitioned | 238 | bswprddb01 |
| P_SCHEMAS_ | SYS | ROW | Table not partitioned | 107 | bswprddb01 |
| P_OBJTYPES_ | SYS | ROW | Table not partitioned | 39 | bswprddb01 |

### 17.1.4 SQL Statement b61a4a7ff31225a908196ac2ff49392b

SELECT "MCS"."SOURCE", "MCS"."EVENT_TIME", "MCS"."HOST", "MCS"."PORT", "MCS"."SCHEMA_NAME", "MCS"."TABLE_NAME", "ST"."UNLOAD_PRIORITY", "MCS"."REASON", "TG"."GROUP_TYPE", "TG"."SUBTYPE", "TG"."GROUP_NAME", "MCS"."SIZE", "MCS"."OBJ_COUNT"

FROM

( -- unloaded tables SELECT '-GDPR-' AS "SOURCE", LEFT(u."UNLOAD_TIME",13) AS"EVENT_TIME", u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON", SUM(t."ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL") AS "SIZE", COUNT(*) AS "OBJ_COUNT" FROM "SYS"."M_CS_UNLOADS" AS u JOIN "SYS"."M_CS_TABLES" AS t ON (u."HOST" = t."HOST" AND u."PORT" = t."PORT" AND u."SCHEMA_NAME" = t."SCHEMA_NAME" AND u."TABLE_NAME" = t."TABLE_NAME") WHERE u."PART_ID" = -1 -- ie whole table is unloaded AND LEFT (u."UNLOAD_TIME",13) = LEFT (ADD_SECONDS (NOW (), -3600), 13) GROUP BY LEFT(u."UNLOAD_TIME",13), u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON" UNION ALL -- unloads SELECT '-GDPR-' AS "SOURCE", LEFT(u."UNLOAD_TIME",13) AS "EVENT_TIME", u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON", SUM(c."MEMORY_SIZE_IN_TOTAL") AS "SIZE", COUNT(*) AS "OBJ_COUNT" FROM "SYS"."M_CS_UNLOADS" AS u JOIN "SYS"."M_CS_ALL_COLUMNS" AS c ON (u."HOST" = c."HOST" AND u."PORT" = c."PORT" AND u."SCHEMA_NAME" = c."SCHEMA_NAME" AND u."TABLE_NAME" = c."TABLE_NAME" AND u."PART_ID" = c."PART_ID" AND u."COLUMN_NAME" = c."COLUMN_NAME") WHERE u."PART_ID" > -1 --ie only select partitions AND LEFT (u."UNLOAD_TIME",13) = LEFT (ADD_SECONDS (NOW (), -3600), 13) GROUP BY LEFT(u."UNLOAD_TIME",13),u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON" UNION ALL -- loads SELECT '-GDPR-' as "SOURCE", LEFT(l."LOAD_TIME", 13) AS "EVENT_TIME", l."HOST", l."PORT", l."SCHEMA_NAME", l."TABLE_NAME", '-GDPR-' AS "REASON", SUM(c."MEMORY_SIZE_IN_TOTAL") AS "SIZE", COUNT(*) AS "OBJ_COUNT" FROM "SYS"."M_CS_LOADS" as l JOIN "SYS"."M_CS_ALL_COLUMNS" as c ON (l."HOST" =c."HOST" AND l."PORT" = c."PORT" AND l."SCHEMA_NAME" = c."SCHEMA_NAME" AND l."TABLE_NAME" = c."TABLE_NAME" AND l."PART_ID" = c."PART_ID" AND l."COLUMN_NAME" = c."COLUMN_NAME") WHERE LEFT (l."LOAD_TIME", 13) = LEFT (ADD_SECONDS (NOW (), -3600), 13) GROUP BY LEFT(l."LOAD_TIME",13),l."HOST", l."PORT", l."SCHEMA_NAME", l."TABLE_NAME" ) AS "MCS" -- left outer jointhe TABLE_GROUPS LEFT OUTER JOIN "SYS"."TABLE_GROUPS" AS "TG" ON "MCS"."TABLE_NAME" = "TG"."TABLE_NAME" AND "MCS"."SCHEMA_NAME" = "TG"."SCHEMA_NAME" -- join SYS.TABLES JOIN "SYS"."TABLES" AS "ST" ON "MCS"."TABLE_NAME" = "ST"."TABLE_NAME" AND "MCS"."SCHEMA_NAME" = "ST"."SCHEMA_NAME"

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 2,95 |
| Contribution to Total Execution Time [%] | 2,47 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 02:00 and 03:00 ) | 0,14 |
| Maximal Memory Consumption [%] ( 01.05.2026 -- 16:05:02 ) | 0,78 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Total Memory) |
| SAP HANA SQL Statements in H4P -> Top Statements (Thread Samples) |

#### 17.1.4.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 2.827 | 16.727.654 | 15.495.373 | 32.595.132 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.1.4.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.1.4.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| P_INDEXES_ | SYS | ROW | Table not partitioned | 164.793 | bswprddb01 |
| P_PROCEDURES_ | SYS | ROW | Table not partitioned | 22.261 | bswprddb01 |
| RS_TABLES_ | SYS | ROW | Table not partitioned | 21.519 | bswprddb01 |
| P_PRINCIPALS_ | SYS | ROW | Table not partitioned | 238 | bswprddb01 |
| P_SCHEMAS_ | SYS | ROW | Table not partitioned | 107 | bswprddb01 |

### 17.1.5 SQL Statement dc718a097243ad453d8133c7742ba743

SELECT

HOST, ROUND(SUM(MEMORY_SIZE_IN_TOTAL)/(1024*1024*1024),3) AS "Column memory in use (Loaded) GB", ROUND(SUM(MEMORY_SIZE_IN_DELTA)/(1024*1024*1024),3) AS "Memory Size in delta GB", ROUND(SUM(MEMORY_SIZE_IN_HISTORY_MAIN + MEMORY_SIZE_IN_HISTORY_DELTA)/(1024*1024*1024),3) AS "Memory size in history GB", ROUND(SUM(CASE WHEN LOADED = '-GDPR-' THEN'-GDPR-' WHEN ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL < 0 THEN '-GDPR-' ELSE ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL END)/(1024*1024*1024),3) AS "Column memory Unloaded GB" FROM M_CS_TABLES GROUP BY HOST ORDER BY HOST

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 2,56 |
| Contribution to Total Execution Time [%] | 2,46 |
| Maximal CPU Consumption per Hour [%] ( 01.05.2026 between 04:00 and 05:00 ) | 0,51 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Total Memory) |
| SAP HANA SQL Statements in H4P -> Top Statements (Thread Samples) |

#### 17.1.5.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 2.814 | 2.775.533 | 2.664.260 | 2.997.579 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.1.5.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.1.5.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| P_PROCEDURES_ | SYS | ROW | Table not partitioned | 22.261 | bswprddb01 |
| P_GRANTEDPRIVS_ | SYS | ROW | Table not partitioned | 4.022 | bswprddb01 |
| P_PRINCIPALS_ | SYS | ROW | Table not partitioned | 238 | bswprddb01 |
| P_SCHEMAS_ | SYS | ROW | Table not partitioned | 107 | bswprddb01 |
| P_OBJTYPES_ | SYS | ROW | Table not partitioned | 39 | bswprddb01 |

## 17.2 Top ACDOCA Statements (Elapsed Time)

This section shows the top non-internal statements according to "Total Elapsed Time". The "Total Elapsed Time" is the sum of the "Total Execution Time" and the "Total Preparation Time" from the SQL PLAN CACHE. It has a direct impact on the response time of the application calling the statement.

Only statements accessing table ACDOCA are shown.

See the following table for details of the selection:

| Database Start | 07.03.2026 -- 16:47:19 |
| --- | --- |
| Data Collection | 04.05.2026 -- 05:18:09 |
| Analysis Type | Analysis of Plan Cache |
| Data Source | HOST_SQL_PLAN_CACHE |
| Begin of Time Interval | 26.04.2026 -- 23:08:21 |
| End of Time Interval | 04.05.2026 -- 00:08:21 |

The selected statements - identified by their "Statement Hash" - are listed in the following table. Further details of these statements can be found in the subsections.

| Statement Hash | Total Elapsed Time [s] | Number of Executions | Time / Execution [us] | Records / Execution | Time / Record [us] |
| --- | --- | --- | --- | --- | --- |
| 5d03ec31dc233f1f9d7effcbf58cda53 | 246,6 | 338 | 729.569,6 | 96.311,9 | 7,6 |
| 3ff60adadf27fa82129ec692ecc6c1f5 | 193,1 | 114 | 1.693.679,3 | 0,0 | 0,0 |
| 086d3e3d7656a869f1fcd5a3d9b8466c | 158,3 | 114 | 1.388.962,5 | 0,0 | 0,0 |
| 926b66ad6813c3c727e9ba0c4e16cf98 | 107,6 | 706.831 | 152,3 | 0,2 | 886,8 |
| acfb3624b83420a3c000e2255102e2ad | 40,4 | 114 | 354.800,0 | 0,0 | 0,0 |

### 17.2.1 SQL Statement 5d03ec31dc233f1f9d7effcbf58cda53

SELECT

"LQUA" . "WERKS" , "LQUA" . "MATNR" , "LQUA" . "CHARG" , "LQUA" . "LENUM" , "LQUA" . "BESTQ" , "LQUA" . "LGTYP" , "LQUA" . "LGPLA" , "LQUA" . "GESME" , "LQUA" . "MEINS" , "LQUA" . "BDATU" , "LQUA" . "WDATU" , "MBEW" . "PEINH" , "MBEW" . "STPRS" , "MBEW" . "VERPR" , "MBEW" . "VPRSV" , "MBEW" . "BWKEY" , "MBEW" . "MATNR" , "MARA" . "MATKL" , "MARA" . "EXTWG" , "MARA" . "PRDHA" , "MARA" . "MATNR" , "MARM" . "UMREN" , "MARM" . "UMREZ" , "MARM" . "MEINH" , "MARM" . "MATNR"

FROM

"LQUA" INNER JOIN /* Redirected table: MBEW */ "MBVMBEW" "MBEW" ON "LQUA" . "MANDT" = "MBEW" . "MANDT" AND "MBEW" . "MATNR" = "LQUA" . "MATNR" AND "MBEW" . "BWKEY" = "LQUA" . "WERKS" INNER JOIN "MARA" ON "LQUA" . "MANDT" = "MARA" . "MANDT"AND "MARA" . "MATNR" = "MBEW" . "MATNR" LEFT OUTER JOIN "MARM" ON "LQUA" . "MANDT" = "MARM" . "MANDT" AND "MARM" . "MATN

R" = "MARA" . "MATNR"

WHERE

"LQUA" . "MANDT" = ? AND NOT "LQUA" . "BESTQ" IN ( ? , ? ) AND "LQUA" . "CHARG" >= ? AND "LQUA" . "LGTYP" >= ? AND NOT "LQUA" . "MATNR" IN ( ? , ? ) AND "LQUA" . "WERKS" IN ( ? , ? , ? , ? , ? , ? )

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,07 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 01:00 and 02:00 ) | 0,02 |

#### 17.2.1.1 Analysis of Where Clause

| Table | Field | Operator | Supported by Single Column Index | Compression | Distinct Values | SCANNED RECORD COUNT | INDEX LOOKUP COUNT |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LQUA | BESTQ | IN |  |  | 3 | 43.462 | 0 |
| LQUA | CHARG | >= |  |  | 27.415 | 343.263.707 | 0 |
| LQUA | LGTYP | >= |  |  | 15 | 380.077 | 0 |
| LQUA | MANDT | = | [GRAY] | RLE | 1 | 256 | 0 |
| LQUA | MATNR | IN | [GRAY] | DEFAULT | 3.055 | 0 | 212 |
| LQUA | WERKS | IN |  |  | 6 | 141.397 | 0 |

#### 17.2.1.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 247 | 729.570 | 620.742 | 890.271 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.2.1.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.2.1.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| CKMLCR | SAPSP4 | COLUMN | Table not partitioned | 1.057.744 | bswprddb01 |
| LQUA | SAPSP4 | COLUMN | Table not partitioned | 29.229 | bswprddb01 |
| DUMMY | SYS | ROW | Table not partitioned | 1 | bswprddb01 |

#### 17.2.1.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding |
| --- | --- | --- | --- | --- | --- |
| S4P | AGED_STOCKBSW | AQA0UK_KG_LIST==AGED_STOCKBSW= | 369 | 30.12.2025 |  |

### 17.2.2 SQL Statement 3ff60adadf27fa82129ec692ecc6c1f5

CALL "CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA#stb2#20220207221012" ( ?, ?, ?, ? )

Statement Impact

| Indicator | Value |
| --- | --- |
| Maximal Memory Consumption [%] ( 27.04.2026 -- 05:12:19 ) | 1,03 |

#### 17.2.2.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 193 | 1.692.493 | 30.741 | 6.942.516 |
| PREPARATION | 0 | 1.187 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.2.2.2 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| ACDOCA | SAPSP4 | COLUMN | Table not partitioned | 78.680.556 | bswprddb01 |
| BSEG | SAPSP4 | COLUMN | Table not partitioned | 33.005.275 | bswprddb01 |
| BKPF | SAPSP4 | COLUMN | Table not partitioned | 6.016.771 | bswprddb01 |

#### 17.2.2.3 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | FINS_REC-04.05.26-05:12:23---1 | CL_FINS_RECONCILE_DOCUMENT====CM005 | 1 | 22.12.2025 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |
| S4P | FINS_REC-04.05.26-05:12:23---2 | CL_FINS_RECONCILE_DOCUMENT====CM005 | 1 | 22.12.2025 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |
| S4P | FINS_REC-04.05.26-05:12:23---3 | CL_FINS_RECONCILE_DOCUMENT====CM005 | 1 | 22.12.2025 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |
| S4P | FINS_REC-04.05.26-05:14:24---3 | CL_FINS_RECONCILE_DOCUMENT====CM005 | 1 | 22.12.2025 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |

### 17.2.3 SQL Statement 086d3e3d7656a869f1fcd5a3d9b8466c

CALL "CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_ACDOCA_AMOUNT#stb2#20220207221012" ( ?, ?, ?, ? )

Statement Impact

| Indicator | Value |
| --- | --- |
| Maximal Memory Consumption [%] ( 27.04.2026 -- 05:12:26 ) | 0,63 |

#### 17.2.3.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 158 | 1.388.376 | 43.443 | 7.296.325 |
| PREPARATION | 0 | 586 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.2.3.2 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| BSEG | SAPSP4 | COLUMN | Table not partitioned | 33.005.275 | bswprddb01 |
| BKPF | SAPSP4 | COLUMN | Table not partitioned | 6.016.771 | bswprddb01 |
| T022 | SAPSP4 | COLUMN | Table not partitioned | 188 | bswprddb01 |

#### 17.2.3.3 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | FINS_REC-13.04.26-05:10:14---1 | CL_FINS_RECONCILE_DOCUMENT====CM00C | 1 | 14.11.2019 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |
| S4P | FINS_REC-13.04.26-05:10:14---2 | CL_FINS_RECONCILE_DOCUMENT====CM00C | 1 | 14.11.2019 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |

### 17.2.4 SQL Statement 926b66ad6813c3c727e9ba0c4e16cf98

SELECT

/* FDA READ */ "KALNR" , "RLDNR" , "RBUKRS" , CAST( ? AS NVARCHAR(7) ) "FISCYEARPER" , SUM( "VMSL" ) "VMSL" , SUM( "HSL" ) "HSL" , SUM( "KSL" ) "KSL" , SUM( "OSL" ) "OSL" , SUM( "VSL" ) "VSL" , SUM( "BSL" ) "BSL" , SUM( "CSL" ) "CSL" , SUM( "DSL" ) "DSL" , SUM( "ESL" ) "ESL" , SUM( "FSL" ) "FSL" , SUM( "GSL" ) "GSL" , SUM( "HVKWRT" ) "HVKWRT"

FROM

"ACDOCA_M_EXTRACT"

WHERE

"RCLNT" = ? AND "KALNR" = ? AND "FISCYEARPER" = N'-GDPR-'

GROUP BY

"RBUKRS" , "KALNR" , "RLDNR"

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,01 |
| Maximal CPU Consumption per Hour [%] ( 29.04.2026 between 02:00 and 03:00 ) | 0,02 |

#### 17.2.4.1 Analysis of Where Clause

| Table | Field | Operator | Supported by Single Column Index | Compression | Distinct Values | SCANNED RECORD COUNT | INDEX LOOKUP COUNT |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACDOCA_M_EXTRACT | FISCYEARPER | = | [GRAY] | INDIRECT | 246 | 36.118.004 | 9.884 |
| ACDOCA_M_EXTRACT | KALNR | = | [GRAY] | DEFAULT | 19.125 | 495.592.676 | 22.261 |
| ACDOCA_M_EXTRACT | RCLNT | = | [GRAY] | RLE | 1 | 132 | 0 |

#### 17.2.4.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 108 | 152 | 94 | 46.462 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.2.4.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.2.4.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| ACDOCA_M_EXTRACT | SAPSP4 | COLUMN | Table not partitioned | 478.267 | bswprddb01 |

#### 17.2.4.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- |
| S4P | CL_FML_ACDOCA_M_EXTRACT_UTIL==CM00T | 14 | 05.11.2021 | [GRAY] | CO-PC-ML | Material Subledger |

### 17.2.5 SQL Statement acfb3624b83420a3c000e2255102e2ad

CALL "CL_FINS_RECONCILE_DOCUMENT=>CHECK_BALANCE_ACDOCA#stb2#20220207221012" ( ?, ?, ?, ? )

Statement Impact

| Indicator | Value |
| --- | --- |
| Maximal Memory Consumption [%] ( 27.04.2026 -- 05:14:53 ) | 0,10 |

#### 17.2.5.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 40 | 353.617 | 50.903 | 1.219.815 |
| PREPARATION | 0 | 1.183 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.2.5.2 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| ACDOCA | SAPSP4 | COLUMN | Table not partitioned | 78.680.556 | bswprddb01 |
| FINS_REC_MSG_MAP | SAPSP4 | COLUMN | Table not partitioned | 225 | bswprddb01 |

#### 17.2.5.3 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | FINS_REC-04.05.26-05:12:23---1 | CL_FINS_RECONCILE_DOCUMENT====CM004 | 1 | 24.05.2017 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |
| S4P | FINS_REC-04.05.26-05:14:24---3 | CL_FINS_RECONCILE_DOCUMENT====CM004 | 1 | 24.05.2017 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |

## 17.3 Top MATDOC Statements (Elapsed Time)

This section shows the top non-internal statements according to "Total Elapsed Time". The "Total Elapsed Time" is the sum of the "Total Execution Time" and the "Total Preparation Time" from the SQL PLAN CACHE. It has a direct impact on the response time of the application calling the statement.

Only statements accessing table MATDOC are shown.

See the following table for details of the selection:

| Database Start | 07.03.2026 -- 16:47:19 |
| --- | --- |
| Data Collection | 04.05.2026 -- 05:18:09 |
| Analysis Type | Analysis of Plan Cache |
| Data Source | HOST_SQL_PLAN_CACHE |
| Begin of Time Interval | 26.04.2026 -- 23:08:21 |
| End of Time Interval | 04.05.2026 -- 00:08:21 |

The selected statements - identified by their "Statement Hash" - are listed in the following table. Further details of these statements can be found in the subsections.

| Statement Hash | Total Elapsed Time [s] | Number of Executions | Time / Execution [us] | Records / Execution | Time / Record [us] |
| --- | --- | --- | --- | --- | --- |
| 237f7f6ff65013fa3016a8b40d6e4772 | 11.928,9 | 6.727 | 1.773.289,9 | 738.710,2 | 2,4 |
| 779fe86da93d0d9f81c11b5c3f890094 | 1.063,1 | 7.977 | 133.275,2 | 0,0 | 0,0 |
| a0d742d17230fa2c0891c8ac2ad6a7b5 | 530,1 | 7.961 | 66.589,1 | 5,3 | 12.454,3 |
| 977915add1769bc480a7f5a9194e26c3 | 186,6 | 261.940 | 712,2 | 1,0 | 720,4 |
| 6afe1f8edd18b682079669c8250689f6 | 135,7 | 715.546 | 189,7 | 0,1 | 1.412,6 |

### 17.3.1 SQL Statement 237f7f6ff65013fa3016a8b40d6e4772

SELECT

/* FDA READ */ "MSEG" . "MBLNR" , "MSEG" . "MJAHR" , "MSEG" . "ZEILE" , "MSEG" . "CHARG"

FROM

/* Redirected table: MSEG */ "NSDM_V_MSEG" "MSEG" INNER JOIN /* Redirected table: MKPF */ "NSDM_V_MKPF" "MKPF" ON "MSEG"

. "MANDT" = "MKPF" . "MANDT" AND "MSEG" . "MBLNR" = "MKPF" . "MBLNR" AND "MSEG" . "MJAHR" = "MKPF" . "MJAHR"

WHERE

"MSEG" . "MANDT" = ? AND "MSEG" . "CHARG" = ?

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 3,79 |
| Contribution to Total Execution Time [%] | 10,42 |
| Maximal CPU Consumption per Hour [%] ( 01.05.2026 between 13:00 and 14:00 ) | 0,29 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top Statements (Total Memory) |
| SAP HANA SQL Statements in H4P -> Top Statements (Thread Samples) |
| SAP HANA SQL Statements in H4P -> Statements on Top Scanned Table |

#### 17.3.1.1 Analysis of Where Clause

| Table | Field | Operator |
| --- | --- | --- |
| ? | CHARG | = |
| ? | MANDT | = |

#### 17.3.1.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 11.929 | 1.773.290 | 1.730.541 | 1.961.674 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.3.1.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.3.1.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| MATDOC | SAPSP4 | COLUMN | Table not partitioned | 14.064.414 | bswprddb01 |

#### 17.3.1.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding |
| --- | --- | --- | --- | --- | --- |
| S4P | LM01 | ZST60000A_P01 | 47 | 25.12.2025 |  |
| S4P | ZAT6A | ZST60000A_P01 | 47 | 25.12.2025 |  |

### 17.3.2 SQL Statement 779fe86da93d0d9f81c11b5c3f890094

CALL "CL_PPH_READ_CLASSIC=>GET_MRP_ELEMENTS#stb2#20221115100728" ( ?, ? )

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,05 |
| Contribution to Total Execution Time [%] | 0,93 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 13:00 and 14:00 ) | 0,02 |
| Maximal Memory Consumption [%] ( 01.05.2026 -- 02:05:04 ) | 1,00 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Statements on Top Scanned Table |

#### 17.3.2.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 1.063 | 133.275 | 67.564 | 7.326.725 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.3.2.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.3.2.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| PBED | SAPSP4 | COLUMN | Table not partitioned | 88.211 | bswprddb01 |
| PBIM | SAPSP4 | COLUMN | Table not partitioned | 15.193 | bswprddb01 |

#### 17.3.2.4 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | MD04 | CL_PPH_READ_CLASSIC===========CM001 | 1 | 22.12.2025 | [GRAY] | PP-MRP | Material Requirements Planning |
| S4P | MD07 | CL_PPH_READ_CLASSIC===========CM001 | 1 | 22.12.2025 | [GRAY] | PP-MRP | Material Requirements Planning |
| S4P | MRP_NETCH_UK | CL_PPH_READ_CLASSIC===========CM001 | 1 | 22.12.2025 | [GRAY] | PP-MRP | Material Requirements Planning |

### 17.3.3 SQL Statement a0d742d17230fa2c0891c8ac2ad6a7b5

/* procedure: "SAPSP4"."CL_PPH_READ_CLASSIC=>GET_MRP_ELEMENTS#stb2#20221115100728" line: 56 col: 3 (at pos 2746), procedure: "SAPSP4"."CL_PPH_READ_CLASSIC=>GET_MRP_ELEMENTS" variable: ET_STOCK_OUT line: 249 col: 5 (at pos 25032) */ WITH "_SYS_ET_STOCK_OUT_1" AS (SELECT m.matnr AS matnr, m.werks AS werks, m.berid AS berid, m.plaab AS plaab, m.planr AS planr, m.sort1 AS sort1, m.sort2 AS sort2, m.delkz AS delkz, m.vrfkz AS vrfkz, m.plumi AS plumi, m.mng01 AS mng01, m.sobkz AS sobkz, m.kdauf AS kdauf, m.kdpos AS kdpos, m.pspel AS pspel, m.lifnr, m.kunnr, m.sgt_scat AS sgt_scat

FROM"V_PPH_STOCK_KF" AS m WHERE (m.matnr, m.werks) IN (select matnr, werks

FROM

"SYS"."_SYS_SS2_TMP_TABLE_15266362_IT_SEL_2_AA0E7015A16ACB478820F00610E4EE00_3" "IT_SEL") AND m.mandt = __typed_NString__($1, 3)) select /* procedure: "CL_PPH_READ_CLASSIC=>GET_MRP_ELEMENTS#stb2#20221115100728" line: 56 col: 3 (at pos 0) */ *

FROM

"_SYS_ET_STOCK_OUT_1" "ET_STOCK_OUT"

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,14 |
| Maximal CPU Consumption per Hour [%] ( 03.05.2026 between 02:00 and 03:00 ) | 0,08 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Statements on Top Scanned Table |

#### 17.3.3.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 530 | 66.589 | 12.550 | 7.216.955 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.3.3.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.3.3.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| T001L | SAPSP4 | COLUMN | Table not partitioned | 1.362 | bswprddb01 |
| T003O | SAPSP4 | COLUMN | Table not partitioned | 324 | bswprddb01 |
| T399D | SAPSP4 | COLUMN | Table not partitioned | 271 | bswprddb01 |
| T441R | SAPSP4 | COLUMN | Table not partitioned | 52 | bswprddb01 |
| TCS41 | SAPSP4 | COLUMN | Table not partitioned | 27 | bswprddb01 |

#### 17.3.3.4 Root Statement

The following table shows details on the "ROOT STATEMENT", which is responsible for the observed SQL statement.

| ROOT_STATEMENT_HASH | ROOT_STATEMENT_TEXT | Samples |
| --- | --- | --- |
| 779fe86da93d0d9f81c11b5c3f890094 | CALL "CL_PPH_READ_CLASSIC=>GET_MRP_ELEMENTS#stb2#20221115100728" ( ?, ? ) | 27 |

#### 17.3.3.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | MD04 | CL_PPH_READ_CLASSIC===========CM001 | 1 | 22.12.2025 | [GRAY] | PP-MRP | Material Requirements Planning |
| S4P | MRP_NETCH_UK | CL_PPH_READ_CLASSIC===========CM001 | 1 | 22.12.2025 | [GRAY] | PP-MRP | Material Requirements Planning |

### 17.3.4 SQL Statement 977915add1769bc480a7f5a9194e26c3

SELECT

"MANDT" , "MATNR" , "WERKS" , "LGORT" , "CHARG" , "LVORM" , "ERSDA" , "ERNAM" , "LAEDA" , "AENAM" , "LFGJA" , "LFMON" ,"SPERC" , "CLABS" , "CUMLM" , "CINSM" , "CEINM" , "CSPEM" , "CRETM" , "CVMLA" , "CVMUM" , "CVMIN" , "CVMEI" , "CVMSP" ,"CVMRE" , "KZICL" , "KZICQ" , "KZICE" , "KZICS" , "KZVCL" , "KZVCQ" , "KZVCE" , "KZVCS" , "HERKL" , "CHDLL" , "CHJIN" ,"CHRUE" , "SGT_SCAT" , "FSH_SEASON_YEAR" , "FSH_SEASON" , "FSH_COLLECTION" , "FSH_THEME" , "FSH_SALLOC_QTY" , "/CWM/CLABS" , "/CWM/CINSM" , "/CWM/CEINM" , "/CWM/CSPEM" , "/CWM/CRETM" , "/CWM/CUMLM" , "/CWM/CVMLA" , "/CWM/CVMIN" , "/CWM/CVMEI" , "/CWM/CVMSP" , "/CWM/CVMRE" , "/CWM/CVMUM"

FROM

/* Redirected table: MCHB */ "NSDM_V_MCHB" "MCHB"

WHERE

"MANDT" = ? AND "MATNR" = ? AND "WERKS" = ? AND "LGORT" = ? AND "CHARG" = ?

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,05 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 19:00 and 20:00 ) | 0,05 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Statements on Top Scanned Table |

#### 17.3.4.1 Analysis of Where Clause

| Table | Field | Operator |
| --- | --- | --- |
| ? | CHARG | = |
| ? | LGORT | = |
| ? | MANDT | = |
| ? | MATNR | = |
| ? | WERKS | = |

#### 17.3.4.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 186 | 711 | 179 | 11.972 |
| PREPARATION | 0 | 1 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.3.4.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.3.4.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| MATDOC_EXTRACT | SAPSP4 | COLUMN | Table not partitioned | 5.176.689 | bswprddb01 |
| MCHB | SAPSP4 | COLUMN | Table not partitioned | 2.791.041 | bswprddb01 |

#### 17.3.4.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | LM01 | LMATLF37 | 15 | 31.07.2015 | [GRAY] | LO-MD-MM | Material Master |
| S4P | VL06O | LMATLF37 | 15 | 31.07.2015 | [GRAY] | LO-MD-MM | Material Master |

### 17.3.5 SQL Statement 6afe1f8edd18b682079669c8250689f6

SELECT

"MANDT" , "MATNR" , "WERKS" , "UMLMC" , "TRAME" , "VKUMC" , "VKTRW" , "GLGMG" , "VKGLG" , "BWESB" , "GJPER" , "MCRUE" ,"/CWM/UMLMC" , "/CWM/TRAME" , "/CWM/BWESB"

FROM

/* Entity name: NSDM_E_MARC_DIFF */ "NSDM_V_MARC_DIFF" "NSDM_E_MARC_DIFF"

WHERE

"MANDT" = ? AND "MATNR" = ? AND "WERKS" = ?

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,02 |
| Maximal CPU Consumption per Hour [%] ( 01.05.2026 between 13:00 and 14:00 ) | 0,04 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Statements on Top Scanned Table |

#### 17.3.5.1 Analysis of Where Clause

| Table | Field | Operator | Supported by Single Column Index | Compression | Distinct Values | SCANNED RECORD COUNT | INDEX LOOKUP COUNT |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MATDOC_EXTRACT | MANDT | = |  |  | 1 | 0 | 0 |
| MATDOC_EXTRACT | MATNR | = |  |  |  |  |  |
| MATDOC_EXTRACT | WERKS | = |  |  | 10 | 67.543.001 | 0 |

#### 17.3.5.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 136 | 190 | 118 | 9.863 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.3.5.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.3.5.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| MATDOC_EXTRACT | SAPSP4 | COLUMN | Table not partitioned | 5.176.689 | bswprddb01 |

#### 17.3.5.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- |
| S4P | CL_NSDM_SELECT_MARC===========CM002 | 2 | 18.04.2021 | [GRAY] | LO-MD-MM | Material Master |

## 17.4 Statements on Top Scanned Table

This section shows the top non-internal statements according to "Total Elapsed Time". The "Total Elapsed Time" is the sum of the "Total Execution Time" and the "Total Preparation Time" from the SQL PLAN CACHE. It has a direct impact on the response time of the application calling the statement.

Only SQL Statement accessing the "top scanned table" are shown. The "top scanned table" is the table that contains the column with the highest number of "SCANNED_RECORDS" in M_CS_ALL_COLUMN_STATISTICS (see the following table). IN many cases, creating an index on that column might improve the accesses.

| Schema | Table | Column |
| --- | --- | --- |
| SAPSP4 | MATDOC | CHARG |

See the following table for details of the selection:

| Database Start | 07.03.2026 -- 16:47:19 |
| --- | --- |
| Data Collection | 04.05.2026 -- 05:18:09 |
| Analysis Type | Analysis of Plan Cache |
| Data Source | HOST_SQL_PLAN_CACHE |
| Begin of Time Interval | 26.04.2026 -- 23:08:21 |
| End of Time Interval | 04.05.2026 -- 00:08:21 |

The selected statements - identified by their "Statement Hash" - are listed in the following table. Further details of these statements can be found in the subsections.

| Statement Hash | Total Elapsed Time [s] | Number of Executions | Time / Execution [us] | Records / Execution | Time / Record [us] |
| --- | --- | --- | --- | --- | --- |
| 237f7f6ff65013fa3016a8b40d6e4772 | 11.928,9 | 6.727 | 1.773.289,9 | 738.710,2 | 2,4 |
| 779fe86da93d0d9f81c11b5c3f890094 | 1.063,1 | 7.977 | 133.275,2 | 0,0 | 0,0 |
| a0d742d17230fa2c0891c8ac2ad6a7b5 | 530,1 | 7.961 | 66.589,1 | 5,3 | 12.454,3 |
| 977915add1769bc480a7f5a9194e26c3 | 186,6 | 261.940 | 712,2 | 1,0 | 720,4 |
| 6afe1f8edd18b682079669c8250689f6 | 135,7 | 715.546 | 189,7 | 0,1 | 1.412,6 |

### 17.4.1 SQL Statement 237f7f6ff65013fa3016a8b40d6e4772

SELECT

/* FDA READ */ "MSEG" . "MBLNR" , "MSEG" . "MJAHR" , "MSEG" . "ZEILE" , "MSEG" . "CHARG"

FROM

/* Redirected table: MSEG */ "NSDM_V_MSEG" "MSEG" INNER JOIN /* Redirected table: MKPF */ "NSDM_V_MKPF" "MKPF" ON "MSEG"

. "MANDT" = "MKPF" . "MANDT" AND "MSEG" . "MBLNR" = "MKPF" . "MBLNR" AND "MSEG" . "MJAHR" = "MKPF" . "MJAHR"

WHERE

"MSEG" . "MANDT" = ? AND "MSEG" . "CHARG" = ?

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 3,79 |
| Contribution to Total Execution Time [%] | 10,42 |
| Maximal CPU Consumption per Hour [%] ( 01.05.2026 between 13:00 and 14:00 ) | 0,29 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top MATDOC Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top Statements (Total Memory) |
| SAP HANA SQL Statements in H4P -> Top Statements (Thread Samples) |

#### 17.4.1.1 Analysis of Where Clause

| Table | Field | Operator |
| --- | --- | --- |
| ? | CHARG | = |
| ? | MANDT | = |

#### 17.4.1.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 11.929 | 1.773.290 | 1.730.541 | 1.961.674 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.4.1.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.4.1.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| MATDOC | SAPSP4 | COLUMN | Table not partitioned | 14.064.414 | bswprddb01 |

#### 17.4.1.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding |
| --- | --- | --- | --- | --- | --- |
| S4P | LM01 | ZST60000A_P01 | 47 | 25.12.2025 |  |
| S4P | ZAT6A | ZST60000A_P01 | 47 | 25.12.2025 |  |

### 17.4.2 SQL Statement 779fe86da93d0d9f81c11b5c3f890094

CALL "CL_PPH_READ_CLASSIC=>GET_MRP_ELEMENTS#stb2#20221115100728" ( ?, ? )

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,05 |
| Contribution to Total Execution Time [%] | 0,93 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 13:00 and 14:00 ) | 0,02 |
| Maximal Memory Consumption [%] ( 01.05.2026 -- 02:05:04 ) | 1,00 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top MATDOC Statements (Elapsed Time) |

#### 17.4.2.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 1.063 | 133.275 | 67.564 | 7.326.725 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.4.2.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.4.2.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| PBED | SAPSP4 | COLUMN | Table not partitioned | 88.211 | bswprddb01 |
| PBIM | SAPSP4 | COLUMN | Table not partitioned | 15.193 | bswprddb01 |

#### 17.4.2.4 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | MD04 | CL_PPH_READ_CLASSIC===========CM001 | 1 | 22.12.2025 | [GRAY] | PP-MRP | Material Requirements Planning |
| S4P | MD07 | CL_PPH_READ_CLASSIC===========CM001 | 1 | 22.12.2025 | [GRAY] | PP-MRP | Material Requirements Planning |
| S4P | MRP_NETCH_UK | CL_PPH_READ_CLASSIC===========CM001 | 1 | 22.12.2025 | [GRAY] | PP-MRP | Material Requirements Planning |

### 17.4.3 SQL Statement a0d742d17230fa2c0891c8ac2ad6a7b5

/* procedure: "SAPSP4"."CL_PPH_READ_CLASSIC=>GET_MRP_ELEMENTS#stb2#20221115100728" line: 56 col: 3 (at pos 2746), procedure: "SAPSP4"."CL_PPH_READ_CLASSIC=>GET_MRP_ELEMENTS" variable: ET_STOCK_OUT line: 249 col: 5 (at pos 25032) */ WITH "_SYS_ET_STOCK_OUT_1" AS (SELECT m.matnr AS matnr, m.werks AS werks, m.berid AS berid, m.plaab AS plaab, m.planr AS planr, m.sort1 AS sort1, m.sort2 AS sort2, m.delkz AS delkz, m.vrfkz AS vrfkz, m.plumi AS plumi, m.mng01 AS mng01, m.sobkz AS sobkz, m.kdauf AS kdauf, m.kdpos AS kdpos, m.pspel AS pspel, m.lifnr, m.kunnr, m.sgt_scat AS sgt_scat

FROM"V_PPH_STOCK_KF" AS m WHERE (m.matnr, m.werks) IN (select matnr, werks

FROM

"SYS"."_SYS_SS2_TMP_TABLE_15266362_IT_SEL_2_AA0E7015A16ACB478820F00610E4EE00_3" "IT_SEL") AND m.mandt = __typed_NString__($1, 3)) select /* procedure: "CL_PPH_READ_CLASSIC=>GET_MRP_ELEMENTS#stb2#20221115100728" line: 56 col: 3 (at pos 0) */ *

FROM

"_SYS_ET_STOCK_OUT_1" "ET_STOCK_OUT"

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,14 |
| Maximal CPU Consumption per Hour [%] ( 03.05.2026 between 02:00 and 03:00 ) | 0,08 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top MATDOC Statements (Elapsed Time) |

#### 17.4.3.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 530 | 66.589 | 12.550 | 7.216.955 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.4.3.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.4.3.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| T001L | SAPSP4 | COLUMN | Table not partitioned | 1.362 | bswprddb01 |
| T003O | SAPSP4 | COLUMN | Table not partitioned | 324 | bswprddb01 |
| T399D | SAPSP4 | COLUMN | Table not partitioned | 271 | bswprddb01 |
| T441R | SAPSP4 | COLUMN | Table not partitioned | 52 | bswprddb01 |
| TCS41 | SAPSP4 | COLUMN | Table not partitioned | 27 | bswprddb01 |

#### 17.4.3.4 Root Statement

The following table shows details on the "ROOT STATEMENT", which is responsible for the observed SQL statement.

| ROOT_STATEMENT_HASH | ROOT_STATEMENT_TEXT | Samples |
| --- | --- | --- |
| 779fe86da93d0d9f81c11b5c3f890094 | CALL "CL_PPH_READ_CLASSIC=>GET_MRP_ELEMENTS#stb2#20221115100728" ( ?, ? ) | 27 |

#### 17.4.3.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | MD04 | CL_PPH_READ_CLASSIC===========CM001 | 1 | 22.12.2025 | [GRAY] | PP-MRP | Material Requirements Planning |
| S4P | MRP_NETCH_UK | CL_PPH_READ_CLASSIC===========CM001 | 1 | 22.12.2025 | [GRAY] | PP-MRP | Material Requirements Planning |

### 17.4.4 SQL Statement 977915add1769bc480a7f5a9194e26c3

SELECT

"MANDT" , "MATNR" , "WERKS" , "LGORT" , "CHARG" , "LVORM" , "ERSDA" , "ERNAM" , "LAEDA" , "AENAM" , "LFGJA" , "LFMON" ,"SPERC" , "CLABS" , "CUMLM" , "CINSM" , "CEINM" , "CSPEM" , "CRETM" , "CVMLA" , "CVMUM" , "CVMIN" , "CVMEI" , "CVMSP" ,"CVMRE" , "KZICL" , "KZICQ" , "KZICE" , "KZICS" , "KZVCL" , "KZVCQ" , "KZVCE" , "KZVCS" , "HERKL" , "CHDLL" , "CHJIN" ,"CHRUE" , "SGT_SCAT" , "FSH_SEASON_YEAR" , "FSH_SEASON" , "FSH_COLLECTION" , "FSH_THEME" , "FSH_SALLOC_QTY" , "/CWM/CLABS" , "/CWM/CINSM" , "/CWM/CEINM" , "/CWM/CSPEM" , "/CWM/CRETM" , "/CWM/CUMLM" , "/CWM/CVMLA" , "/CWM/CVMIN" , "/CWM/CVMEI" , "/CWM/CVMSP" , "/CWM/CVMRE" , "/CWM/CVMUM"

FROM

/* Redirected table: MCHB */ "NSDM_V_MCHB" "MCHB"

WHERE

"MANDT" = ? AND "MATNR" = ? AND "WERKS" = ? AND "LGORT" = ? AND "CHARG" = ?

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,05 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 19:00 and 20:00 ) | 0,05 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top MATDOC Statements (Elapsed Time) |

#### 17.4.4.1 Analysis of Where Clause

| Table | Field | Operator |
| --- | --- | --- |
| ? | CHARG | = |
| ? | LGORT | = |
| ? | MANDT | = |
| ? | MATNR | = |
| ? | WERKS | = |

#### 17.4.4.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 186 | 711 | 179 | 11.972 |
| PREPARATION | 0 | 1 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.4.4.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.4.4.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| MATDOC_EXTRACT | SAPSP4 | COLUMN | Table not partitioned | 5.176.689 | bswprddb01 |
| MCHB | SAPSP4 | COLUMN | Table not partitioned | 2.791.041 | bswprddb01 |

#### 17.4.4.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | LM01 | LMATLF37 | 15 | 31.07.2015 | [GRAY] | LO-MD-MM | Material Master |
| S4P | VL06O | LMATLF37 | 15 | 31.07.2015 | [GRAY] | LO-MD-MM | Material Master |

### 17.4.5 SQL Statement 6afe1f8edd18b682079669c8250689f6

SELECT

"MANDT" , "MATNR" , "WERKS" , "UMLMC" , "TRAME" , "VKUMC" , "VKTRW" , "GLGMG" , "VKGLG" , "BWESB" , "GJPER" , "MCRUE" ,"/CWM/UMLMC" , "/CWM/TRAME" , "/CWM/BWESB"

FROM

/* Entity name: NSDM_E_MARC_DIFF */ "NSDM_V_MARC_DIFF" "NSDM_E_MARC_DIFF"

WHERE

"MANDT" = ? AND "MATNR" = ? AND "WERKS" = ?

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,02 |
| Maximal CPU Consumption per Hour [%] ( 01.05.2026 between 13:00 and 14:00 ) | 0,04 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top MATDOC Statements (Elapsed Time) |

#### 17.4.5.1 Analysis of Where Clause

| Table | Field | Operator | Supported by Single Column Index | Compression | Distinct Values | SCANNED RECORD COUNT | INDEX LOOKUP COUNT |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MATDOC_EXTRACT | MANDT | = |  |  | 1 | 0 | 0 |
| MATDOC_EXTRACT | MATNR | = |  |  |  |  |  |
| MATDOC_EXTRACT | WERKS | = |  |  | 10 | 67.543.001 | 0 |

#### 17.4.5.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 136 | 190 | 118 | 9.863 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.4.5.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.4.5.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| MATDOC_EXTRACT | SAPSP4 | COLUMN | Table not partitioned | 5.176.689 | bswprddb01 |

#### 17.4.5.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- |
| S4P | CL_NSDM_SELECT_MARC===========CM002 | 2 | 18.04.2021 | [GRAY] | LO-MD-MM | Material Master |

## 17.5 Top Statements (Total Memory)

This section shows the top statements according to memory consumption as obtained from the SQL PLAN CACHE. It considers the product of the number of executions and the average memory consumption per execution.

See the following table for details of the selection:

| Database Start | 07.03.2026 -- 16:47:19 |
| --- | --- |
| Data Collection | 04.05.2026 -- 05:18:09 |
| Analysis Type | Analysis of Plan Cache |
| Data Source | M_SQL_PLAN_CACHE |

The selected statements - identified by their "Statement Hash" - are listed in the following table. Further details of these statements can be found in the subsections.

| Statement Hash | Number of Executions | Time / Execution [us] | Records / Execution | Executions x Avg Mem x Avg Time[GB x s] | Memory / Execution [MB] |
| --- | --- | --- | --- | --- | --- |
| b61a4a7ff31225a908196ac2ff49392b | 1.380 | 16.313.553,8 | 19,5 | 80.330 | 3.653,8 |
| 3936e6e71a78fd05240f77e046f1ca06 | 2 | 72.824.842,5 | 0,0 | 7.618 | 53.560,1 |
| 1fa05502938f0afe1a4a782b6b9bd775 | 8.277 | 3.293.760,8 | 1,0 | 3.985 | 149,7 |
| 237f7f6ff65013fa3016a8b40d6e4772 | 53.770 | 1.765.775,7 | 734.232,5 | 3.818 | 41,2 |
| dc718a097243ad453d8133c7742ba743 | 8.277 | 2.748.108,9 | 1,0 | 3.289 | 148,1 |

### 17.5.1 SQL Statement b61a4a7ff31225a908196ac2ff49392b

SELECT "MCS"."SOURCE", "MCS"."EVENT_TIME", "MCS"."HOST", "MCS"."PORT", "MCS"."SCHEMA_NAME", "MCS"."TABLE_NAME", "ST"."UNLOAD_PRIORITY", "MCS"."REASON", "TG"."GROUP_TYPE", "TG"."SUBTYPE", "TG"."GROUP_NAME", "MCS"."SIZE", "MCS"."OBJ_COUNT"

FROM

( -- unloaded tables SELECT '-GDPR-' AS "SOURCE", LEFT(u."UNLOAD_TIME",13) AS"EVENT_TIME", u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON", SUM(t."ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL") AS "SIZE", COUNT(*) AS "OBJ_COUNT" FROM "SYS"."M_CS_UNLOADS" AS u JOIN "SYS"."M_CS_TABLES" AS t ON (u."HOST" = t."HOST" AND u."PORT" = t."PORT" AND u."SCHEMA_NAME" = t."SCHEMA_NAME" AND u."TABLE_NAME" = t."TABLE_NAME") WHERE u."PART_ID" = -1 -- ie whole table is unloaded AND LEFT (u."UNLOAD_TIME",13) = LEFT (ADD_SECONDS (NOW (), -3600), 13) GROUP BY LEFT(u."UNLOAD_TIME",13), u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON" UNION ALL -- unloads SELECT '-GDPR-' AS "SOURCE", LEFT(u."UNLOAD_TIME",13) AS "EVENT_TIME", u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON", SUM(c."MEMORY_SIZE_IN_TOTAL") AS "SIZE", COUNT(*) AS "OBJ_COUNT" FROM "SYS"."M_CS_UNLOADS" AS u JOIN "SYS"."M_CS_ALL_COLUMNS" AS c ON (u."HOST" = c."HOST" AND u."PORT" = c."PORT" AND u."SCHEMA_NAME" = c."SCHEMA_NAME" AND u."TABLE_NAME" = c."TABLE_NAME" AND u."PART_ID" = c."PART_ID" AND u."COLUMN_NAME" = c."COLUMN_NAME") WHERE u."PART_ID" > -1 --ie only select partitions AND LEFT (u."UNLOAD_TIME",13) = LEFT (ADD_SECONDS (NOW (), -3600), 13) GROUP BY LEFT(u."UNLOAD_TIME",13),u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON" UNION ALL -- loads SELECT '-GDPR-' as "SOURCE", LEFT(l."LOAD_TIME", 13) AS "EVENT_TIME", l."HOST", l."PORT", l."SCHEMA_NAME", l."TABLE_NAME", '-GDPR-' AS "REASON", SUM(c."MEMORY_SIZE_IN_TOTAL") AS "SIZE", COUNT(*) AS "OBJ_COUNT" FROM "SYS"."M_CS_LOADS" as l JOIN "SYS"."M_CS_ALL_COLUMNS" as c ON (l."HOST" =c."HOST" AND l."PORT" = c."PORT" AND l."SCHEMA_NAME" = c."SCHEMA_NAME" AND l."TABLE_NAME" = c."TABLE_NAME" AND l."PART_ID" = c."PART_ID" AND l."COLUMN_NAME" = c."COLUMN_NAME") WHERE LEFT (l."LOAD_TIME", 13) = LEFT (ADD_SECONDS (NOW (), -3600), 13) GROUP BY LEFT(l."LOAD_TIME",13),l."HOST", l."PORT", l."SCHEMA_NAME", l."TABLE_NAME" ) AS "MCS" -- left outer jointhe TABLE_GROUPS LEFT OUTER JOIN "SYS"."TABLE_GROUPS" AS "TG" ON "MCS"."TABLE_NAME" = "TG"."TABLE_NAME" AND "MCS"."SCHEMA_NAME" = "TG"."SCHEMA_NAME" -- join SYS.TABLES JOIN "SYS"."TABLES" AS "ST" ON "MCS"."TABLE_NAME" = "ST"."TABLE_NAME" AND "MCS"."SCHEMA_NAME" = "ST"."SCHEMA_NAME"

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 2,95 |
| Contribution to Total Execution Time [%] | 2,20 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 02:00 and 03:00 ) | 0,14 |
| Maximal Memory Consumption [%] ( 01.05.2026 -- 16:05:02 ) | 0,78 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top Statements (Thread Samples) |

#### 17.5.1.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 22.512 | 16.313.361 | 14.378.891 | 35.294.968 |
| PREPARATION | 0 | 192 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.5.1.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.5.1.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| P_INDEXES_ | SYS | ROW | Table not partitioned | 164.793 | bswprddb01 |
| P_PROCEDURES_ | SYS | ROW | Table not partitioned | 22.261 | bswprddb01 |
| RS_TABLES_ | SYS | ROW | Table not partitioned | 21.519 | bswprddb01 |
| P_PRINCIPALS_ | SYS | ROW | Table not partitioned | 238 | bswprddb01 |
| P_SCHEMAS_ | SYS | ROW | Table not partitioned | 107 | bswprddb01 |

### 17.5.2 SQL Statement 3936e6e71a78fd05240f77e046f1ca06

SELECT

"LIPS" . "VBELN" , "LIPS" . "POSNR" , "LIPS" . "LFIMG" , "LIPS" . "VRKME" , "LIPS" . "BRGEW" , "LIPS" . "GEWEI" , "LIPS" . "WERKS" , "LIPS" . "MATNR" , "LIPS" . "VGBEL" , "VBAK" . "BSTNK" , "VBAK" . "ERDAT" , "VBAK" . "MANDT" , "VBAK" . "VBELN" , "LQUA" . "LGTYP" , "LQUA" . "LGPLA" , "LQUA" . "GESME" , "LQUA" . "MEINS" , "LQUA" . "MATNR" , "LQUA" . "WERKS" , "VBPA" . "PARVW" , "VBPA" . "VBELN" , "VBPA" . "ADRNR" , "VBPA" . "KUNNR" , "LIKP" . "VBELN" , "MAKT" . "MATNR" , "MAKT" . "MAKTX" , "MAKT" . "SPRAS" , "MARM" . "MEINH" , "MARM" . "UMREZ" , "MARM" . "LAENG" , "MARM" . "MEABM" , "MARM" . "MATNR" , "ADRC" . "NAME1" , "ADRC" . "NAME4" , "ADRC" . "CITY1" , "ADRC" . "CITY2" , "ADRC" . "STREET" , "ADRC" . "POST_CODE1" , "ADRC" . "ADDRNUMBER" , "MLGT" . "LGPLA" , "MLGT" . "MATNR" , "KNA1" . "KUNNR" , "ADR6" . "SMTP_ADDR" , "ADR6" . "ADDRNUMBER" , "ADR2" . "TELNR_CALL" , "ADR2" . "CONSNUMBER" , "ADR2" . "ADDRNUMBER" , "VBFA" . "POSNN" , "VBFA" . "VBELN" , "VBFA" . "POSNV" , "VBFA" . "VBELV" , "VBEP" . "EDATU" , "VBEP" . "POSNR" , "VBEP" . "VBELN"

FROM

"LIPS" INNER JOIN "VBAK" ON "LIPS" . "MANDT" = "VBAK" . "MANDT" AND "VBAK" . "VBELN" = "LIPS" . "VGBEL" LEFT OUTER JOIN"LQUA" ON "LIPS" . "MANDT" = "LQUA" . "MANDT" AND "LQUA" . "MATNR" = "LIPS" . "MATNR" AND "LQUA" . "WERKS" = "LIPS" . "WERKS" INNER JOIN "VBPA" ON "LIPS" . "MANDT" = "VBPA" . "MANDT" AND "VBPA" . "VBELN" = "VBAK" . "VBELN" LEFT OUTER JOIN "LIKP" ON "LIPS" . "MANDT" = "LIKP" . "MANDT" AND "LIKP" . "VBELN" = "LIPS" . "VBELN" LEFT OUTER JOIN "MAKT" ON "LIPS" ."MANDT" = "MAKT" . "MANDT" AND "MAKT" . "MATNR" = "LIPS" . "MATNR" LEFT OUTER JOIN "MARM" ON "LIPS" . "MANDT" = "MARM" . "MANDT" AND "MARM" . "MATNR" = "LIPS" . "MATNR" INNER JOIN "ADRC" ON "LIPS" . "MANDT" = "ADRC" . "CLIENT" AND "ADRC" ."ADDRNUMBER" = "VBPA" . "ADRNR" LEFT OUTER JOIN "MLGT" ON "LIPS" . "MANDT" = "MLGT" . "MANDT" AND "MLGT" . "MATNR" = "LIPS" . "MATNR" INNER JOIN "KNA1" ON "LIPS" . "MANDT" = "KNA1" . "MANDT" AND "KNA1" . "KUNNR" = "VBPA" . "KUNNR" LEFT OUTER JOIN "ADR6" ON "LIPS" . "MANDT" = "ADR6" . "CLIENT" AND "ADR6" . "ADDRNUMBER" = "ADRC" . "ADDRNUMBER" LEFT OUTER JOIN"ADR2" ON "LIPS" . "MANDT" = "ADR2" . "CLIENT" AND "ADR2" . "ADDRNUMBER" = "ADRC" . "ADDRNUMBER" LEFT OUTER JOIN "VBFA"ON "LIPS" . "MANDT" = "VBFA" . "MANDT" AND "VBFA" . "POSNN" = "LIPS" . "POSNR" AND "VBFA" . "VBELN" = "LIPS" . "VBELN" INNER JOIN "VBEP" ON "LIPS" . "MANDT" = "VBEP" . "MANDT" AND "VBEP" . "POSNR" = "VBFA" . "POSNV" AND "VBEP" . "VBELN" = "

VBFA" . "VBELV"

WHERE

"LIPS" . "MANDT" = ? AND "LIPS" . "WERKS" = ? AND "VBPA" . "PARVW" = ?

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,01 |
| Maximal CPU Consumption per Hour [%] ( 30.04.2026 between 14:00 and 15:00 ) | 0,02 |
| Maximal Memory Consumption [%] ( 30.04.2026 -- 14:35:16 ) | 8,26 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statement (Maximal Memory in Trace) |

#### 17.5.2.1 Analysis of Where Clause

| Table | Field | Operator | SCANNED RECORD COUNT | INDEX LOOKUP COUNT |
| --- | --- | --- | --- | --- |
| ? | PARVW | = |  |  |
| LIPS | MANDT | = | 449.642 | 190 |
| LIPS | WERKS | = | 2.340.904 | 0 |

#### 17.5.2.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 145 | 72.575.672 | 49.158.293 | 95.993.051 |
| PREPARATION | 0 | 249.171 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.5.2.3 Memory Consumption

The following table provides an overview of the memory consumption of the analyzed SQL statement as obtained from the monitoring view M_SQL_PLAN_STATISTICS (or – if not yet available – M_SQL_PLAN_CACHE), that is, without taking a specific time interval into account.

| Activity | Total Memory [GB] | Average Memory [MB] | Minimal Memory [MB] | Maximal Memory [MB] |
| --- | --- | --- | --- | --- |
| EXECUTION_MEMORY_SIZE | 105 | 53.560,1 | 38.691,5 | 68.428,7 |

##### High Memory Consumption

The memory consumption of this statement is relatively high when compared with the minimum "effective allocation limit" of the index server(s) as obtained from M_SERVICE_MEMORY. See the following table for details. Note that the excessive memory consumption of a single statement might impact the stability of the whole SAP HANA system. See [SAP Note 1999997](https://launchpad.support.sap.com/#/notes/1999997) for details and for an option to restrict the maximum memory allocated by a single statement.

| (Minimal) Effective Allocation Limit [GB] | 457,3 |
| --- | --- |
| Maximal Statement Size / Effective Allocation Limit [%] | 14,6 |
| Average Statement Size / Effective Allocation Limit [%] | 11,4 |

#### 17.5.2.4 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.5.2.5 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| LIPS | SAPSP4 | COLUMN | Table not partitioned | 9.116.136 | bswprddb01 |
| LIKP | SAPSP4 | COLUMN | Table not partitioned | 1.056.668 | bswprddb01 |
| ADR2 | SAPSP4 | COLUMN | Table not partitioned | 617.920 | bswprddb01 |
| MLGT | SAPSP4 | COLUMN | Table not partitioned | 33.050 | bswprddb01 |
| LQUA | SAPSP4 | COLUMN | Table not partitioned | 29.229 | bswprddb01 |

#### 17.5.2.6 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding |
| --- | --- | --- | --- | --- | --- |
| S4P | SQ00 | AQA0UK==========HOTTIES_PICK== | 352 | 07.04.2026 |  |

### 17.5.3 SQL Statement 1fa05502938f0afe1a4a782b6b9bd775

SELECT ROUND(SUM(MEMORY_SIZE_IN_TOTAL)/(1024*1024*1024),3) AS "Column memory in use (Loaded) GB", ROUND(SUM(MEMORY_SIZE_IN_DELTA)/(1024*1024*1024),3) AS "Memory Size in delta GB", ROUND(SUM(MEMORY_SIZE_IN_HISTORY_MAIN + MEMORY_SIZE_IN_HISTORY_DELTA) / (1024*1024*1024),3) AS "Memory size in history GB", ROUND(SUM( CASE WHEN LOADED = '-GDPR-' THEN '-GDPR-' WHEN ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL < 0 THEN '-GDPR-' ELSE ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL END)/(1024*1024*1024),3) AS "Column memory Unloaded GB"

FROM

M_CS_TABLES

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 2,85 |
| Contribution to Total Execution Time [%] | 2,67 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 14:00 and 15:00 ) | 0,36 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top Statements (Thread Samples) |

#### 17.5.3.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 27.262 | 3.293.755 | 2.635.660 | 71.591.409 |
| PREPARATION | 0 | 6 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.5.3.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.5.3.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| P_PROCEDURES_ | SYS | ROW | Table not partitioned | 22.261 | bswprddb01 |
| P_GRANTEDPRIVS_ | SYS | ROW | Table not partitioned | 4.022 | bswprddb01 |
| P_PRINCIPALS_ | SYS | ROW | Table not partitioned | 238 | bswprddb01 |
| P_SCHEMAS_ | SYS | ROW | Table not partitioned | 107 | bswprddb01 |
| P_OBJTYPES_ | SYS | ROW | Table not partitioned | 39 | bswprddb01 |

### 17.5.4 SQL Statement 237f7f6ff65013fa3016a8b40d6e4772

SELECT

/* FDA READ */ "MSEG" . "MBLNR" , "MSEG" . "MJAHR" , "MSEG" . "ZEILE" , "MSEG" . "CHARG"

FROM

/* Redirected table: MSEG */ "NSDM_V_MSEG" "MSEG" INNER JOIN /* Redirected table: MKPF */ "NSDM_V_MKPF" "MKPF" ON "MSEG"

. "MANDT" = "MKPF" . "MANDT" AND "MSEG" . "MBLNR" = "MKPF" . "MBLNR" AND "MSEG" . "MJAHR" = "MKPF" . "MJAHR"

WHERE

"MSEG" . "MANDT" = ? AND "MSEG" . "CHARG" = ?

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 3,79 |
| Contribution to Total Execution Time [%] | 9,29 |
| Maximal CPU Consumption per Hour [%] ( 01.05.2026 between 13:00 and 14:00 ) | 0,29 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top MATDOC Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top Statements (Thread Samples) |
| SAP HANA SQL Statements in H4P -> Statements on Top Scanned Table |

#### 17.5.4.1 Analysis of Where Clause

| Table | Field | Operator |
| --- | --- | --- |
| ? | CHARG | = |
| ? | MANDT | = |

#### 17.5.4.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 94.946 | 1.765.772 | 23.412 | 2.121.435 |
| PREPARATION | 0 | 4 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.5.4.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.5.4.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| MATDOC | SAPSP4 | COLUMN | Table not partitioned | 14.064.414 | bswprddb01 |

#### 17.5.4.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding |
| --- | --- | --- | --- | --- | --- |
| S4P | LM01 | ZST60000A_P01 | 47 | 25.12.2025 |  |
| S4P | ZAT6A | ZST60000A_P01 | 47 | 25.12.2025 |  |

### 17.5.5 SQL Statement dc718a097243ad453d8133c7742ba743

SELECT

HOST, ROUND(SUM(MEMORY_SIZE_IN_TOTAL)/(1024*1024*1024),3) AS "Column memory in use (Loaded) GB", ROUND(SUM(MEMORY_SIZE_IN_DELTA)/(1024*1024*1024),3) AS "Memory Size in delta GB", ROUND(SUM(MEMORY_SIZE_IN_HISTORY_MAIN + MEMORY_SIZE_IN_HISTORY_DELTA)/(1024*1024*1024),3) AS "Memory size in history GB", ROUND(SUM(CASE WHEN LOADED = '-GDPR-' THEN'-GDPR-' WHEN ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL < 0 THEN '-GDPR-' ELSE ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL END)/(1024*1024*1024),3) AS "Column memory Unloaded GB" FROM M_CS_TABLES GROUP BY HOST ORDER BY HOST

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 2,56 |
| Contribution to Total Execution Time [%] | 2,23 |
| Maximal CPU Consumption per Hour [%] ( 01.05.2026 between 04:00 and 05:00 ) | 0,51 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top Statements (Thread Samples) |

#### 17.5.5.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 22.746 | 2.748.099 | 2.432.586 | 146.530.658 |
| PREPARATION | 0 | 10 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.5.5.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.5.5.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| P_PROCEDURES_ | SYS | ROW | Table not partitioned | 22.261 | bswprddb01 |
| P_GRANTEDPRIVS_ | SYS | ROW | Table not partitioned | 4.022 | bswprddb01 |
| P_PRINCIPALS_ | SYS | ROW | Table not partitioned | 238 | bswprddb01 |
| P_SCHEMAS_ | SYS | ROW | Table not partitioned | 107 | bswprddb01 |
| P_OBJTYPES_ | SYS | ROW | Table not partitioned | 39 | bswprddb01 |

## 17.6 Top Statement (Maximal Memory in Trace)

This section shows the top statements according to the maximal memory usage as of observed in the expensive statement trace, i.e. M_EXPENSIVE_STATEMENTS.

See the following table for details of the selection:

| Database Start | 07.03.2026 -- 16:47:19 |
| --- | --- |
| Data Collection | 04.05.2026 -- 05:18:09 |
| Analysis Type | Analysis of Expensive Statement Trace |
| Data Source | M_EXPENSIVE_STATEMENTS |
| First Day | 27.04.2026 |
| Last Day | 03.05.2026 |

The selected statements - identified by their "Statement Hash" - are listed in the following table. Further details of these statements can be found in the subsections.

| Statement Hash | Time / Execution [us] | Records / Execution | Time / Record [us] | Maximum Memory [MB] |
| --- | --- | --- | --- | --- |
| 3936e6e71a78fd05240f77e046f1ca06 | 49.403.316,0 | 0,0 | 0,0 | 38.691,0 |
| a0a33f001aab35f98bfcb496f422cc54 | 0,0 | 0,0 | 0,0 | 17.641,0 |
| d2040795d0fa208871e56bd08995dfee | 0,0 | 0,0 | 0,0 | 16.970,0 |
| 7e3b27c93bd4fd7f2dfba19861cb957c | 35.646.404,0 | 20,0 | 1.782.320,2 | 7.838,0 |
| 7648c0cbc7b7e85e3631b41aae312071 | 0,0 | 0,0 | 0,0 | 7.465,0 |

### 17.6.1 SQL Statement 3936e6e71a78fd05240f77e046f1ca06

SELECT

"LIPS" . "VBELN" , "LIPS" . "POSNR" , "LIPS" . "LFIMG" , "LIPS" . "VRKME" , "LIPS" . "BRGEW" , "LIPS" . "GEWEI" , "LIPS" . "WERKS" , "LIPS" . "MATNR" , "LIPS" . "VGBEL" , "VBAK" . "BSTNK" , "VBAK" . "ERDAT" , "VBAK" . "MANDT" , "VBAK" . "VBELN" , "LQUA" . "LGTYP" , "LQUA" . "LGPLA" , "LQUA" . "GESME" , "LQUA" . "MEINS" , "LQUA" . "MATNR" , "LQUA" . "WERKS" , "VBPA" . "PARVW" , "VBPA" . "VBELN" , "VBPA" . "ADRNR" , "VBPA" . "KUNNR" , "LIKP" . "VBELN" , "MAKT" . "MATNR" , "MAKT" . "MAKTX" , "MAKT" . "SPRAS" , "MARM" . "MEINH" , "MARM" . "UMREZ" , "MARM" . "LAENG" , "MARM" . "MEABM" , "MARM" . "MATNR" , "ADRC" . "NAME1" , "ADRC" . "NAME4" , "ADRC" . "CITY1" , "ADRC" . "CITY2" , "ADRC" . "STREET" , "ADRC" . "POST_CODE1" , "ADRC" . "ADDRNUMBER" , "MLGT" . "LGPLA" , "MLGT" . "MATNR" , "KNA1" . "KUNNR" , "ADR6" . "SMTP_ADDR" , "ADR6" . "ADDRNUMBER" , "ADR2" . "TELNR_CALL" , "ADR2" . "CONSNUMBER" , "ADR2" . "ADDRNUMBER" , "VBFA" . "POSNN" , "VBFA" . "VBELN" , "VBFA" . "POSNV" , "VBFA" . "VBELV" , "VBEP" . "EDATU" , "VBEP" . "POSNR" , "VBEP" . "VBELN"

FROM

"LIPS" INNER JOIN "VBAK" ON "LIPS" . "MANDT" = "VBAK" . "MANDT" AND "VBAK" . "VBELN" = "LIPS" . "VGBEL" LEFT OUTER JOIN"LQUA" ON "LIPS" . "MANDT" = "LQUA" . "MANDT" AND "LQUA" . "MATNR" = "LIPS" . "MATNR" AND "LQUA" . "WERKS" = "LIPS" . "WERKS" INNER JOIN "VBPA" ON "LIPS" . "MANDT" = "VBPA" . "MANDT" AND "VBPA" . "VBELN" = "VBAK" . "VBELN" LEFT OUTER JOIN "LIKP" ON "LIPS" . "MANDT" = "LIKP" . "MANDT" AND "LIKP" . "VBELN" = "LIPS" . "VBELN" LEFT OUTER JOIN "MAKT" ON "LIPS" ."MANDT" = "MAKT" . "MANDT" AND "MAKT" . "MATNR" = "LIPS" . "MATNR" LEFT OUTER JOIN "MARM" ON "LIPS" . "MANDT" = "MARM" . "MANDT" AND "MARM" . "MATNR" = "LIPS" . "MATNR" INNER JOIN "ADRC" ON "LIPS" . "MANDT" = "ADRC" . "CLIENT" AND "ADRC" ."ADDRNUMBER" = "VBPA" . "ADRNR" LEFT OUTER JOIN "MLGT" ON "LIPS" . "MANDT" = "MLGT" . "MANDT" AND "MLGT" . "MATNR" = "LIPS" . "MATNR" INNER JOIN "KNA1" ON "LIPS" . "MANDT" = "KNA1" . "MANDT" AND "KNA1" . "KUNNR" = "VBPA" . "KUNNR" LEFT OUTER JOIN "ADR6" ON "LIPS" . "MANDT" = "ADR6" . "CLIENT" AND "ADR6" . "ADDRNUMBER" = "ADRC" . "ADDRNUMBER" LEFT OUTER JOIN"ADR2" ON "LIPS" . "MANDT" = "ADR2" . "CLIENT" AND "ADR2" . "ADDRNUMBER" = "ADRC" . "ADDRNUMBER" LEFT OUTER JOIN "VBFA"ON "LIPS" . "MANDT" = "VBFA" . "MANDT" AND "VBFA" . "POSNN" = "LIPS" . "POSNR" AND "VBFA" . "VBELN" = "LIPS" . "VBELN" INNER JOIN "VBEP" ON "LIPS" . "MANDT" = "VBEP" . "MANDT" AND "VBEP" . "POSNR" = "VBFA" . "POSNV" AND "VBEP" . "VBELN" = "

VBFA" . "VBELV"

WHERE

"LIPS" . "MANDT" = ? AND "LIPS" . "WERKS" = ? AND "VBPA" . "PARVW" = ?

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,01 |
| Maximal CPU Consumption per Hour [%] ( 30.04.2026 between 14:00 and 15:00 ) | 0,02 |
| Maximal Memory Consumption [%] ( 30.04.2026 -- 14:35:16 ) | 8,26 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Total Memory) |

#### 17.6.1.1 Analysis of Where Clause

| Table | Field | Operator |
| --- | --- | --- |
| ? | MANDT | = |
| ? | PARVW | = |
| ? | WERKS | = |

#### 17.6.1.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 49 | 49.158.293 | 49.158.293 | 49.158.293 |
| PREPARATION | 0 | 245.023 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.6.1.3 Memory Consumption

The following table provides an overview of the memory consumption of the analyzed SQL statement as obtained from the monitoring view M_SQL_PLAN_STATISTICS (or – if not yet available – M_SQL_PLAN_CACHE), that is, without taking a specific time interval into account.

| Activity | Average Memory [MB] | Minimal Memory [MB] | Maximal Memory [MB] |
| --- | --- | --- | --- |
| EXECUTION_MEMORY_SIZE | 53.560,1 | 38.691,5 | 68.428,7 |

##### High Memory Consumption

The memory consumption of this statement is relatively high when compared with the minimum "effective allocation limit" of the index server(s) as obtained from M_SERVICE_MEMORY. See the following table for details. Note that the excessive memory consumption of a single statement might impact the stability of the whole SAP HANA system. See [SAP Note 1999997](https://launchpad.support.sap.com/#/notes/1999997) for details and for an option to restrict the maximum memory allocated by a single statement.

| (Minimal) Effective Allocation Limit [GB] | 457,3 |
| --- | --- |
| Maximal Statement Size / Effective Allocation Limit [%] | 14,6 |
| Average Statement Size / Effective Allocation Limit [%] | 11,4 |

#### 17.6.1.4 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.6.1.5 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| LIKP | SAPSP4 | COLUMN | Table not partitioned | 1.056.668 | bswprddb01 |
| ADR2 | SAPSP4 | COLUMN | Table not partitioned | 617.920 | bswprddb01 |
| ADR6 | SAPSP4 | COLUMN | Table not partitioned | 448.100 | bswprddb01 |
| ADRC | SAPSP4 | COLUMN | Table not partitioned | 337.060 | bswprddb01 |
| KNA1 | SAPSP4 | COLUMN | Table not partitioned | 6.530 | bswprddb01 |

#### 17.6.1.6 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding |
| --- | --- | --- | --- | --- | --- |
| S4P | SQ00 | AQA0UK==========HOTTIES_PICK== | 352 | 07.04.2026 |  |

### 17.6.2 SQL Statement a0a33f001aab35f98bfcb496f422cc54

SELECT

ZZHDBSSA1.*

FROM

(WITH BASIS_INFO AS ( SELECT HOST, ONLY_POTENTIALLY_CRITICAL_RESULTS, SKIP_LESS_RELEVANT_CHECKS_IN_SYSTEMDB, SKIP_OVERLAPPING_CHECKS_IN_SYSTEMDB, MAX_VALUE_LENGTH, CHECK_ID, CHECK_GROUP, CHECK_ID_PREFIX,MAP(SHORTTERM_DAYS, -1, 99999, SHORTTERM_DAYS) SHORTTERM_DAYS, MAP(MIDTERM_DAYS, -1, 99999, MIDTERM_DAYS) MIDTERM_DAYS, MAP(LONGTERM_DAYS, -1, 99999, LONGTERM_DAYS) LONGTERM_DAYS, ORDER_BY

FROM

( SELECT /* Modification section */ '-GDPR-' HOST, '-GDPR-'ONLY_POTENTIALLY_CRITICAL_RESULTS, '-GDPR-' SKIP_LESS_RELEVANT_CHECKS_IN_SYSTEMDB, '-GDPR-' SKIP_OVERLAPPING_CHECKS_IN_SYSTEMDB, 60 MAX_VALUE_LENGTH, -1 CHECK_ID, '-GDPR-' CHECK_GROUP, '-GDPR-' CHECK_ID_PREFIX, 1 SHORTTERM_DAYS, 7 MIDTERM_DAYS, 31 LONGTERM_DAYS, '-GDPR-' ORDER_BY /* HOST, CHECK */

FROM DUMMY ) ), TEMP_M_CS_TABLES AS ( SELECT *

FROM M_CS_TABLES ), TEMP_M_BACKUP_CATALOG AS ( SELECT *

FROM M_BACKUP_CATALOG ), TEMP_M_BACKUP_CATALOG_FILES AS ( SELECT *

FROM M_BACKUP_CATALOG_FILES ), TEMP_M_VOLUME_FILES AS ( SELECT *

FROM M_VOLUME_FILES ), TEMP_M_TABLE_LOB_STATISTICS AS ( SELECT *

FROM

M_TABLE_LOB_STATISTICS ), GENERAL_INFO AS ( SELECT ALLOC_LIM_GB + MAP(PMEM_USED, '-GDPR-', PMEM_SIZE_GB, 0) ALLOC_LIM_GB, TOTAL_ALLOC_LIM_GB + MAP(PMEM_USED, '-GDPR-', PMEM_SIZE_GB, 0) TOTAL_ALLOC_LIM_GB, COL_MEM_GB, DATA_DISK_GB, DB_TYPE, PMEM_USED, FRO_USED, REVISION, STARTUP_TIME, IFNULL(THREAD_SAMPLES_FILTER_FACTOR, 50) THREAD_SAMPLES_FILTER_FACTOR, UPTIME_S

FROM ( SELECT IFNULL(TO_NUMBER(VALUE), 50) THREAD_SAMPLES_FILTER_FACTOR

FROM

DUMMY LEFT OUTER JOIN _SYS_STATISTICS.STATISTICS_PROPERTIES ON KEY = '-GDPR-' ), ( SELECTMAX(ALLOC_LIM_GB) ALLOC_LIM_GB, SUM(ALLOC_LIM_GB) TOTAL_ALLOC_LIM_GB

FROM ( SELECT S.HOST, MAX(S.ALLOCATION_LIMIT) / 1024 / 1024 / 1024 ALLOC_LIM_GB

FROM

M_DATABASE D, M_HOST_RESOURCE_UTILIZATION H, M_SERVICE_MEMORY S

WHERE

H.HOST = S.HOST AND ( D.DATABASE_NAME = '-GDPR-' AND S.SERVICE_NAME = '-GDPR-' OR S.SERVICE_NA

ME = '-GDPR-' )

GROUP BY S.HOST ) ), ( SELECT SUM(USED_SIZE) / 1024 / 1024 / 1024 DATA_DISK_GB

FROM

M_VOLUME_FILES

WHERE

FILE_TYPE = '-GDPR-' ), ( SELECT MAX(START_TIME) STARTUP_TIME, MIN(SECONDS_BETWEEN(START_TIME, CURRENT_TIMESTAMP)) UPTIME_S

FROM

M_DATABASE ), ( SELECT SUM(MEMORY_SIZE_IN_TOTAL + PERSISTENT_MEMORY_SIZE_IN_TOTAL) / 1024 / 1024 / 1024COL_MEM_GB

FROM

TEMP_M_CS_TABLES ), ( SELECT CASE WHEN MAX(P.VALUE) = '-GDPR-' AND MAX(D.DATABASE_NAME) = '-GDPR-' THEN'-GDPR-' ELSE '-GDPR-' END DB_TYPE

FROM

M_CONFIGURATION_PARAMETER_VALUES P, M_DATABASE D

WHERE

P.FILE_NAME = '-GDPR-' AND P.SECTION = '-GDPR-' AND P.KEY = '-GDPR-' ), ( SELECT TO_NUMBER(SUBSTR(VALUE, LOCATE(VALUE, '-GDPR-', 1, 2) + 1, LOCATE(VALUE, '-GDPR-', 1, 3) - LOCATE(VALUE, '-GDPR-', 1, 2) - 1) || MAP(LOCATE(VALUE, '-GDPR-', 1, 4), 0, ''-GDPR-'.'-GDPR-'.'-GDPR-'.'-GDPR-'.'-GDPR-'System'-GDPR-'Version'-GDPR-' '-GDPR-'X'-GDPR-'tmpfs'-GDPR-' '-GDPR-'X'-GDPR-'tmpfs'-GDPR-'BLANK_LINE'-GDPR-''-GDPR-'INFO_LINE'-GDPR-'****'-GDPR-'X'-GDPR-'HOST'-GDPR-''-GDPR-''-GDPR-'X'-GDPR-'HOST'-GDPR-''-GDPR-''-GDPR-'999999'-GDPR-'never'-GDPR-'999999.00'-GDPR-'never'-GDPR-'-999999'-GDPR-'never'-GDPR-'-999999.00'-GDPR-'never'-GDPR-'n/a'-GDPR-'...'-GDPR-'any'-GDPR-''-GDPR-'='-GDPR-'like'-GDPR-'between'-GDPR-'-'-GDPR-'to'-GDPR-'-'-GDPR-'999999'-GDPR-'999999.00'-GDPR-'-999999'-GDPR-'-999999.00'-GDPR-'X'-GDPR-'999999'-GDPR-'999999.00'-GDPR-'-999999'-GDPR-'-999999.00'-GDPR-' '-GDPR-'any'-GDPR-'NONE'-GDPR-'N/A'-GDPR-' '-GDPR-'not'-GDPR-'X'-GDPR-'='-GDPR-'X'-GDPR-'>='-GDPR-'X'-GDPR-'>'-GDPR-'X'-GDPR-'='-GDPR-'X'-GDPR-'X'-GDPR-'between'-GDPR-'-'-GDPR-'-'-GDPR-'X'-GDPR-'like'-GDPR-'X'-GDPR-'not like'-GDPR-'X'-GDPR-''-GDPR-'CONFIGURED_TIME_INTERVALS'-GDPR-''-GDPR-'short-term: '-GDPR-', mid-term: '-GDPR-', long-term: '-GDPR-'BLANK_LINE'-GDPR-''-GDPR-''-GDPR-'INFO_LINE'-GDPR-''-GDPR-''-GDPR-'LOG_WAIT_RATIO'-GDPR-'LOG_RACE_RATIO'-GDPR-''-GDPR-'HIGH_CRIT_SAVEPOINT_PHASE'-GDPR-'AVG_CRIT_SAVEPOINT_PHASE'-GDPR-'MAX_CRIT_SAVEPOINT_PHASE'-GDPR-'WAITFORLOCK_SAVEPOINT_PHASE'-GDPR-'CRIT_SAVEPOINT_PHASE'-GDPR-'WAITFORFLUSH_SAVEPOINT_PHASE'-GDPR-'HIGH_CRIT_SAVEPOINT_PHASE'-GDPR-'AVG_CRIT_SAVEPOINT_PHASE'-GDPR-'MAX_CRIT_SAVEPOINT_PHASE'-GDPR-'WAITFORLOCK_SAVEPOINT_PHASE'-GDPR-'CRIT_SAVEPOINT_PHASE'-GDPR-'WAITFORFLUSH_SAVEPOINT_PHASE'-GDPR-'TIME_SINCE_LAST_SAVEPOINT'-GDPR-'DISK_DATA_FRAGMENTATION'-GDPR-''-GDPR-'999999'-GDPR-'DATA'-GDPR-''-GDPR-'OLDEST_REPLICATION_SNAPSHOT'-GDPR-'n/a'-GDPR-'OL

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,53 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 07:00 and 08:00 ) | 0,43 |
| Maximal Memory Consumption [%] ( 27.04.2026 -- 04:44:52 ) | 3,76 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (CPU Peak Hour) |

#### 17.6.2.1 Analysis of Where Clause

| Table | Field | Operator |
| --- | --- | --- |
| ? | DATABASE_NAME | = |
| ? | HOST | = |
| ? | SERVICE_NAME | = |

#### 17.6.2.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.6.2.3 Correlation with Index Server Resource Consumption

The distribution of thread samples with the status "Running" correlates strongly with the overall CPU or memory consumption of the system. Such a correlation indicates that this statement might be responsible for peaks in the memory or CPU consumption.

| Distiribution | Correlation Coefficient | Comment |
| --- | --- | --- |
| CPU consumption index server(s) - Threads (running) from this SQL statement | 0,64 | strong correlation |
| Memory consumption index server(s) - Threads (running) from this SQL Statement | 0,68 | strong correlation |

#### 17.6.2.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| CS_COLUMNS_ | SYS | ROW | Table not partitioned | 2.278.841 | bswprddb01 |
| CS_TABLES_ | SYS | ROW | Table not partitioned | 159.330 | bswprddb01 |
| CS_CONCAT_ATTRIBUTES_ | SYS | ROW | Table not partitioned | 2.914 | bswprddb01 |
| DUMMY | SYS | ROW | Table not partitioned | 1 | bswprddb01 |
| CLIENTSIDE_ENCRYPTION_COLUMN_KEYS_ | SYS | ROW | Table not partitioned | 0 | bswprddb01 |

#### 17.6.2.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | /BDL/TASK_PROCESSOR | CL_SQL_STATEMENT==============CM00L | 3 | 23.04.2019 | [GRAY] | BC-DB-DBI | DB-Independent Database Interface |

### 17.6.3 SQL Statement d2040795d0fa208871e56bd08995dfee

SELECT

ZZHDBSSA1.*

FROM

(WITH BASIS_INFO AS ( SELECT HOST, ONLY_POTENTIALLY_CRITICAL_RESULTS, SKIP_LESS_RELEVANT_CHECKS_IN_SYSTEMDB, SKIP_OVERLAPPING_CHECKS_IN_SYSTEMDB, MAX_VALUE_LENGTH, CHECK_ID, CHECK_GROUP, CHECK_ID_PREFIX,MAP(SHORTTERM_DAYS, -1, 99999, SHORTTERM_DAYS) SHORTTERM_DAYS, MAP(MIDTERM_DAYS, -1, 99999, MIDTERM_DAYS) MIDTERM_DAYS, MAP(LONGTERM_DAYS, -1, 99999, LONGTERM_DAYS) LONGTERM_DAYS, ORDER_BY

FROM

( SELECT /* Modification section */ '-GDPR-' HOST, '-GDPR-'ONLY_POTENTIALLY_CRITICAL_RESULTS, '-GDPR-' SKIP_LESS_RELEVANT_CHECKS_IN_SYSTEMDB, '-GDPR-' SKIP_OVERLAPPING_CHECKS_IN_SYSTEMDB, 60 MAX_VALUE_LENGTH, -1 CHECK_ID, '-GDPR-' CHECK_GROUP, '-GDPR-' CHECK_ID_PREFIX, 1 SHORTTERM_DAYS, 7 MIDTERM_DAYS, 31 LONGTERM_DAYS, '-GDPR-' ORDER_BY /* HOST, CHECK */

FROM DUMMY ) ), TEMP_M_CS_TABLES AS ( SELECT *

FROM M_CS_TABLES ), TEMP_M_MVCC_TABLES AS ( SELECT *

FROM M_MVCC_TABLES ), TEMP_M_TRANSACTIONS AS ( SELECT *

FROM M_TRANSACTIONS ), TEMP_M_TABLE_LOB_STATISTICS AS ( SELECT *

FROM M_TABLE_LOB_STATISTICS ), TEMP_M_TABLES AS ( SELECT *

FROM M_TABLES ), TEMP_M_CONNECTIONS AS ( SELECT *

FROM

M_CONNECTIONS ), GENERAL_INFO AS ( SELECT ALLOC_LIM_GB + MAP(PMEM_USED, '-GDPR-', PMEM_SIZE_GB, 0) ALLOC_LIM_GB, TOTAL_ALLOC_LIM_GB + MAP(PMEM_USED, '-GDPR-', PMEM_SIZE_GB, 0) TOTAL_ALLOC_LIM_GB, COL_MEM_GB, DATA_DISK_GB, DB_TYPE, PMEM_USED, FRO_USED, REVISION, STARTUP_TIME, IFNULL(THREAD_SAMPLES_FILTER_FACTOR, 50) THREAD_SAMPLES_FILTER_FACTOR, UPTIME_S

FROM ( SELECT IFNULL(TO_NUMBER(VALUE), 50) THREAD_SAMPLES_FILTER_FACTOR

FROM

DUMMY LEFT OUTER JOIN _SYS_STATISTICS.STATISTICS_PROPERTIES ON KEY = '-GDPR-' ), ( SELECTMAX(ALLOC_LIM_GB) ALLOC_LIM_GB, SUM(ALLOC_LIM_GB) TOTAL_ALLOC_LIM_GB

FROM ( SELECT S.HOST, MAX(S.ALLOCATION_LIMIT) / 1024 / 1024 / 1024 ALLOC_LIM_GB

FROM

M_DATABASE D, M_HOST_RESOURCE_UTILIZATION H, M_SERVICE_MEMORY S

WHERE

H.HOST = S.HOST AND ( D.DATABASE_NAME = '-GDPR-' AND S.SERVICE_NAME = '-GDPR-' OR S.SERVICE_NA

ME = '-GDPR-' )

GROUP BY S.HOST ) ), ( SELECT SUM(USED_SIZE) / 1024 / 1024 / 1024 DATA_DISK_GB

FROM

M_VOLUME_FILES

WHERE

FILE_TYPE = '-GDPR-' ), ( SELECT MAX(START_TIME) STARTUP_TIME, MIN(SECONDS_BETWEEN(START_TIME, CURRENT_TIMESTAMP)) UPTIME_S

FROM

M_DATABASE ), ( SELECT SUM(MEMORY_SIZE_IN_TOTAL + PERSISTENT_MEMORY_SIZE_IN_TOTAL) / 1024 / 1024 / 1024COL_MEM_GB

FROM

TEMP_M_CS_TABLES ), ( SELECT CASE WHEN MAX(P.VALUE) = '-GDPR-' AND MAX(D.DATABASE_NAME) = '-GDPR-' THEN'-GDPR-' ELSE '-GDPR-' END DB_TYPE

FROM

M_CONFIGURATION_PARAMETER_VALUES P, M_DATABASE D

WHERE

P.FILE_NAME = '-GDPR-' AND P.SECTION = '-GDPR-' AND P.KEY = '-GDPR-' ), ( SELECT TO_NUMBER(SUBSTR(VALUE, LOCATE(VALUE, '-GDPR-', 1, 2) + 1, LOCATE(VALUE, '-GDPR-', 1, 3) - LOCATE(VALUE, '-GDPR-', 1, 2) - 1) || MAP(LOCATE(VALUE, '-GDPR-', 1, 4), 0, ''-GDPR-'.'-GDPR-'.'-GDPR-'.'-GDPR-'.'-GDPR-'System'-GDPR-'Version'-GDPR-' '-GDPR-'X'-GDPR-'tmpfs'-GDPR-' '-GDPR-'X'-GDPR-'tmpfs'-GDPR-'BLANK_LINE'-GDPR-''-GDPR-'INFO_LINE'-GDPR-'****'-GDPR-'X'-GDPR-'HOST'-GDPR-''-GDPR-''-GDPR-'X'-GDPR-'HOST'-GDPR-''-GDPR-''-GDPR-'999999'-GDPR-'never'-GDPR-'999999.00'-GDPR-'never'-GDPR-'-999999'-GDPR-'never'-GDPR-'-999999.00'-GDPR-'never'-GDPR-'n/a'-GDPR-'...'-GDPR-'any'-GDPR-''-GDPR-'='-GDPR-'like'-GDPR-'between'-GDPR-'-'-GDPR-'to'-GDPR-'-'-GDPR-'999999'-GDPR-'999999.00'-GDPR-'-999999'-GDPR-'-999999.00'-GDPR-'X'-GDPR-'999999'-GDPR-'999999.00'-GDPR-'-999999'-GDPR-'-999999.00'-GDPR-' '-GDPR-'any'-GDPR-'NONE'-GDPR-'N/A'-GDPR-' '-GDPR-'not'-GDPR-'X'-GDPR-'='-GDPR-'X'-GDPR-'>='-GDPR-'X'-GDPR-'>'-GDPR-'X'-GDPR-'='-GDPR-'X'-GDPR-'X'-GDPR-'between'-GDPR-'-'-GDPR-'-'-GDPR-'X'-GDPR-'like'-GDPR-'X'-GDPR-'not like'-GDPR-'X'-GDPR-''-GDPR-'CONFIGURED_TIME_INTERVALS'-GDPR-''-GDPR-'short-term: '-GDPR-', mid-term: '-GDPR-', long-term: '-GDPR-'BLANK_LINE'-GDPR-''-GDPR-''-GDPR-'INFO_LINE'-GDPR-''-GDPR-''-GDPR-'VERSIONS_ROW_STORE_CURR'-GDPR-'VERSIONS_ROW_STORE_SHORTTERM'-GDPR-'COMMIT_ID_RANGE_SHORTTERM'-GDPR-'VERSIONS_ROW_STORE_SHORTTERM'-GDPR-'COMMIT_ID_RANGE_SHORTTERM'-GDPR-'MVCC_REC_VERSIONS_ROW_STORE'-GDPR-'MAX_VERSIONS_PER_RECORD'-GDPR-'MVCC_TAB_VERSIONS_ROW_STORE'-GDPR-''-GDPR-'MVCC_TRANS_START_TIME'-GDPR-''-GDPR-'0'-GDPR-'MIN_SNAPSHOT_TS'-GDPR-'ACTIVE_COMMIT_ID_RANGE'-GDPR-'ACTIVE_COMMIT_ID_RANGE'-GDPR-'MIN_SNAPSHOT_TS'-GDPR-'GLOBAL_TS'-GDPR-'ACTIVE_UPDATE_TRANS_CURR'-GDPR-''-GDPR-'0.00'-GDPR-'ACTIVE'-GDPR-'ACTIVE_UPDATE_TRANS_HIST'-GDPR-''-GDPR-'ACTIVE_SQL_CUR

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,53 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 04:00 and 05:00 ) | 0,60 |
| Maximal Memory Consumption [%] ( 27.04.2026 -- 05:46:03 ) | 3,62 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (CPU Peak Hour) |

#### 17.6.3.1 Analysis of Where Clause

| Table | Field | Operator |
| --- | --- | --- |
| ? | DATABASE_NAME | = |
| ? | HOST | = |
| ? | SERVICE_NAME | = |

#### 17.6.3.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.6.3.3 Correlation with Index Server Resource Consumption

The distribution of thread samples with the status "Running" correlates strongly with the overall CPU or memory consumption of the system. Such a correlation indicates that this statement might be responsible for peaks in the memory or CPU consumption.

| Distiribution | Correlation Coefficient | Comment |
| --- | --- | --- |
| CPU consumption index server(s) - Threads (running) from this SQL statement | 0,70 | strong correlation |
| Memory consumption index server(s) - Threads (running) from this SQL Statement | 0,67 | strong correlation |

#### 17.6.3.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| CS_COLUMNS_ | SYS | ROW | Table not partitioned | 2.278.841 | bswprddb01 |
| CS_TABLES_ | SYS | ROW | Table not partitioned | 159.330 | bswprddb01 |
| CS_CONCAT_ATTRIBUTES_ | SYS | ROW | Table not partitioned | 2.914 | bswprddb01 |
| DUMMY | SYS | ROW | Table not partitioned | 1 | bswprddb01 |
| CLIENTSIDE_ENCRYPTION_COLUMN_KEYS_ | SYS | ROW | Table not partitioned | 0 | bswprddb01 |

#### 17.6.3.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | /BDL/TASK_PROCESSOR | CL_SQL_STATEMENT==============CM00L | 3 | 23.04.2019 | [GRAY] | BC-DB-DBI | DB-Independent Database Interface |

### 17.6.4 SQL Statement 7e3b27c93bd4fd7f2dfba19861cb957c

SELECT

ZZHDBSSA1.*

FROM

(SELECT /* [NAME] HANA_Tables_ColumnStore_Columns_2.00.040+ [DESCRIPTION] - Provides information for columns located in column store [SOURCE] - SAP Note 1969700 [DETAILS AND RESTRICTIONS] - M_CS_ALL_COLUMN_STATISTICS available withSAP HANA >= 2.00.030 - M_CS_ALL_COLUMNS.PERSISTENT_MEMORY_SIZE_IN_TOTAL available with SAP HANA >= 2.00.030 - M_CS_ALL_COLUMNS.NUMA_NODE_INDEX available with SAP HANA >= 2.00.040 [VALID FOR] - Revisions: >= 2.00.040 [SQL COMMAND VERSION] - 2014/03/13: 1.0 (initial version) - 2014/04/02: 1.1 (NUM_DISTINCT included) - 2014/07/09: 1.2 (LOADED added) - 2014/10/20: 1.3 (OBJECT_LEVEL added) - 2015/01/17: 1.4 (FULLTEXT_INDEXES included) - 2015/07/21: 1.5 (EXCLUDE_PK_AND_UNIQUE included) - 2017/03/21: 1.6 (LAST_LOAD_TIME included) - 2018/12/17: 1.7 (dedicated 2.00.030+ version including M_CS_ALL_COLUMN_STATISTICS) - 2019/03/16: 1.8 (PERSISTENT_MEMORY included) - 2019/06/05: 1.9 (persistent memory details considered) - 2019/06/26: 2.0 (COLUMN_NAME filter added) - 2019/11/03: 2.1 (ONLY_PK_AND_UNIQUE added) - 2020/09/24: 2.2 (dedicated 2.00.040+ version including NUMA node information, PART_ID filter added) - 2020/10/01: 2.3 (PERSISTENCY_TYPE and LOAD_UNIT added) - 2020/12/05: 2.4 (MEM_PAGED_MB added) - 2021/06/15: 2.5 (DISK_MB and DISK_PAGE_MB added) [INVOLVED TABLES] - CS_JOIN_CONDITIONS - CONSTRAINTS - INDEX_COLUMNS - INDEXES - M_CS_ALL_COLUMNS - M_CS_ALL_COLUMN_STATISTICS - M_CS_COLUMNS_PERSISTENCE - TABLE_COLUMNS [INPUT PARAMETERS] - HOST Host name '-GDPR-' --> Specic host saphana01 '-GDPR-' --> All hosts starting with saphana '-GDPR-' --> All hosts - PORT Port number '-GDPR-' --> Port 30007 '-GDPR-' --> All ports ending with '-GDPR-' '-GDPR-' --> No restriction to ports - SERVICE_NAME Service name '-GDPR-' --> Specific service indexserver'-GDPR-' --> All services ending with '-GDPR-' '-GDPR-' --> All services - SCHEMA_NAME Schema name or pattern '-GDPR-' --> Specific schema SAPSR3 '-GDPR-' --> All schemata starting with '-GDPR-' '-GDPR-' --> All schemata - TABLE_NAME Table name or pattern '-GDPR-' --> Specific table T000 '-GDPR-' --> All tables starting with '-GDPR-' '-GDPR-' --> All tables - COLUMN_NAMEColumn name '-GDPR-' --> Column MATNR '-GDPR-' --> Columns starting with "Z" '-GDPR-' --> No restriction related to columns - PART_ID Partition number 2 --> Only show information for partition number 2 -1 --> No restriction related to partition number - DATA_TYPE Column data type '-GDPR-' --> Type '-GDPR-' '-GDPR-' --> All types containing '-GDPR-' '-GDPR-' --> All types - COLUMN_NAME_LENGTH_LIMIT Maximum length of displayed column name (truncation if name is longer) 40 --> Display a maximum of 40 characters of column name -1 --> Display complete column names - ATTRIBUTE_TYPE Column attribute type '-GDPR-' --> Restriction to columns with internal attribute type '-GDPR-' '-GDPR-' --> Restriction to columns with internal attribute type starting with '-GDPR-' '-GDPR-' --> No restriction by internal attribute type - LOADED Column memory load state '-GDPR-' --> Column loaded into memory '-GDPR-' --> Columns not loaded into memory '-GDPR-' --> No restriction related to column load state - LOAD_UNIT Column load unit '-GDPR-' --> Load unit COLUMN (i.e. loading of complete column) '-GDPR-' --> Load unit PAGE (i.e. page-wise loads) - PAGEABLE Restriction to pageable / non-pageable columns (paged attributes, see SAP Note 1871386) '-GDPR-' --> Only show columns that can be defined as paged attributes '-GDPR-' --> Only show columns that cannot be defined as paged attributes '-GDPR-' --> No restriction related to paged attributes - PERSISTENT_MEMORY Utilization of persistent memory (SAP Note 2700084) '-GDPR-' --> Only show tables using persistent memory '-GDPR-' --> Only show tables not using persistent memory '-GDPR-' --> No restriction related to persistent memory - PERSISTENCE_TYPEPersistence type of column '-GDPR-' --> Persistence type SINGLE '-GDPR-' --> Persistence type VIRTUAL_FILE '-GDPR-' --> No restriction related to persistence type - ONLY_INTERNAL_COLUMNS Activates / deactivates restriction to internal columns '-GDPR-' --> Only internal columns (typically starting with '-GDPR-') are considered '-GDPR-' --> All columns are considered - EXCLUDE_PK_AND_UNIQUE Possibility to exclude columns related to primary keys and unique indexes '-G

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,07 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 05:00 and 06:00 ) | 0,11 |
| Maximal Memory Consumption [%] ( 27.04.2026 -- 05:02:15 ) | 1,67 |

#### 17.6.4.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 35 | 35.204.257 | 35.204.257 | 35.204.257 |
| PREPARATION | 0 | 442.147 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.6.4.2 Memory Consumption

The following table provides an overview of the memory consumption of the analyzed SQL statement as obtained from the monitoring view M_SQL_PLAN_STATISTICS (or – if not yet available – M_SQL_PLAN_CACHE), that is, without taking a specific time interval into account.

| Activity | Average Memory [MB] | Minimal Memory [MB] | Maximal Memory [MB] |
| --- | --- | --- | --- |
| EXECUTION_MEMORY_SIZE | 7.848,9 | 7.848,9 | 7.848,9 |

##### High Memory Consumption

The memory consumption of this statement is relatively high when compared with the minimum "effective allocation limit" of the index server(s) as obtained from M_SERVICE_MEMORY. See the following table for details. Note that the excessive memory consumption of a single statement might impact the stability of the whole SAP HANA system. See [SAP Note 1999997](https://launchpad.support.sap.com/#/notes/1999997) for details and for an option to restrict the maximum memory allocated by a single statement.

| (Minimal) Effective Allocation Limit [GB] | 457,3 |
| --- | --- |
| Maximal Statement Size / Effective Allocation Limit [%] | 1,7 |
| Average Statement Size / Effective Allocation Limit [%] | 1,7 |

#### 17.6.4.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.6.4.4 Correlation with Index Server Resource Consumption

The distribution of thread samples with the status "Running" correlates strongly with the overall CPU or memory consumption of the system. Such a correlation indicates that this statement might be responsible for peaks in the memory or CPU consumption.

| Distiribution | Correlation Coefficient | Comment |
| --- | --- | --- |
| CPU consumption index server(s) - Threads (running) from this SQL statement | 0,59 | strong correlation |
| Memory consumption index server(s) - Threads (running) from this SQL Statement | 0,40 | medium correlation |

#### 17.6.4.5 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| CS_COLUMNS_ | SYS | ROW | Table not partitioned | 2.278.841 | bswprddb01 |
| CS_JOIN_CONSTRAINTS_ | SYS | ROW | Table not partitioned | 16.800 | bswprddb01 |
| CS_JOIN_CONDITIONS_ | SYS | ROW | Table not partitioned | 14.632 | bswprddb01 |
| CS_CONCAT_ATTRIBUTES_ | SYS | ROW | Table not partitioned | 2.914 | bswprddb01 |
| CLIENTSIDE_ENCRYPTION_COLUMN_KEYS_ | SYS | ROW | Table not partitioned | 0 | bswprddb01 |

#### 17.6.4.6 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | /BDL/TASK_PROCESSOR | CL_SQL_STATEMENT==============CM00L | 3 | 23.04.2019 | [GRAY] | BC-DB-DBI | DB-Independent Database Interface |

### 17.6.5 SQL Statement 7648c0cbc7b7e85e3631b41aae312071

SELECT

ZZHDBSSA1.*

FROM

(WITH BASIS_INFO AS ( SELECT HOST, ONLY_POTENTIALLY_CRITICAL_RESULTS, SKIP_LESS_RELEVANT_CHECKS_IN_SYSTEMDB, SKIP_OVERLAPPING_CHECKS_IN_SYSTEMDB, MAX_VALUE_LENGTH, CHECK_ID, CHECK_GROUP, CHECK_ID_PREFIX,MAP(SHORTTERM_DAYS, -1, 99999, SHORTTERM_DAYS) SHORTTERM_DAYS, MAP(MIDTERM_DAYS, -1, 99999, MIDTERM_DAYS) MIDTERM_DAYS, MAP(LONGTERM_DAYS, -1, 99999, LONGTERM_DAYS) LONGTERM_DAYS, ORDER_BY

FROM

( SELECT /* Modification section */ '-GDPR-' HOST, '-GDPR-'ONLY_POTENTIALLY_CRITICAL_RESULTS, '-GDPR-' SKIP_LESS_RELEVANT_CHECKS_IN_SYSTEMDB, '-GDPR-' SKIP_OVERLAPPING_CHECKS_IN_SYSTEMDB, 60 MAX_VALUE_LENGTH, -1 CHECK_ID, '-GDPR-' CHECK_GROUP, '-GDPR-' CHECK_ID_PREFIX, 1 SHORTTERM_DAYS, 7 MIDTERM_DAYS, 31 LONGTERM_DAYS, '-GDPR-' ORDER_BY /* HOST, CHECK */

FROM DUMMY ) ), SQL_DATA_AREAS AS ( SELECT '-GDPR-' ALLOCATOR

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROMDUMMY UNION ALL SELECT '-GDPR-'

FROM

DUMMY UNION ALL SELECT '-GDPR-'

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,14 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 04:00 and 05:00 ) | 0,20 |
| Maximal Memory Consumption [%] ( 27.04.2026 -- 04:47:05 ) | 1,54 |

#### 17.6.5.1 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.6.5.2 Correlation with Index Server Resource Consumption

The distribution of thread samples with the status "Running" correlates strongly with the overall CPU or memory consumption of the system. Such a correlation indicates that this statement might be responsible for peaks in the memory or CPU consumption.

| Distiribution | Correlation Coefficient | Comment |
| --- | --- | --- |
| CPU consumption index server(s) - Threads (running) from this SQL statement | 0,45 | medium correlation |
| Memory consumption index server(s) - Threads (running) from this SQL Statement | 0,56 | strong correlation |

#### 17.6.5.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| CS_COLUMNS_ | SYS | ROW | Table not partitioned | 2.278.841 | bswprddb01 |
| CS_TABLES_ | SYS | ROW | Table not partitioned | 159.330 | bswprddb01 |
| CS_CONCAT_ATTRIBUTES_ | SYS | ROW | Table not partitioned | 2.914 | bswprddb01 |
| DUMMY | SYS | ROW | Table not partitioned | 1 | bswprddb01 |
| CLIENTSIDE_ENCRYPTION_COLUMN_KEYS_ | SYS | ROW | Table not partitioned | 0 | bswprddb01 |

#### 17.6.5.4 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | /BDL/TASK_PROCESSOR | CL_SQL_STATEMENT==============CM00L | 3 | 23.04.2019 | [GRAY] | BC-DB-DBI | DB-Independent Database Interface |

## 17.7 Top Statements (Thread Samples)

This section shows the top statements according to the number of observed "threads" ("Number of Samples") in the SERVICE THREAD SAMPLES. A statement might occupy a high number of threads if (a) it has a long execution time, (b) it is executed very often, or (c) it has a highly parallelized execution. In any case, it shows statements with a high resource consumption on the SAP HANA database.

See the following table for details of the selection:

| Database Start | 07.03.2026 -- 16:47:19 |
| --- | --- |
| Data Collection | 04.05.2026 -- 05:18:09 |
| Analysis Type | Analysis of Thread Samples |
| Data Source | HOST_SERVICE_THREAD_SAMPLES |
| First Day | 27.04.2026 |
| Last Day | 03.05.2026 |

The selected statements - identified by their "Statement Hash" - are listed in the following table. Further details of these statements can be found in the subsections.

| Statement Hash | Time / Execution [us] | Records / Execution | Time / Record [us] | Number of Samples |
| --- | --- | --- | --- | --- |
| 9aaf8105bdad5308ab706eea28078d28 | 413.120,4 | 0,0 | 0,0 | 581 |
| 237f7f6ff65013fa3016a8b40d6e4772 | 1.773.289,9 | 738.710,2 | 2,4 | 316 |
| b61a4a7ff31225a908196ac2ff49392b | 16.727.653,8 | 3,0 | 5.631.421,3 | 246 |
| 1fa05502938f0afe1a4a782b6b9bd775 | 3.345.235,1 | 1,0 | 3.345.235,1 | 237 |
| dc718a097243ad453d8133c7742ba743 | 2.775.533,5 | 1,0 | 2.775.533,5 | 213 |

### 17.7.1 SQL Statement 9aaf8105bdad5308ab706eea28078d28

/* procedure: "_SYS_STATISTICS"."ALERT_BACKUP_LONG_LOG_BACKUP" variable: BACKUPCATALOG line: 21 col: 104 (at pos 1788) */ SELECT SECONDS_BETWEEN (SYS_START_TIME, CURRENT_TIMESTAMP) "RUNNING", backup_id

FROM_SYS_STATISTICS.source_alert_65_backup_catalog where backup_id IN ( select min(backup_id)

FROM_SYS_STATISTICS.source_alert_65_backup_catalog_files where backup_id IN ( select backup_id

FROM

_SYS_STATISTICS.source_alert_65_backup_catalog

WHERE

"STATE_NAME" = '-GDPR-' and "ENTRY_TYPE_NAME" = '-GDPR-')

GROUP BY

destination_path)

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 6,98 |
| Contribution to Total Execution Time [%] | 3,66 |
| Maximal CPU Consumption per Hour [%] ( 30.04.2026 between 14:00 and 15:00 ) | 0,45 |

#### 17.7.1.1 Known Issue

Information about this statement (as identified by its STATEMENT_HASH) can be found in the following SAP Note:

**Recommendation:** Check the mentioned SAP Note(s) for the recommendation concerning the statement and apply the recommendation if applicable.

| STATEMENT_HASH | SAP Note | Type | Object |
| --- | --- | --- | --- |
| 9aaf8105bdad5308ab706eea28078d28 | 2000002 | CALL | ALERT_BACKUP_LONG_LOG_BACKUP |

#### 17.7.1.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- |
| TOTAL EXECUTION | 413.120 | 347.828 | 654.586 |
| PREPARATION | 0 |  |  |
| LOCK DURATION | 0 |  |  |

#### 17.7.1.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.7.1.4 Root Statement

The following table shows details on the "ROOT STATEMENT", which is responsible for the observed SQL statement.

| ROOT_STATEMENT_HASH | ROOT_STATEMENT_TEXT | Samples |
| --- | --- | --- |
| d6fd6678833f9a2e25e7b53239c50e9a | call _SYS_STATISTICS.STATISTICS_SCHEDULABLEWRAPPER('-GDPR-', ?, ?, ?, ?) | 787 |

#### 17.7.1.5 Internal SQL Statement

This SQL statement was executed from an internal database connection.

### 17.7.2 SQL Statement 237f7f6ff65013fa3016a8b40d6e4772

SELECT

/* FDA READ */ "MSEG" . "MBLNR" , "MSEG" . "MJAHR" , "MSEG" . "ZEILE" , "MSEG" . "CHARG"

FROM

/* Redirected table: MSEG */ "NSDM_V_MSEG" "MSEG" INNER JOIN /* Redirected table: MKPF */ "NSDM_V_MKPF" "MKPF" ON "MSEG"

. "MANDT" = "MKPF" . "MANDT" AND "MSEG" . "MBLNR" = "MKPF" . "MBLNR" AND "MSEG" . "MJAHR" = "MKPF" . "MJAHR"

WHERE

"MSEG" . "MANDT" = ? AND "MSEG" . "CHARG" = ?

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 3,79 |
| Contribution to Total Execution Time [%] | 10,42 |
| Maximal CPU Consumption per Hour [%] ( 01.05.2026 between 13:00 and 14:00 ) | 0,29 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top MATDOC Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top Statements (Total Memory) |
| SAP HANA SQL Statements in H4P -> Statements on Top Scanned Table |

#### 17.7.2.1 Analysis of Where Clause

| Table | Field | Operator |
| --- | --- | --- |
| ? | CHARG | = |
| ? | MANDT | = |

#### 17.7.2.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- |
| TOTAL EXECUTION | 1.773.290 | 1.730.541 | 1.961.674 |
| PREPARATION | 0 |  |  |
| LOCK DURATION | 0 |  |  |

#### 17.7.2.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.7.2.4 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| MATDOC | SAPSP4 | COLUMN | Table not partitioned | 14.064.414 | bswprddb01 |

#### 17.7.2.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding |
| --- | --- | --- | --- | --- | --- |
| S4P | LM01 | ZST60000A_P01 | 47 | 25.12.2025 |  |
| S4P | ZAT6A | ZST60000A_P01 | 47 | 25.12.2025 |  |

### 17.7.3 SQL Statement b61a4a7ff31225a908196ac2ff49392b

SELECT "MCS"."SOURCE", "MCS"."EVENT_TIME", "MCS"."HOST", "MCS"."PORT", "MCS"."SCHEMA_NAME", "MCS"."TABLE_NAME", "ST"."UNLOAD_PRIORITY", "MCS"."REASON", "TG"."GROUP_TYPE", "TG"."SUBTYPE", "TG"."GROUP_NAME", "MCS"."SIZE", "MCS"."OBJ_COUNT"

FROM

( -- unloaded tables SELECT '-GDPR-' AS "SOURCE", LEFT(u."UNLOAD_TIME",13) AS"EVENT_TIME", u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON", SUM(t."ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL") AS "SIZE", COUNT(*) AS "OBJ_COUNT" FROM "SYS"."M_CS_UNLOADS" AS u JOIN "SYS"."M_CS_TABLES" AS t ON (u."HOST" = t."HOST" AND u."PORT" = t."PORT" AND u."SCHEMA_NAME" = t."SCHEMA_NAME" AND u."TABLE_NAME" = t."TABLE_NAME") WHERE u."PART_ID" = -1 -- ie whole table is unloaded AND LEFT (u."UNLOAD_TIME",13) = LEFT (ADD_SECONDS (NOW (), -3600), 13) GROUP BY LEFT(u."UNLOAD_TIME",13), u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON" UNION ALL -- unloads SELECT '-GDPR-' AS "SOURCE", LEFT(u."UNLOAD_TIME",13) AS "EVENT_TIME", u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON", SUM(c."MEMORY_SIZE_IN_TOTAL") AS "SIZE", COUNT(*) AS "OBJ_COUNT" FROM "SYS"."M_CS_UNLOADS" AS u JOIN "SYS"."M_CS_ALL_COLUMNS" AS c ON (u."HOST" = c."HOST" AND u."PORT" = c."PORT" AND u."SCHEMA_NAME" = c."SCHEMA_NAME" AND u."TABLE_NAME" = c."TABLE_NAME" AND u."PART_ID" = c."PART_ID" AND u."COLUMN_NAME" = c."COLUMN_NAME") WHERE u."PART_ID" > -1 --ie only select partitions AND LEFT (u."UNLOAD_TIME",13) = LEFT (ADD_SECONDS (NOW (), -3600), 13) GROUP BY LEFT(u."UNLOAD_TIME",13),u."HOST", u."PORT", u."SCHEMA_NAME", u."TABLE_NAME", u."REASON" UNION ALL -- loads SELECT '-GDPR-' as "SOURCE", LEFT(l."LOAD_TIME", 13) AS "EVENT_TIME", l."HOST", l."PORT", l."SCHEMA_NAME", l."TABLE_NAME", '-GDPR-' AS "REASON", SUM(c."MEMORY_SIZE_IN_TOTAL") AS "SIZE", COUNT(*) AS "OBJ_COUNT" FROM "SYS"."M_CS_LOADS" as l JOIN "SYS"."M_CS_ALL_COLUMNS" as c ON (l."HOST" =c."HOST" AND l."PORT" = c."PORT" AND l."SCHEMA_NAME" = c."SCHEMA_NAME" AND l."TABLE_NAME" = c."TABLE_NAME" AND l."PART_ID" = c."PART_ID" AND l."COLUMN_NAME" = c."COLUMN_NAME") WHERE LEFT (l."LOAD_TIME", 13) = LEFT (ADD_SECONDS (NOW (), -3600), 13) GROUP BY LEFT(l."LOAD_TIME",13),l."HOST", l."PORT", l."SCHEMA_NAME", l."TABLE_NAME" ) AS "MCS" -- left outer jointhe TABLE_GROUPS LEFT OUTER JOIN "SYS"."TABLE_GROUPS" AS "TG" ON "MCS"."TABLE_NAME" = "TG"."TABLE_NAME" AND "MCS"."SCHEMA_NAME" = "TG"."SCHEMA_NAME" -- join SYS.TABLES JOIN "SYS"."TABLES" AS "ST" ON "MCS"."TABLE_NAME" = "ST"."TABLE_NAME" AND "MCS"."SCHEMA_NAME" = "ST"."SCHEMA_NAME"

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 2,95 |
| Contribution to Total Execution Time [%] | 2,47 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 02:00 and 03:00 ) | 0,14 |
| Maximal Memory Consumption [%] ( 01.05.2026 -- 16:05:02 ) | 0,78 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top Statements (Total Memory) |

#### 17.7.3.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- |
| TOTAL EXECUTION | 16.727.654 | 15.495.373 | 32.595.132 |
| PREPARATION | 0 |  |  |
| LOCK DURATION | 0 |  |  |

#### 17.7.3.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.7.3.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| P_INDEXES_ | SYS | ROW | Table not partitioned | 164.793 | bswprddb01 |
| P_PROCEDURES_ | SYS | ROW | Table not partitioned | 22.261 | bswprddb01 |
| RS_TABLES_ | SYS | ROW | Table not partitioned | 21.519 | bswprddb01 |
| P_PRINCIPALS_ | SYS | ROW | Table not partitioned | 238 | bswprddb01 |
| P_SCHEMAS_ | SYS | ROW | Table not partitioned | 107 | bswprddb01 |

### 17.7.4 SQL Statement 1fa05502938f0afe1a4a782b6b9bd775

SELECT ROUND(SUM(MEMORY_SIZE_IN_TOTAL)/(1024*1024*1024),3) AS "Column memory in use (Loaded) GB", ROUND(SUM(MEMORY_SIZE_IN_DELTA)/(1024*1024*1024),3) AS "Memory Size in delta GB", ROUND(SUM(MEMORY_SIZE_IN_HISTORY_MAIN + MEMORY_SIZE_IN_HISTORY_DELTA) / (1024*1024*1024),3) AS "Memory size in history GB", ROUND(SUM( CASE WHEN LOADED = '-GDPR-' THEN '-GDPR-' WHEN ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL < 0 THEN '-GDPR-' ELSE ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL END)/(1024*1024*1024),3) AS "Column memory Unloaded GB"

FROM

M_CS_TABLES

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 2,85 |
| Contribution to Total Execution Time [%] | 2,96 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 14:00 and 15:00 ) | 0,36 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top Statements (Total Memory) |

#### 17.7.4.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- |
| TOTAL EXECUTION | 3.345.235 | 2.900.383 | 60.919.628 |
| PREPARATION | 0 |  |  |
| LOCK DURATION | 0 |  |  |

#### 17.7.4.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.7.4.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| P_PROCEDURES_ | SYS | ROW | Table not partitioned | 22.261 | bswprddb01 |
| P_GRANTEDPRIVS_ | SYS | ROW | Table not partitioned | 4.022 | bswprddb01 |
| P_PRINCIPALS_ | SYS | ROW | Table not partitioned | 238 | bswprddb01 |
| P_SCHEMAS_ | SYS | ROW | Table not partitioned | 107 | bswprddb01 |
| P_OBJTYPES_ | SYS | ROW | Table not partitioned | 39 | bswprddb01 |

### 17.7.5 SQL Statement dc718a097243ad453d8133c7742ba743

SELECT

HOST, ROUND(SUM(MEMORY_SIZE_IN_TOTAL)/(1024*1024*1024),3) AS "Column memory in use (Loaded) GB", ROUND(SUM(MEMORY_SIZE_IN_DELTA)/(1024*1024*1024),3) AS "Memory Size in delta GB", ROUND(SUM(MEMORY_SIZE_IN_HISTORY_MAIN + MEMORY_SIZE_IN_HISTORY_DELTA)/(1024*1024*1024),3) AS "Memory size in history GB", ROUND(SUM(CASE WHEN LOADED = '-GDPR-' THEN'-GDPR-' WHEN ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL < 0 THEN '-GDPR-' ELSE ESTIMATED_MAX_MEMORY_SIZE_IN_TOTAL - MEMORY_SIZE_IN_TOTAL END)/(1024*1024*1024),3) AS "Column memory Unloaded GB" FROM M_CS_TABLES GROUP BY HOST ORDER BY HOST

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 2,56 |
| Contribution to Total Execution Time [%] | 2,46 |
| Maximal CPU Consumption per Hour [%] ( 01.05.2026 between 04:00 and 05:00 ) | 0,51 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statements (Elapsed Time) |
| SAP HANA SQL Statements in H4P -> Top Statements (Total Memory) |

#### 17.7.5.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- |
| TOTAL EXECUTION | 2.775.533 | 2.664.260 | 2.997.579 |
| PREPARATION | 0 |  |  |
| LOCK DURATION | 0 |  |  |

#### 17.7.5.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.7.5.3 Tables

The following lists the tables involved in the SQL statement (maximum of 5)

| Table Name | Schema Name | Table Type | Partition Type | Number of Records | Host |
| --- | --- | --- | --- | --- | --- |
| P_PROCEDURES_ | SYS | ROW | Table not partitioned | 22.261 | bswprddb01 |
| P_GRANTEDPRIVS_ | SYS | ROW | Table not partitioned | 4.022 | bswprddb01 |
| P_PRINCIPALS_ | SYS | ROW | Table not partitioned | 238 | bswprddb01 |
| P_SCHEMAS_ | SYS | ROW | Table not partitioned | 107 | bswprddb01 |
| P_OBJTYPES_ | SYS | ROW | Table not partitioned | 39 | bswprddb01 |

## 17.8 Top Statements (CPU Peak Hour)

This section shows the top statements according to the number of observed "threads" ("Number of Samples") in the SERVICE THREAD SAMPLES. A statement might occupy a high number of threads if (a) it has a long execution time, (b) it is executed very often, or (c) it has a highly parallelized execution. In any case, it shows statements with a high resource consumption on the SAP HANA database.

For this section, the hour with the highest number of thread samples in thread state" "Running" is determined, that is, the "CPU peak hour". The top statements observed in this hour are listed and analyzed.

Hour of Maximal CPU Consumptiion

| From | To |
| --- | --- |
| 27.04.2026 -- 05:00:00 | 27.04.2026 -- 06:00:00 |

See the following table for details of the selection:

| Database Start | 07.03.2026 -- 16:47:19 |
| --- | --- |
| Data Collection | 04.05.2026 -- 05:18:09 |
| Analysis Type | Analysis of Thread Samples |
| Data Source | HOST_SERVICE_THREAD_SAMPLES |
| First Day | 27.04.2026 |
| Last Day | 03.05.2026 |

The selected statements - identified by their "Statement Hash" - are listed in the following table. Further details of these statements can be found in the subsections.

| Statement Hash | Time / Execution [us] | Records / Execution | Time / Record [us] | Number if Samples in CPU Peak Hour |
| --- | --- | --- | --- | --- |
| 323dddb78365d35bdb48b1f85d720252 | 1.677.674,8 | 0,0 | 0,0 | 23 |
| 3cb183ab6c11b06817bdaff653a0be15 | 538.068,0 | 0,0 | 0,0 | 14 |
| a0a33f001aab35f98bfcb496f422cc54 | 0,0 | 0,0 | 0,0 | 13 |
| 38a8e11286f7309f2715c07c270a473b | 2.830.194,4 | 0,0 | 0,0 | 13 |
| d2040795d0fa208871e56bd08995dfee | 0,0 | 0,0 | 0,0 | 13 |

### 17.8.1 SQL Statement 323dddb78365d35bdb48b1f85d720252

/* procedure: "SAPSP4"."CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA" variable: ET_ISSUES line: 298 col: 5 (at pos 12110), procedure: "SAPSP4"."CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA" variable: LT_NO_ACDOCA line: 80 col: 5 (at pos 4472), procedure: "SAPSP4"."CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA" variable: LT_NO_ACDOCA_ADD line: 99 col: 5 (at pos 5058), procedure: "SAPSP4"."CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA" variable: LT_NO_BSEG line: 125 col: 5 (at pos 5932), procedure: "SAPSP4"."CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA" variable: LT_NO_BSEG_ADD line: 146 col: 5 (at pos 6688), procedure: "SAPSP4"."CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA" variable: LT_FIELDS_BSEG line: 167 col: 5 (at pos 7414), procedure: "SAPSP4"."CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA" variable: LT_CLEARING_FIELDS_BSEG line: 193 col: 5 (at pos 8328), procedure: "SAPSP4"."CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA" variable: LT_FIELDS_BSEG_ADD line: 232 col: 5 (at pos 9734), procedure: "SAPSP4"."CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA" variable: LT_CLEARING_FIELDS_BSEG_ADD line: 263 col: 5 (at pos 10817), procedure: "SAPSP4"."CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA#stb2#20220207221012" variable: IT_RLDNR line: 11 col: 3 (at pos 317) */ WITH "_SYS_LT_NO_ACDOCA_2" AS (Select h.mandt, h.bukrs, h.belnr, h.gjahr, h.buzei

FROM

"CL_FINS_RECONCILE_DOCUMENT=>BSEG#covw" as h

WHERE

mandt = __typed_NString__($1, 3) and gjahr = __typed_NString__($2, 4) and bukrs = __typed_NString__($3, 4) and belnr like $4 and ( h_bstat = '-GDPR-' or h_bstat = '-GDPR-' or h_bstat = '-GDPR-' ) and not exists ( select mandt

FROM

"CL_FINS_RECONCILE_DOCUMENT=>ACDOCA#covw" as a

WHERE

h.mandt = a.rclnt and h.bukrs = a.rbukrs and h.belnr = a.belnr and h.gjahr = a.gjahr and h.buzei = a.buzei )), "_SYS_LT_NO_ACDOCA_ADD_2" AS (Select b.mandt, b.bukrs, b.belnr, b.gjahr, right(b.buzei,3) as buzei

FROM

"CL_FINS_RECONCILE_DOCUMENT=>BSEG_ADD#covw" as b join "CL_FINS_RECONCILE_DOCUMENT=>BKPF#covw" as h on h.mandt =

b.mandt and h.bukrs = b.bukrs and h.belnr = b.belnr and h.gjahr = b.gjahr

WHERE

b.mandt = __typed_NString__($1, 3) and b.gjahr = __typed_NString__($2, 4) and b.bukrs = __typed_NString__($3, 4) and b.belnr like $4 and h.mandt = __typed_NString__($1, 3) and h.gjahr = __typed_NString__($2, 4) and h.bukrs = __typed_NString__($3, 4) and h.belnr like $4 and h.bstat = '-GDPR-' and not exists ( select a.rclnt

FROM

"CL_FINS_RECONCILE_DOCUMENT=>ACDOCA#covw" as a

WHERE

b.mandt = a.rclnt and b.bukrs = a.rbukrs and b.belnr = a.belnr and b.gjahr = a.gjahr and right(b.buzei,3) = a.buzei )), "_SYS_LT_NO_BSEG_2" AS (Select a.rclnt as mandt, a.rbukrs as bukrs, a.belnr, a.gjahr, a.buzei

FROM

"CL_FINS_RECONCILE_DOCUMENT=>ACDOCA#covw" as a -- join :it_rldnr as ld -- on ld.rldnr = a.rldnr

WHERE

rclnt = __typed_NString__($1, 3) and gjahr = __typed_NString__($2, 4) and rbukrs = __typed_NString__($3, 4) and belnr like $4 and ( bstat <> '-GDPR-' and bstat <> '-GDPR-' ) and ( mig_source = '-GDPR-' or mig_source ='-GDPR-' or mig_source = '-GDPR-' ) and buzei > '-GDPR-' and not exists ( select b.mandt

FROM

"CL_FINS_RECONCILE_DOCUMENT=>BSEG#covw" as b

WHERE

b.mandt = a.rclnt and b.bukrs = a.rbukrs and b.belnr = a.belnr and b.gjahr = a.gjahr and b.buzei = a.buzei )), "_SYS_LT_NO_BSEG_ADD_2" AS (Select a.rclnt as mandt, a.rbukrs as bukrs, a.belnr, a.gjahr, a.buzei

FROM

"CL_FINS_RECONCILE_DOCUMENT=>ACDOCA#covw" as a -- join :it_rldnr as ld -- on ld.rldnr = a.rldnr

WHERE

rclnt = __typed_NString__($1, 3) and gjahr = __typed_NString__($2, 4) and rbukrs = __typed_NString__($3, 4) and belnr like $4 and bstat = '-GDPR-' and ( mig_source = '-GDPR-' or mig_source = '-GDPR-' or mig_source = '-GDPR-' ) and buzei > '-GDPR-' and not exists ( select b.mandt

FROM

"CL_FINS_RECONCILE_DOCUMENT=>BSEG_ADD#covw" as b

WHERE

b.mandt = a.rclnt and b.bukrs = a.rbukrs and b.belnr = a.belnr and b.gjahr = a.gjahr and right(b.buzei,3) = a.buzei )), "_SYS_IT_RLDNR_2" AS (select *

FROM

"CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA=>P00000#tft#20220207221012"), "_SYS_LT_FIELDS_BSEG_2" AS (Select a.rclnt as mandt, a.rbukrs as bukrs, a.belnr, a.gjahr, a.buzei, a.bldat || '-GDPR-' || a.budat || '-GDPR-' || a.racct asacdoca_fields, b.h_bldat || '-GDPR-' || b.h_budat || '-GDPR-' || b.hkont as bseg_fields

FROM

"CL_FINS_RECONCILE_DOCUMENT=>ACDOCA#covw" as a join "_SYS_IT_RLDNR_2" as ld on ld.rldnr = a.rldnr join "CL_FINS_RECONCILE_DOCUMENT=>BSEG#covw" as b on a.rclnt = b.mandt and a.rbukrs = b.bukrs and a.belnr = b.beln

r and a.gjahr = b.gjahr and a.buzei = b.buzei

WHERE

a.rclnt = __typed_NString__($

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,28 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 05:00 and 06:00 ) | 0,44 |
| Maximal Memory Consumption [%] | 1,03 |

#### 17.8.1.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 191 | 1.671.893 | 19.379 | 6.929.907 |
| PREPARATION | 1 | 5.782 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.8.1.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.8.1.3 Correlation with Index Server Resource Consumption

The distribution of thread samples with the status "Running" correlates strongly with the overall CPU or memory consumption of the system. Such a correlation indicates that this statement might be responsible for peaks in the memory or CPU consumption.

| Distiribution | Correlation Coefficient | Comment |
| --- | --- | --- |
| CPU consumption index server(s) - Threads (running) from this SQL statement | 0,59 | strong correlation |
| Memory consumption index server(s) - Threads (running) from this SQL Statement | 0,40 | medium correlation |

#### 17.8.1.4 Root Statement

The following table shows details on the "ROOT STATEMENT", which is responsible for the observed SQL statement.

| ROOT_STATEMENT_HASH | ROOT_STATEMENT_TEXT | Samples |
| --- | --- | --- |
| 3ff60adadf27fa82129ec692ecc6c1f5 | CALL "CL_FINS_RECONCILE_DOCUMENT=>CHECK_BSEG_VS_ACDOCA#stb2#20220207221012" ( ?, ?, ?, ? ) | 53 |

#### 17.8.1.5 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | Transaction / Jobaname | Report | Line | Last Changed on: | SAP Coding | Application Component | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4P | FINS_REC-04.05.26-05:12:23---1 | CL_FINS_RECONCILE_DOCUMENT====CM005 | 1 | 22.12.2025 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |
| S4P | FINS_REC-04.05.26-05:12:23---2 | CL_FINS_RECONCILE_DOCUMENT====CM005 | 1 | 22.12.2025 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |
| S4P | FINS_REC-04.05.26-05:12:23---3 | CL_FINS_RECONCILE_DOCUMENT====CM005 | 1 | 22.12.2025 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |
| S4P | FINS_REC-04.05.26-05:14:24---3 | CL_FINS_RECONCILE_DOCUMENT====CM005 | 1 | 22.12.2025 | [GRAY] | FIN-MIG | SAP Simple Finance data migration |

#### 17.8.1.6 Internal SQL Statement

This SQL statement was executed from an internal database connection.

### 17.8.2 SQL Statement 3cb183ab6c11b06817bdaff653a0be15

/* procedure: "_SYS_STATISTICS"."ALERT_BACKUP_BACKINT_FALLBACK" variable: CATALOG line: 13 col: 341 (at pos 1345) */ select count(*) LATEST_LOG_BACKUP_USED_FALLBACK

FROM(select BC.BACKUP_ID, BCF.DESTINATION_TYPE_NAME, BCF.BACKINT_FALLBACK_USED, BC.STATE_NAME

FROM

_SYS_STATISTICS.source_alert_143_backup_catalog BC inner join _SYS_STATISTICS.source_alert_143_backup_catalog_

files BCF on BC.BACKUP_ID = BCF.BACKUP_ID

WHERE

BC.ENTRY_TYPE_NAME = '-GDPR-' and BCF.SOURCE_TYPE_NAME = '-GDPR-' order by BC.BACKUP_ID DESC limit 1)

WHERE

BACKINT_FALLBACK_USED = '-GDPR-' or (DESTINATION_TYPE_NAME = '-GDPR-' and STATE_NAME <> '-GDPR-' and (select count(*)

FROM

_SYS_STATISTICS.source_alert_143_statistics_current_alerts

WHERE

ALERT_ID=143) > 0)

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 1,14 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 05:00 and 06:00 ) | 0,27 |

#### 17.8.2.1 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 364 | 538.068 | 470.193 | 676.456 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.8.2.2 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.8.2.3 Root Statement

The following table shows details on the "ROOT STATEMENT", which is responsible for the observed SQL statement.

| ROOT_STATEMENT_HASH | ROOT_STATEMENT_TEXT | Samples |
| --- | --- | --- |
| d6fd6678833f9a2e25e7b53239c50e9a | call _SYS_STATISTICS.STATISTICS_SCHEDULABLEWRAPPER('-GDPR-', ?, ?, ?, ?) | 132 |

#### 17.8.2.4 Origin of SQL Statement

| APPLICATION_NAME | APPLICATION_SOURCE | PASSPORT_ACTION |
| --- | --- | --- |
| Embedded Statistics Server | running ID (143, deletion: no) for 02.05.2026 11:18:37 000 Sat |  |
| Embedded Statistics Server | running ID (143, deletion: no) for 02.05.2026 14:48:37 000 Sat |  |
| Embedded Statistics Server | running ID (143, deletion: no) for 05.04.2026 09:48:37 000 Sun |  |
| Embedded Statistics Server | running ID (143, deletion: no) for 20.04.2026 02:48:37 000 Mon |  |
| Embedded Statistics Server | running ID (143, deletion: no) for 20.04.2026 10:48:37 000 Mon |  |
| Embedded Statistics Server | running ID (143, deletion: no) for 21.04.2026 15:48:37 000 Tue |  |
| Embedded Statistics Server | running ID (143, deletion: no) for 24.03.2026 20:48:37 000 Tue |  |
| Embedded Statistics Server | running ID (143, deletion: no) for 28.03.2026 08:03:37 000 Sat |  |
| Embedded Statistics Server | running ID (143, deletion: no) for 29.04.2026 19:48:37 000 Wed |  |
| Embedded Statistics Server | running ID (143, deletion: no) for 31.03.2026 08:48:37 000 Tue |  |

#### 17.8.2.5 Internal SQL Statement

This SQL statement was executed from an internal database connection.

### 17.8.3 SQL Statement a0a33f001aab35f98bfcb496f422cc54

SELECT

ZZHDBSSA1.*

FROM

(WITH BASIS_INFO AS ( SELECT HOST, ONLY_POTENTIALLY_CRITICAL_RESULTS, SKIP_LESS_RELEVANT_CHECKS_IN_SYSTEMDB, SKIP_OVERLAPPING_CHECKS_IN_SYSTEMDB, MAX_VALUE_LENGTH, CHECK_ID, CHECK_GROUP, CHECK_ID_PRE

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,53 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 07:00 and 08:00 ) | 0,43 |
| Maximal Memory Consumption [%] ( 27.04.2026 -- 04:44:52 ) | 3,76 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statement (Maximal Memory in Trace) |

#### 17.8.3.1 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.8.3.2 Correlation with Index Server Resource Consumption

The distribution of thread samples with the status "Running" correlates strongly with the overall CPU or memory consumption of the system. Such a correlation indicates that this statement might be responsible for peaks in the memory or CPU consumption.

| Distiribution | Correlation Coefficient | Comment |
| --- | --- | --- |
| CPU consumption index server(s) - Threads (running) from this SQL statement | 0,64 | strong correlation |
| Memory consumption index server(s) - Threads (running) from this SQL Statement | 0,68 | strong correlation |

#### 17.8.3.3 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | APPLICATION_SOURCE | Transaction / Jobaname |
| --- | --- | --- |
| DSA | CL_SQL_STATEMENT==============CP:500 | /BDL/TASK_PROCESSOR |
| S4P | CL_SQL_STATEMENT==============CP:703 | /BDL/TASK_PROCESSOR |

### 17.8.4 SQL Statement 38a8e11286f7309f2715c07c270a473b

/* procedure: "_SYS_STATISTICS"."ALERT_DELTA_MEM_MERGE_DOG" variable: TABLES line: 23 col: 104 (at pos 1938) */ select top 100 t0.schema_name || '-GDPR-' || t0.table_name || '-GDPR-' || t0.part_id index_id, t0.host, t0.port, t0.schema_name, t0.table_name, t0.part_id, to_int(t0.memory_size_in_delta / 1024 / 1024) memory_size_in_delta, t0.memory_size_in_delta / least(t1.allocation_limit, t2.allocation_limit) * 100 memory_size_in_delta_percent from _SYS_STATISTICS.source_alert_29_cs_tables t0, _SYS_STATISTICS.source_alert_29_service_memory t1, _SYS_STATISTICS.source_alert_29_host_resource_utilization t2 where t0.host=t1.host and t0.port=t1.port and t2.host= t0.host and t0.memory_size_in_total >= 1024 * 1024 order by t0.memory_size_in_delta desc

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 1,22 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 21:00 and 22:00 ) | 0,34 |

#### 17.8.4.1 Known Issue

Information about this statement (as identified by its STATEMENT_HASH) can be found in the following SAP Note:

**Recommendation:** Check the mentioned SAP Note(s) for the recommendation concerning the statement and apply the recommendation if applicable.

| STATEMENT_HASH | SAP Note | Type | Object |
| --- | --- | --- | --- |
| 38a8e11286f7309f2715c07c270a473b | 2000002 | SELECT | M_CS_ALL_COLUMNS, M_CS_COLUMNS, M_CS_TABLES |

#### 17.8.4.2 Time Consumption

The following table gives an overview of the time consumption of the analyzed SQL statement.

| Activity | Total Time [s] | Average Time [us] | Minimal Time [us] | Maximal Time [us] |
| --- | --- | --- | --- | --- |
| TOTAL EXECUTION | 475 | 2.830.194 | 1.813.263 | 4.157.977 |
| PREPARATION | 0 | 0 |  |  |
| LOCK DURATION | 0 | 0 |  |  |

#### 17.8.4.3 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.8.4.4 Root Statement

The following table shows details on the "ROOT STATEMENT", which is responsible for the observed SQL statement.

| ROOT_STATEMENT_HASH | ROOT_STATEMENT_TEXT | Samples |
| --- | --- | --- |
| d6fd6678833f9a2e25e7b53239c50e9a | call _SYS_STATISTICS.STATISTICS_SCHEDULABLEWRAPPER('-GDPR-', ?, ?, ?, ?) | 139 |

#### 17.8.4.5 Internal SQL Statement

This SQL statement was executed from an internal database connection.

### 17.8.5 SQL Statement d2040795d0fa208871e56bd08995dfee

SELECT

ZZHDBSSA1.*

FROM

(WITH BASIS_INFO AS ( SELECT HOST, ONLY_POTENTIALLY_CRITICAL_RESULTS, SKIP_LESS_RELEVANT_CHECKS_IN_SYSTEMDB, SKIP_OVERLAPPING_CHECKS_IN_SYSTEMDB, MAX_VALUE_LENGTH, CHECK_ID, CHECK_GROUP, CHECK_ID_PRE

Statement Impact

| Indicator | Value |
| --- | --- |
| Contribution to Total CPU Load [%] | 0,53 |
| Maximal CPU Consumption per Hour [%] ( 27.04.2026 between 04:00 and 05:00 ) | 0,60 |
| Maximal Memory Consumption [%] ( 27.04.2026 -- 05:46:03 ) | 3,62 |

**Note:** The statement as identified by its statement hash can also be found in other sections of this report:

| Other Sections Dealing with this Statement |
| --- |
| SAP HANA SQL Statements in H4P -> Top Statement (Maximal Memory in Trace) |

#### 17.8.5.1 Statement History (Thread Sample 'Running')

The following graph shows the number of observed thread samples (in state "running") related to this SQL statement together with the contribution of those samples to all thread samples (in state "running") active in the system.
[IMAGE]

#### 17.8.5.2 Correlation with Index Server Resource Consumption

The distribution of thread samples with the status "Running" correlates strongly with the overall CPU or memory consumption of the system. Such a correlation indicates that this statement might be responsible for peaks in the memory or CPU consumption.

| Distiribution | Correlation Coefficient | Comment |
| --- | --- | --- |
| CPU consumption index server(s) - Threads (running) from this SQL statement | 0,70 | strong correlation |
| Memory consumption index server(s) - Threads (running) from this SQL Statement | 0,67 | strong correlation |

#### 17.8.5.3 Origin of SQL Statement

The following table shows details of the applications responsible for the statement. This information is based on the information provided by SAP HANA in the "application source" connected to the statement in the "thread samples" or the list of "prepared" or "active" statements, and is not necessarily complete.

| SID | APPLICATION_SOURCE | Transaction / Jobaname |
| --- | --- | --- |
| DSA | CL_SQL_STATEMENT==============CP:500 | /BDL/TASK_PROCESSOR |
| S4P | CL_SQL_STATEMENT==============CP:703 | /BDL/TASK_PROCESSOR |

# 18 SAP NetWeaver Gateway

| [IMAGE] | The gateway configuration and administration of your SAP S/4HANA system S4P have been analyzed and areas that require your attention have been highlighted. To ensure system stability, you should implement the recommendations in the following section. |
| --- | --- |

| Rating | Check |
| --- | --- |
| [GREEN] | MetaData Cache Activation |
| [GREEN] | Logging Configuration |
| [YELLOW] | Gateway Error Logs |
| [YELLOW] | Important Periodic Jobs |

## 18.1 Gateway Configuration

### 18.1.1 MetaData Cache Activation

| Cache | Activated |
| --- | --- |
| Metadata Cache | Yes |

The metadata cache is activated in your system as recommended.

### 18.1.2 Logging Configuration

| Logging Use Case | Log Level | Recommended Log Level |
| --- | --- | --- |
| Regular processing | Error, Security, Warning | Error, Security, Warning |

The gateway logging configuration is set correctly on your system.

## 18.2 Gateway Administration

### 18.2.1 Gateway Error Logs

Number Of Errors in last 7 Days

| Date | Number of Errors |
| --- | --- |
| 03.05.2026 | 2 |
| 01.05.2026 | 20 |
| 30.04.2026 | 22 |
| 29.04.2026 | 19 |
| 28.04.2026 | 15 |
| 27.04.2026 | 19 |

Error types by number of occurrences

| Error Message | Message ID | Number of Occurrences | Service Name | Date (e.g.) | Time (e.g.) |
| --- | --- | --- | --- | --- | --- |
| /IWFND/CM_CONSUMER | 101 | 78 | ESH_SEARCH_SRV | 29.04.2026 | 14:13:58 |
| /IWFND/MED | 170 | 14 |  | 27.04.2026 | 08:47:06 |
| /IWBEP/CM_V4_COS | 014 | 5 | UI_JOURNALENTRY_VERIFY | 03.05.2026 | 20:22:24 |

The tables above list the top gateway errors during the last 7 days.

**Recommendation:** 
 Monitor the error logs periodically for errors and take administrative action to resolve these errors.

Implementation: To search for errors, call transaction /IWFND/ERROR_LOG and select the desired timeframe and error type.

If you need further information on how to resolve specific errors, refer to [SAP Note 3013836](https://me.sap.com/notes/3013836) , which explains the most common Gateway errors. If the error cannot be resolved, open a customer message under the relevant component.

### 18.2.2 Important Periodic Jobs

The jobs based on the reports listed in the table below are important for the smooth operation of your system.

| Report Name | Scheduled Periodically? | Scheduled Frequency | Recommended Frequency | Rating | Further Information |
| --- | --- | --- | --- | --- | --- |
| /IWBEP/R_CLEAN_UP_QRL | X | Daily | Daily | [GREEN] | LINK |
| /IWBEP/SUTIL_CLEANUP | X | Daily | Daily | [GREEN] | LINK |
| /IWFND/R_METERING_AGGREGATE | X | Daily | Daily | [GREEN] | LINK |
| /IWFND/R_METERING_DELETE | X | Daily | Daily | [GREEN] | LINK |
| /IWFND/R_SM_CLEANUP | X | Daily | Daily | [GREEN] | LINK |
| /UI2/PAGE_CACHE_SYNCHRONIZE |  | - | Daily | [YELLOW] | LINK |
| /UI2/PERS_EXPIRED_DELETE | X | Monthly | Monthly | [GREEN] | LINK |
| /UI5/APP_INDEX_CALCULATE | X | 15 minutes | Daily* | [BLUE] | LINK |
| /UI5/UPD_ODATA_METADATA_CACHE | X | Hourly | 2 days* | [GREEN] | LINK |
| /UIF/CLEAN_LREP | X | Daily | Daily | [GREEN] | LINK |

*Schedule these jobs as indicated, or more often in periods of frequent imports, depending on your use case. Take observed job duration for your system into account when tuning the schedule.

For your S/4HANA release, a list of all jobs that are delivered as job definitions by the Technical Job Repository is provided in SAP Note [3389524](https://me.sap.com/notes/3389524) .

**Recommendation** : See the recommended schedule for the important periodic jobs listed in the table above. One or more periodic jobs important for the smooth operation of your system are not scheduled to run regularly as recommended.

## 18.3 Gateway Workload Statistics

### 18.3.1 Gateway Processing Performance

The following tables and diagrams show the load and performance of OData gateway calls for the previous week. These diagrams show the top 10 OData calls, sorted by the following criteria:

- Total Calls

- Total Call Time in Milliseconds

- Average Data Received in Bytes

Note: A few OData requests are filtered out here, such as the one for notifications in the SAP Fiori Launchpad. This is because they are constantly called and therefore generally outweigh all other requests.

The complete OData request statistics can be viewed and further analyzed by visiting the [SAP EarlyWatch Alert Workspace](https://me.sap.com/ewa/dashboard/uxODataRequestsDetail/S4P_0021220331_000000000800631194/202619) .
[IMAGE]
[IMAGE]
[IMAGE]

Top OData Calls by Total Calls

| Service | Entity set or Function | Operation | Total Calls |
| --- | --- | --- | --- |
| INTEROP | PersContainers |  | 428 |
| INTEROP | PersContainers() |  | 355 |
| ESH_SEARCH_SRV | ServerInfos |  | 116 |
| PAGE_BUILDER_PERS | PageSets() |  | 106 |
| ESH_SEARCH_SRV | PersonalizedSearchMainSwitches |  | 76 |
| ESH_SEARCH_SRV | Users() |  | 76 |
| ESH_SEARCH_SRV |  | $metadata | 38 |
| ESH_SEARCH_SRV | DataSources |  | 38 |
| PAGE_BUILDER_PERS | Pages()/allCatalogs |  | 26 |
| INTEROP |  |  | 18 |

Top OData Calls by Total Call Time[ms]

| Service | Entity set or Function | Operation | Total Call Time [ms] | Average Call Time[ms] |
| --- | --- | --- | --- | --- |
| PAGE_BUILDER_PERS | PageSets() |  | 20.776 | 196 |
| INTEROP | PersContainers |  | 20.116 | 47 |
| INTEROP | PersContainers() |  | 16.685 | 47 |
| ESH_SEARCH_SRV | DataSources |  | 13.224 | 348 |
| ESH_SEARCH_SRV | ServerInfos |  | 5.452 | 47 |
| ESH_SEARCH_SRV |  | $metadata | 3.762 | 99 |
| ESH_SEARCH_SRV | PersonalizedSearchMainSwitches |  | 3.116 | 41 |
| ESH_SEARCH_SRV | Users() |  | 2.964 | 39 |
| PAGE_BUILDER_PERS | Pages()/allCatalogs |  | 1.742 | 67 |
| PAGE_BUILDER_PERS | Chips() |  | 1.510 | 302 |

Top OData Calls by Average Data Received[bytes]

| Service | Entity set or Function | Operation | Average Data Received[bytes] |
| --- | --- | --- | --- |
| INTEROP | PersContainers |  | 5.448 |
| PAGE_BUILDER_PERS | PageSets() |  | 3.434 |
| PAGE_BUILDER_PERS | Chips() |  | 3.338 |
| ESH_SEARCH_SRV | DataSources |  | 3.314 |
| UI_JOURNALENTRY_VERIFY | JournalEntryWorkflow | $count | 3.297 |
| INTEROP | PersContainers() |  | 3.266 |
| SUI_FLP_APP_SUP_SRV |  | $metadata | 3.243 |
| ESH_SEARCH_SRV | PersonalizedSearchMainSwitches |  | 3.237 |
| C_BALANCECARRYFWDSTATUS_CDS | C_BalanceCarryFwdStatus | $count | 3.222 |
| ESH_SEARCH_SRV | ServerInfos |  | 3.209 |

# 19 UI Technologies Checks

| [IMAGE] | The UI technology configuration and administration of your SAP S/4HANA system S4P have been analyzed and areas that require your attention have been highlighted. To ensure system stability, you should implement the recommendations in the following section. |
| --- | --- |

## 19.1 Fiori Checks for S4P

| Rating | Check |
| --- | --- |
| [GREEN] | SAP Fiori Cache Buster Activation |
| [GREEN] | HTTP/2 Support |
| [GREEN] | SAP Fiori Launchpad Performance - Home Page Mode |
| [YELLOW] | SAP Fiori Launchpad - Spaces and Pages adoption |
| [GREEN] | Activated but unused ICF services in UI5 apps |

The SAP Fiori configuration and administration of your SAP S/4HANA system S4P have been analyzed and problems that require your attention have been found. To ensure system stability, you should take corrective action as soon as possible.

### 19.1.1 SAP Fiori Cache Buster Activation

You have activated the cache buster mechanism for system S4P because the ICF service /sap/bc/ui2/flp is activated in SICF.

Please note that to use the cache buster mechanism, you need to call the SAP Fiori launchpad with one of the following URLs:

[https://<server>:<port>/sap/bc/ui2/flp/](https://%3cserver%3e:%3cport%3e/sap/bc/ui2/flp/)

[https://<server>:<port>/sap/bc/ui2/flp/index.html](https://%3cserver%3e:%3cport%3e/sap/bc/ui2/flp/index.html)

[https://<server>:<port>/sap/bc/ui2/flp/FioriLaunchpad.html](https://%3cserver%3e:%3cport%3e/sap/bc/ui2/flp/FioriLaunchpad.html)

You can also maintain a custom URL via an SICF external alias as described here: [Customize the Launchpad URL](http://help.sap.com/saphelp_uiaddon10/helpdata/en/c9/44dc71fc7d49b4a1239a4231563c80/content.htm)

Background:

Web browsers store static resources like JavaScript files, stylesheets, and images in the browser cache. When these resources are changed on the server in a software upgrade, you want the browser to load the new resources from the server rather than from the cache, without having to manually clear the browser cache.

Cache buster techniques cause Web browsers to load content from the server rather than from the browser cache when new resources are available on the server.

You can find the latest information about the cache buster for SAP Fiori components in [2043432](https://launchpad.support.sap.com/#/notes/0002043432) .

### 19.1.2 HTTP/2 Support

HTTP/2 support is currently active as recommended.

The HTTP protocol is one of the most frequently used protocols on the Internet. However, HTTP/1.0 and HTTP/1.1 have some disadvantages for modern applications, in particular with respect to performance in wide-area networks. To improve these problems, their successor RFC 7540 HTTP/2 has been implemented.

For more information on HTTP/2 Support, see [here](https://help.sap.com/viewer/683d6a1797a34730a6e005d1e8de6f22/1809.000/en-US/c7b46000a76445f489e86f4c5814c7e8.html)

| Host | Parameter Name | Current Value | Rating |
| --- | --- | --- | --- |
| bsws4pap01 | icm/HTTP/support_http2 | TRUE | [GREEN] |

### 19.1.3 SAP Fiori User Count

There were **25** different users on the system using SAP Fiori in the analyzed week.

The calculation is based on the number of different users who loaded the SAP Fiori launchpad at least once in the report timeframe. Please note that the total number also includes users who opened SAP Fiori apps via a direct URL, since the Launchpad is loaded in the background.

### 19.1.4 SAP Fiori Launchpad Performance - Home Page Mode

| FLP Mode | Avg. Request Time [s] | Avg. Data Sent [KB] | Rating |
| --- | --- | --- | --- |
| Home Page / Groups | 0,20 | 12,01 | [GREEN] |

The performance of the SAP Fiori launchpad is good. When using the SAP Fiori launchpad in the Home Page/Groups mode, its average request time should not exceed 5 seconds.

### 19.1.5 SAP Fiori Launchpad - Spaces and Pages adoption

| Launchpad Parameters | Current Value | Recommended Value | Rating |
| --- | --- | --- | --- |
| SPACES / SPACES_ENABLE_USER |  | true | [YELLOW] |

From SAP S/4HANA 2021, groups mode is officially deprecated, meaning that while groups currently still exist, they will be removed in a future release. The earlier you start making the shift to spaces and pages the better, given that most customers will need to consider how they want to migrate each business role.

Therefore, we recommend that one of the two parameters that enable Spaces and Pages are activated.

We found that the Spaces and Pages option was not enabled on your system.

The SPACES parameter enables the use of Spaces and Pages for your users.

The SPACES_ENABLE_USER allows the user to choose if they want to switch between Spaces and Groups.

CAUTION: If you enable SPACES and there are no spaces added to the user roles, your end users will just see a blank launchpad. If you only have defined a few pages so far, you should not yet enable the spaces mode. You can set the parameter SPACE_ENABLE_USER to true and ask users with roles that have pages available to switch to the spaces mode themselves. They can then start working with pages.

See more information on these settings in the What’s New Viewer for ABAP Platform the entries: [SAP Fiori Launchpad: Home Page Deprecated (CA-FE-FLP-COR)](https://help.sap.com/doc/34796706f38646f68d51a0fa0d4636e4/100/en-US/cf27dceb447b43099026b46b69b1b16f.html) and [SAP Fiori Launchpad Home Page Deprecated (CA-FE-FLP-UI)](https://help.sap.com/doc/34796706f38646f68d51a0fa0d4636e4/100/en-US/02aa13a2ac514762976b6971d06d5ff8.html) .

For more information, see [Setting Parameters in SAP Fiori Customizing](https://help.sap.com/docs/ABAP_PLATFORM_2021/a7b390faab1140c087b8926571e942b7/eae3cc31b1d34d139d153067fcecd975.html??locale=en-USstate=PRODUCTION&version=202110.001) .

### 19.1.6 Activated but unused ICF services in UI5 apps

| Rating | Unused ICF Services | Percentage of usable ICF Services |
| --- | --- | --- |
| [GREEN] | 1 | 99.3% |

SAP detected **1** activated ICF services in your system that cannot be used since the corresponding SAPUI5 apps have not been configured correctly.

Active ICF services represent a security risk as they can be accessed directly from the Internet via the HTTP protocol. A warning is triggered if less than 95% of the activated ICF services are usable.

**Recommendation:** ICF services for SAPUI5 apps that are not used should be deactivated. The identification of such ICF services is described in SAP KBA [3261151](https://launchpad.support.sap.com/#/notes/0003261151) .

# 20 Cross Application Business Process Analysis

This section provides insights into cross-application data in the areas of jobs, interfaces, and data consistency.

The data is collected in the cross-application business process analysis (BPA) and the data collection findings are displayed in the EWA if it is configured to include BPA data. Further details can be found in the cross-application BPA.

With Business Process Monitoring in SAP Solution Manager, you can continuously analyze the key figures displayed below in addition to approximately 800 out-of-the-box key figures.

**Disclaimer**

Bear in mind that all assumptions and ratings in this presentation are based on our general experience with other customers and that the findings are not necessarily business-critical in your particular case.

| Rating | Area | Key Figure | Finding |
| --- | --- | --- | --- |
| [GREEN] | Jobs | Canceled background jobs | 5 of jobs have been canceled on the peak day of the analyzed week. |
| [GRAY] | Interfaces | IDoc throughput (Inbound) | 1216 of all inbound IDocs have been successfully processed in the analyzed week. |
| [YELLOW] | Interfaces | Erroneous IDocs (Inbound) | 3 erroneous inbound IDocs were identified for the analyzed week. |
| [GREEN] | Interfaces | IDoc backlog (Inbound) | 0 backlog inbound IDocs have been identified in the analyzed week. |
| [GRAY] | Interfaces | IDoc throughput (Outbound) | 3323 of all outbound IDocs have been successfully processed in the analyzed week. |
| [GREEN] | Interfaces | Erroneous IDocs (Outbound) | 0 erroneous outbound IDocs were identified for the analyzed week. |
| [GREEN] | Interfaces | IDoc backlog (Outbound) | 0 backlog outbound IDocs have been identified in the analyzed week. |
| [GREEN] | Interfaces | Erroneous qRFC (Inbound) | 0 qRFC inbound errors occurred during the analyzed week. |
| [GREEN] | Interfaces | Backlog qRFC (Inbound) | 0 inbound qRFC were in backlog in the analyzed week. |
| [GREEN] | Interfaces | Erroneous qRFC (Outbound) | 0 qRFC outbound errors occurred during the analyzed week. |
| [GREEN] | Interfaces | Backlog qRFC (Outbound) | 0 outbound qRFC were in backlog in the analyzed week. |
| [GREEN] | Interfaces | Erroneous tRFC (Outbound) | 1 tRFC errors occurred during the analyzed week. |
| [GREEN] | Interfaces | Backlog tRFC (Outbound) | 1 tRFC were in backlog in the analyzed week. |
| [GREEN] | Interfaces | Erroneous bgRFC (Inbound) | 0 bgRFC inbound errors occurred during the analyzed week. |
| [GREEN] | Interfaces | Backlog bgRFC (Inbound) | 0 inbound bgRFC were in backlog in the analyzed week. |
| [GREEN] | Interfaces | Erroneous bgRFC (Outbound) | 0 bgRFC outbound errors occurred during the analyzed week. |
| [GREEN] | Interfaces | Backlog bgRFC (Outbound) | 0 outbound bgRFC were in backlog in the analyzed week. |
| [GREEN] | Interfaces | Workflows in error | 0 errors in workflows have been identified in the analyzed week. |
| [GRAY] | Interfaces | Throughput batch input sessions | 31 throughput batch input sessions have been identified in the analyzed week. |
| [RED] | Interfaces | Batch input sessions with errors | 911 erroneous batch input sessions have been identified in the analyzed week. |
| [RED] | Interfaces | Batch input sessions in backlog | 13667 batch input sessions in backlog have been identified in the analyzed week. |
| [GREEN] | Interfaces | Erroneous PI messages | 0 erroneous PI messages have been identified in the analyzed week. |
| [GREEN] | Interfaces | PI messages in backlog | 0 PI messages in backlog have been identified in the analyzed week. |
| [GREEN] | Interfaces | Canceled PI messages messages | 0 canceled PI messages have been identified in the analyzed week. |
| [GREEN] | Data Consistency | Errors in update task | 0 errors in update tasks occurred during the analyzed week. |
| [YELLOW] | Data Consistency | Consistency check scheduling verification | Not all variants for all recommended Data Consistency reports have been executed |

The displayed measurements relate to the findings in the cross-application business process analysis (BPA). For more information, see the results of the BPA. For more information about the BPA, check the following link:

[SAP CQC BPI.pdf](https://support.sap.com/content/dam/support/en_us/library/ssp/offerings-and-programs/sap-enterprise-support/enterprise-support-academy/continuous-quality-check-improvement-services/SAP%20CQC%20BPI.pdf)

If you have an **SAP Enterprise Support** contract, SAP Active Global Support will provide you with the following offerings to provide job monitoring, interface monitoring, and data consistency monitoring:

- Expert Guided Implementation Data Consistency Management

- CQC Interface Management

- CQC Data Consistency Management

If you have an **SAP Max Attention Contract** , contact your Technical Quality Manager (TQM) for information about how SAP Active Global Support can help you to implement job, interface, and consistency monitoring.

# 21 Trend Analysis

This section contains the trend analysis for key performance indicators (KPIs).

Diagrams are built weekly once the EarlyWatch Alert service is activated.

In this section, a "week" is from Monday to Sunday. The date displayed is the Sunday of the week.

## 21.1 System Activity

The following diagrams show the system activity over time.

The "Transaction Activity" diagram below depicts transaction activity in the system over time.

**- Total Activity:** Transaction steps performed each week (in thousands) 
 - Dialog Activity: Transaction steps performed in dialog task each week (in thousands) 
 - Peak Activity: Transaction steps (in thousands) during the peak hour; this peak hour is calculated as the hour with the maximum dialog activity in the ST03 time profile divided by 5 working days per week.

(Peak Activity is absent if "Activity Data" is taken from ST03 data directly).
[IMAGE]

The "User Activity" diagram below shows the user activity on the system over time.

**- Total Users:** Total users that logged on in one week.

- Active Users: Users who performed more than 400 transaction steps in one week.
[IMAGE]

## 21.2 Response Times

The following diagrams show how the response time varies over time.

The "System Performance" diagram below shows the average response time in dialog tasks for the previous week.
[IMAGE]

**The** "Database Performance" diagram below shows the average DB response time in dialog tasks.
[IMAGE]

**The** "Top 5 transactions" diagram below shows the average response time in dialog tasks for the top 5 transactions.
[IMAGE]

**The** "Transaction Code" table below shows the load percentage caused by the top 5 transactions.

| No | Transaction Code | Load (%) |
| --- | --- | --- |
| Transaction 1 | ZAT6A | 9,6 |
| Transaction 2 | ZST11 | 8,3 |
| Transaction 3 | ZU22_1 | 8,2 |
| Transaction 4 | SESSION_MANAGER | 4,9 |
| Transaction 5 | ZTCT_SCA_RF_PICK_AU | 4,9 |

[IMAGE]
[IMAGE]
[IMAGE]

## 21.3 System Operation

The following diagram or table shows important KPIs for system operation.
[IMAGE]

## 21.4 Hardware Capacity

The following diagram or table shows the maximum CPU load from the database server and the highest CPU load among all application servers.
[IMAGE]

**Report** time frame: Service data was collected starting at 04.05.2026 04:41:12. This took 45 minutes.

You can see sample SAP EarlyWatch Alert reports on SAP Support Portal at [SAP EarlyWatch Alert](https://support.sap.com/ewa) -> Sample Reports.

For general information about SAP EarlyWatch Alert, see [SAP Note 1257308](https://launchpad.support.sap.com/#/notes/1257308) .

About System And Solution Manager

| System No. Of Target System | 800631194 |
| --- | --- |
| Solution Manager System | DSA |
| Solution Manager Version | SOLUTION MANAGER 7.2 |
| Service Tool | 720 SP19 |
| Service Content Update On | 23.04.2026 |
