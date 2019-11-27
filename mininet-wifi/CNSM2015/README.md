### Requirements
- Mininet-WiFi
- Floodlight 

### Reproducibility Steps

**Terminal 1**
```
~/floodlight$ sudo java -jar target/floodlight.jar
```

**Terminal 2**
```
sudo python ncasting.py
mininet-wifi> sh python ncasting-controller.py
```

### bibtex
@inproceedings{fontes2015mininet,  
  title={Mininet-WiFi: Emulating software-defined wireless networks},  
  author={Fontes, Ramon R and Afzal, Samira and Brito, Samuel HB and Santos, Mateus AS and Rothenberg, Christian Esteve},  
  booktitle={Network and Service Management (CNSM), 2015 11th International Conference on},  
  pages={384--389},  
  year={2015},  
  organization={IEEE}  
}
