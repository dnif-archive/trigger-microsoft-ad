# Microsoft Active Directory 

### Overview
Active Directory (Microsoft-AD) is a Microsoft product that consists of several services that run on Windows Server to manage permissions and access to networked resources. Active Directory stores data as objects. 

Microsoft Active Directory helps you organize your company’s users, computer and more. Your IT admin uses Microsoft-AD to organize your company’s complete hierarchy from which computers belong on which network, to what your profile picture looks like or which users have access to the storage room.
 
### PRE-REQUISITES to use Microsoft-AD and DNIF  
Install ldap3 python library for this Integration  
` pip install ldap3 `

Outbound access required for github to clone the plugin

| Protocol   | Source IP  | Source Port  | DNIF FW	| Microsoft-AD FW | Destination Domain | Destination Port  |  
|:------------- |:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|  
| TCP | DS,CR,A10 | Any | Egress	| Ingress | github.com | 443 |
| TCP | DS,CR,A10 | Any | Egress	| Ingress | Microsoft-AD (Host/Domain) | 636 |

#### `*`The above rule assumes both request and response is enabled

#### Note

In all the functions explained below, the examples use an event store named **adtest**.  
**This event store does not exist in DNIF by default**. However, it can be created/imported.
 
 
## microsoft-ad trigger plugin functions
Details of the function that can be used with the microsoft-ad trigger is given in this section.
- [add_to_group](#add_to_group)
- [remove_from_group](#remove_from_group)
- [enable_user](#enable_user)
- [disable_user](#disable_user)

### add_to_group 
This function allows for adding a user of an observerd event to a specific group.
### Input  
- User Common Name Details 
- Group Common Name Details 
   
### Example
```
_fetch * from adtest limit 1
>>_field $GroupID string "CN=TestDomain,OU=DomainGroup,DC=DNIFAD,DC=org"
>>_trigger api microsoft-ad add_to_group $AccountID , $GroupID
```
### Output  
![ms_add_grp](https://user-images.githubusercontent.com/37173181/49505156-2a6cda00-f8a1-11e8-9a28-b59736e1a6c3.jpg)


The trigger call returns output in the following structure for available data

  | Fields        | Description  |
|:------------- |:-------------|
| $ADGrpStatus  | Message for successful/unsuccessful addition of user to group |


### remove_from_group 
This function allows for removing an user from a specific group.
### Input  
- User Common Name Details 
- Group Common Name Details 
   
### Example
```
_fetch * from adtest limit 1
>>_field $GroupID string "CN=TestDomain,OU=DomainGroup,DC=DNIFAD,DC=org"
>>_trigger api microsoft-ad remove_from_group $AccountID , $GroupID
```
### Output  
![ms_remove_from_grp](https://user-images.githubusercontent.com/37173181/49505227-4bcdc600-f8a1-11e8-863c-1a2056a63619.jpg)

The trigger call returns output in the following structure for available data

  | Fields        | Description  |
|:------------- |:-------------|
| $ADGrpStatus     | Message for successful/unsuccessful removal of user from group |

### enable_user 
This function allows for activating a previously disabled user account .

### Input  
- User Common Name Details  
   
### Example
```
_fetch * from adtest limit 1
>>_trigger api microsoft-ad enable_user $AccountID 
```
### Output  
![ms_enableusr](https://user-images.githubusercontent.com/37173181/49505251-5be5a580-f8a1-11e8-8bb1-0998da41aa5a.jpg)

The trigger call returns output in the following structure for available data

  | Fields        | Description  |
|:------------- |:-------------|
| $ADUserStatus     | Message for successful/unsuccessful account enabling |


### disable_user 
This function allows for de-activating an user account 

### Input  
- User Common Name Details  
   
### Example
```
_fetch * from adtest limit 1
>>_trigger api microsoft-ad disable_user $AccountID 
```
### Output  
![ms_disableuser](https://user-images.githubusercontent.com/37173181/49505281-699b2b00-f8a1-11e8-8f59-8b44f95f4372.jpg)

The trigger call returns output in the following structure for available data

  | Fields        | Description  |
|:------------- |:-------------|
| $ADUserStatus     | Message for successful/unsuccessful account disabling |


### Using the microsoft-ad API and DNIF  
The microsoft-ad API is found on github at 

  https://github.com/dnif/trigger-microsoft-ad

The following process has to be repeated on all of the following components
DS,CR,A10

### Getting started with microsoft-ad API and DNIF

1. ####    Login to your Data Store, Correlator, and A10 containers.  
   [ACCESS DNIF CONTAINER VIA SSH](https://dnif.it/docs/guides/tutorials/access-dnif-container-via-ssh.html)
2. ####    Move to the `‘/dnif/<Deployment-key>/trigger_plugins’` folder path.
```
$cd /dnif/CnxxxxxxxxxxxxV8/trigger_plugins/
```
3. ####   Clone using the following command  
```  
git clone https://github.com/dnif/trigger-microsoft-ad.git microsoft-ad
```
4. ####   Move to the `‘/dnif/<Deployment-key>/trigger_plugins/microsoft-ad/’` folder path and open dnifconfig.yml configuration file    
   Replace the tags: <Add_your_AD_*> with your ad credentials
```
trigger_plugin:
  AD_SERVER: <Add_your_AD_Server/Host>
  AD_DOMAIN: <Add_your_AD_Domain_Name>
  AD_USER: <Add_your_AD_User_Name>
  AD_USER_PASS: <Add_your_AD_User_Password>
```
