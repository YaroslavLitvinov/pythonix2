This project was derived from free version of Pythonix2 Mikrotik billing. Original version of pythonix2 is freely available in internet as vbox image: 
[http://asp24.com.ua/asp24/billing-dlja-mikrotik-routerboard/].
This is a webservice which provide billing and allows to manage Mikrotik users. It also give for end users ability to change their tariff in web ui.
The updated web service engine:
* Has no limits for users count, which are settled on many Mikrotik devices; 
* tested with 4.11 - 5.25 versions of Mikrotik.
* synchronizes settings between Mikrotik and Pythonix at the action moment in web ui;
* supports two auth methods for end Mikrotik users: ARP, and VPN. VPN mode is optional and ARP is required;
* expects that Miktorik itself will shutdown internet for users by using script provided below, previously added from web ui ;
* web service db schema provided in pythonix-db.backup and has a little differences comparing to unmodified pythonix version.
* Can do automatic backup of pythonix db by saving it to the github repository "turbo-backup"  :)


The both original and derived version of web interface are using russian language, so probably it will be useless for english speakers.

- Схема работы с учетными записями клиентов:
Когда клиент добавляется, то :
в arp заносится запись, тем самым мы разрешаем доступ к локальной сети, при удалении клиента запись из arp удаляется;
в dhcp-leases добавляется локальный ip адрес;
в queue добавляется очередь с указанием локального ip адреса, скорость будет резаться для интернета и для локального трафика сети;
в ppp secrets добавляется login & password с указанием vpn ip адреса;
в ip firewall address-list добавляется vpn ip адрес и локальный ip адрес и в комментарии к нему последний день интернета. Только адресам в этом списке разрешен доступ в интернет (во время переходного периода будет разрешен доступ всем компам сети через очередь, как сейчас);
Когда клиент удаляется, то :
удаляются записи из arp, dhcp-leases, ip firewall address-list (удаляется и локальный и vpn адрес), queue, ppp secrets;
Когда происходит отключение клиента, то :
arp остается без изменений, тем самым оставляет возможность клиенту подключиться и оплатить услуги в будущем;
в ip firewall address-list деактивируется адрес, так отключается интернет;
Когда клиент включается, то :
arp, dhcp-leases остаются без изменений.
в ip firewall address-list активируется адрес, и указывается в комментарии дата последнего проплаченного дня, так включается интернет;

cron settings for nightly backups:
crontab -e -u tram
58 23 * * * cd ~/git/turbo-backup/ && ./backup_run.sh pythonix2 > /tmp/bckp1 && logger -f /tmp/bckp1

Mikrotik settings:
```
/system scheduler
add comment="" disabled=no interval=1d name="BILLING MIDNIGTH EVENT" \
    on-event=BILLING policy=read,write,policy,test,sniff,sensitive \
    start-date=apr/08/2015 start-time=23:59:00
/system script
add name=BILLING policy=\
    ftp,reboot,read,write,policy,test,winbox,sniff,sensitive source=":local cd\
    ate [/system clock get date]\r\
    \n:local runinfoaddress (\"Locate ADDRESSES in address-list with exact day\
    \_in comment as TODAY \". \$cdate)\r\
    \n/log info message=\$runinfoaddress\r\
    \n\r\
    \n#For each address in the address-list\r\
    \n:foreach i in=[/ip firewall address-list find comment =\$cdate ] do={\r\
    \n    :local addrdisabled [/ip firewall address-list get \$i disabled]\r\
    \n    :if ( addrdisabled = false ) do={ \r\
    \n        :local ipaddr [/ip firewall address-list get \$i address]\r\
    \n        /ip firewall address-list set \$i disabled=yes\r\
    \n        :local addrnewcomment ( \$cdate .\" disabled: Date matched\")\r\
    \n        /ip firewall address-list set \$i comment= \$addrnewcomment\r\
    \n        :local printing (\"!!!!!!!!!!!!!! '\". \$ipaddr.\"' Account stop\
    ed, Address disabled!\")\r\
    \n        /log info message=\$printing\r\
    \n    } \r\
    \n}\r\
    \n"
    ```

/ip firewall filter add action=accept chain=input comment=api disabled=no dst-port=8728 protocol=tcp
/ip service set api address=0.0.0.0/0 disabled=no port=8728

/queue type add kind=pcq name="UploadTarif0" pcq-rate=4M 
add kind=pcq name="Download Tarif0" pcq-rate=4M
add kind=pcq name="Upload Tarif1" pcq-rate=10M
add kind=pcq name="Download Tarif1" pcq-rate=30M
add kind=pcq name="Upload Tarif2" pcq-rate=50M
add kind=pcq name="Download Tarif2" pcq-rate=50M
add kind=pcq name="Download Tarif3" pcq-rate=100M 
add kind=pcq name="Upload Tarif3" pcq-rate=40M
```

Скрипт BILLING запускается каждые сутки для отключения пользователей точно по дате. 
Проблема: Если микротик будет недоступен в момент запуска скрипта т.е. ночью в 11:59, то пользователь не будет отключен вообще.

