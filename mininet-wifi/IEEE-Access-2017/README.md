### Requirements
- Mininet-WiFi
- VLC

### Reprocubibility steps
- ~/mininet-wifi$ git clone https://github.com/ramonfontes/reproducible-research
- ~/mininet-wifi$ sudo rm -r /usr/local/lib/python2.7/dist-packages/mininet*
- ~/mininet-wifi$ git reset --hard b43af65
- ~/mininet-wifi$ sudo make install
- ~/mininet-wifi$ cd reproducible-research/mininet-wifi/IEEE-Access-2017
- ~/mininet-wifi/reproducible-research/mininet-wifi/IEEE-Access-2017$ sudo python vanet.py

### Bibtex:  
@article{DosReisFontes2017,  
  doi = {10.1109/access.2017.2671030},  
  url = {https://doi.org/10.1109%2Faccess.2017.2671030},  
  year  = {2017},  
  publisher = {Institute of Electrical and Electronics Engineers ({IEEE})},  
  volume = {5},  
  pages = {3069--3076},  
  author = {Ramon Dos Reis Fontes and Claudia Campolo and Christian Esteve Rothenberg and Antonella Molinaro},  
  title = {From Theory to Experimental Evaluation: Resource Management in Software-Defined Vehicular Networks},  
  journal = {{IEEE} Access}  
}

