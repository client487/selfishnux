<h1 align="center">
    selfishnux
    <br>
</h1>

<p align="center">
    <strong>A short reimplementation of selfishnet in python</strong>
</p>

---
---

## Requirements
Windows :
``` bash
pip install -r requirements.txt
```
Linux :
``` bash
sudo pip install -r requirements.txt --break-system-packages
```
And finaly run `main.py` :

Windows :
``` bash
python main.py
```
Linux :
``` bash
sudo python main.py
```

## Config

`config.json` example :
``` json
{
    "global" : {
        "gateway_ip" : "192.168.1.1",
        "target_ip" : "192.168.1.2",
        "interface" : "wlp2s0"
    },
    "infos" : {
        "version" : 0.1
    }
}
```