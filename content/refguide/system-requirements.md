---
title: "System Requirements"
category: "General Info"
menu_order: 10
description: "Presents the system requirements for using the Mendix Platform."
tags: ["studio pro"]
#If moving or renaming this doc file, implement a temporary redirect and let the respective team know they should update the URL in the product. See Mapping to Products for more details.
---

## 1 Introduction

This document presents the system requirements for the various parts of the Mendix Platform.

## 2 Mendix Studio Pro {#sp}

Mendix **Studio Pro** version 9 is supported on 64-bit versions of Windows 10 release 1809 and above. Studio Pro does not run on Windows emulators on Apple Silicon Macs, such as the M1, or on any other ARM-based machines.

The following frameworks are automatically installed (if necessary):

* Microsoft .NET Framework 4.7.2 and all applicable Windows security patches
* Microsoft Visual C++ 2010 SP1 Redistributable Package
* Microsoft Visual C++ 2015 Redistributable Package
* AdoptOpenJDK 11 or Oracle JDK 11 (the former is installed automatically) if you do not have any JDK 11 installed) 

{{% alert type="info" %}}
You can choose which JDK is used for building and running locally via the **Edit** > **Preferences** menu item in Studio Pro.
{{% /alert %}}

{{% alert type="warning" %}}
Please note the limitation that the database viewer built into Studio Pro (as described in **How to Share the Development Database**) does not work with JDK 11.06 or 11.07.
{{% /alert %}}

### 2.1 Firewall Settings

Studio Pro needs access to the following URLs in order to work. If your firewall is currently blocking these, you will need to whitelist them.

* `*.mendix.com`
* `*.mendixcloud.com`
* `*.teamserver.sprintr.com`

### 2.2 TortoiseSVN

If you want to use TortoiseSVN in combination with Studio Pro, download the latest version from the [TortoiseSVN](https://tortoisesvn.net/) website.

{{% alert type="warning" %}}
Mendix Studio Pro uses the Subversion 1.9 working copy. Previous versions of the Mendix Desktop Modeler used a Subversion 1.7 working copy. These working copy versions **are not compatible**.<br />
<br />
Always use the version of TortoiseSVN which matches your app model. If you open a local model from Mendix version 7.x or 6.x with the latest version of TortoiseSVN **you will no longer be able to open it in Mendix**.
{{% /alert %}}

### 2.3 File Locations

For active development and running your application locally, your app folder should be on local drive (such as C:) or on a network folder that has been mapped to a **Windows drive letter**.

### 2.4 Supported Git Service Providers {#supported-providers}

#### 2.4.1 Azure Repos and Azure DevOps Server 

We support both Microsoft’s **Azure Repos** hosted Git service, and Azure DevOps Server (former Team Foundation Server) which is an on-premises solution for hosting your Git repos on private infrastructure.

To get a PAT for your user account, see the **Use personal access tokens** instructions in the Microsoft documentation.

You need `Code (full)` permission for your token.

##### 2.4.2 GitHub 

We support GitHub’s hosting solutions, including the free GitHub.com cloud-hosted service and GitHub Enterprise, both hosted (Enterprise Cloud) and on-premises (Enterprise Server).

To get a PAT for your user account, see the **Creating a personal access token** instructions in the GitHub documentation. 

You need `repo` permissions for your token.

##### 2.4.3 GitLab 

We support all tiers of GitLab’s service, including GitLab.com, GitLab Community Edition, and GitLab Enterprise Edition.

To get a PAT for your user account , see the **Personal access tokens** instructions in the GitLab documentation. 

You need `write_repository` permission for the token.

##### 2.4.4 BitBucket 

We support all tiers of Atlassian’s BitBucket service, including BitBucket.org, BitBucket Server, and BitBucket Data Center on-premises solutions.

On BitBucket.org, the Personal Access Tokens are called App Passwords.

To setup an App Password for your BitBucket.org account, see the **App passwords** instructions.

BitBucket Server and BitBucket Data Center, on the other hand, still use the term Personal Access Tokens. To set up a personal access token, see **Personal access tokens** instructions.

In both cases you need `repository write` permission.

##### 2.4.5 AWS CodeCommit Limitation

We have a compatibility limitation with AWS CodeCommit in Git Technology Preview for Studio Pro.

### 2.5 Graphics Card

If you are using the Intel® UHD Graphics 630 graphics processor, please ensure that you are using **driver version 27.20.100.9664**+UHD+Graphics+630) or above.

## 3 Team Server {#ts}

The **Team Server** is implemented using Subversion, and Studio Pro uses the HTTPS protocol to communicate with that server. To access the Team Server from within Studio Pro, the network at your location needs the following settings:

* The HTTPS port (TCP 443) needs to be open
* The HTTP port (TCP 80) needs to be open
* WebDAV (verbs within the HTTP protocol) needs to be enabled on the proxy server (if any)

## 4 Mendix Studio

**Mendix Studio** is optimized for use with Google Chrome. While Chrome is the officially supported browser, you can also use Mendix Studio with other popular browsers like Mozilla Firefox, Apple Safari, and Microsoft Edge. 

{{% alert type="info" %}}
The browser you use needs to have JavaScript turned on.
{{% /alert %}}

## 5 Cloud Foundry

The **Mendix Cloud Foundry buildpack** supports Cloud Foundry versions v9 and above. 

## 6 Docker

The **Mendix Docker buildpack** supports Docker version 18.09.0 and above. 

### 6.1 Kubernetes

The Mendix Docker buildpack supports the following Kubernetes versions: 

* Kubernetes version v1.12 and above
* Red Hat OpenShift v3.11 and v4.2 and above

## 7 Server

### 7.1 Operating System

* Microsoft Windows Server 2008 SP2 and above
* Debian 8 (Jessie) and above
* Red Hat Enterprise Linux 6, Red Hat Enterprise Linux 7
* CentOS 6, CentOS 7

### 7.2 Web Server

* Microsoft Internet Information Services 7 and above
* Nginx (tested with versions included in Debian Jessie and Debian Jessie Backports)
* Apache

### 7.3 Java {#java}

When running Mendix on a server, you will need Java Runtime Environment (JRE) 11. To download an OpenJDK distribution from AdoptOpenJDK, see **AdoptOpenJDK Installation**. To download a commercial Oracle distribution, see **Java SE Downloads**.

{{% alert type="info" %}}
There is an issue since Java 7 that causes timeouts when using web services with a certain amount of data. You can circumvent this issue by adding the VM params `-Djava.net.preferIPv4Stack=true`. Mendix Studio Pro will do this for you, but if you are running Mendix on premises on a Windows server, you will need to do this yourself. For more information about this issue, see **HotSpot (64bit server) hangs on socket read (JVM 1.7 bug?) - updated** and **Possible Bug in Java 7**.
{{% /alert %}}

## 8 Databases {#databases}

Mendix tries to support the most recent and patched database server versions from database vendors. We aim to add support for a new vendor version two minor Mendix versions after the vendor has released it. Dropping support for a database will be announced in the release notes at the date the vendor drops support. We will drop support two minor Mendix versions later.

Current support:

* **IBM DB2** 11.1 and 11.5 for Linux, Unix, and Windows
* **MariaDB** 10.2, 10.3, 10.4, 10.5
* **Microsoft SQL Server** 2017, 2019
* **Azure SQL** v12 compatibility mode 140 or higher
* **MySQL** 8.0
* **Oracle Database** 19
* PostgreSQL 9.6, 10, 11, 12, 13
* **SAP HANA** 2.00.040.00.1545918182

{{% alert type="warning" %}}
Each app must have its own database. Mendix apps cannot share data by sharing the same database.

If you want two apps to share the same database, then you need to share the data from one app to the other using APIs. In Mendix these are supported by **Data Hub** or the REST and OData services described in the **integration** section of the *Studio Pro Guide*. This is referred to as a *microservices* architecture.

For more information on why data cannot be shared between apps see **Data Storage**. Use the **Database Replication** module if you need to copy the data from one app to another.
{{% /alert %}}

## 9 File Storage {#file-storage}

### 9.1 Storage Services for Containers

For container-based deployments using Docker, Kubernetes, or Cloud Foundry, the following storage services are supported:

* AWS S3
* Azure Blob Storage
* IBM Cloud Object Storage
* SAP AWS S3 Object Storage
* SAP Azure Blob Storage

For container-mounted storage in Kubernetes, provided by an external storage class, see also **Run Mendix on Kubernetes**.

###  9.2 Storage Types for Servers

For server-based installations, the following storage types mounted by the OS are supported:

* NAS 
* SAN 
* GFS
* Local Storage 

## 10 Browsers {#browsers}

* Google Chrome (latest stable desktop and Android versions)
* Mozilla Firefox (latest stable desktop version)
* Apple Safari (latest stable desktop version and latest version for each [supported iOS](#mobileos) version)
* Microsoft Edge (latest stable desktop version)

{{% alert type="warning" %}}
Internet Explorer is no longer supported in Studio Pro 9. As the market is moving away from Internet Explorer and Mendix continues to align with the best practices of the modern web ecosystem, we have dropped support for Internet Explorer 11. This allows us to keep in line with user expectations. Removing support has already improved app loading times and performance, and it will enable us to continue making improvements and innovating using modern web features.<br />
<br />
As of Studio Pro 9, app end-users still using IE will be shown an **Unsupported Browser** message stating that upgrading to a modern browser is required. You can **customize this message** to meet your needs.<br />
<br />
If you still need to support IE11, note that Studio Pro **8** and **7** will continue supporting IE11. Mendix recommends using Studio Pro 8 or 7 until your app end-users have upgraded their browsers.
{{% /alert %}}

## 11 Mobile Operating Systems {#mobileos}

For Mendix native apps, hybrid apps, and the Mendix Mobile app the following operating systems are supported:

* Latest two major versions of iOS
* Android 5.0 and above

### 11.1 Hybrid Apps Preview

Using a hybrid preview feature is not the same as testing an app on a phone or simulator. A hybrid preview only shows a resized view of an app to give an impression of what that app might look like on a mobile device. Some hybrid app functionality will not be supported in this browser view. Full tests always need to be done on a device or emulator. Offline apps can only be previewed in Google Chrome.

Hybrid apps cannot be tested in Android Emulator, only on a real device.

## 12 MxBuild {#mxbuild}

MxBuild is a Windows and Linux command-line tool that can be used to build a Mendix Deployment Package. For more information, see **MxBuild**.

* Mono v5.20.x or .NET v4.7.2
* JDK 11

## 13 mx Command-Line Tool {#mxtool}

The **mx** command-line tool is a Windows and Linux command-line tool that can be used to do useful things with your Mendix app. For more information, see **mx Command-Line Tool**.

* Mono v5.20.x or .NET v4.7.2
