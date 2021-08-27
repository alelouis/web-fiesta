# Web-Fiesta

Fiesta De Los Muertos, on the web !

## Contribute
Clone repository and work and `dev` branch.  
```bash
git clone git@github.com:alelouis/web-fiesta.git
```
### **Front end**
Setup:  
```
cd fiesta-front  
npm install -g @angular/cli  
npm install
```

Run the front end:  
```bash
cd fiesta-front  
ng build
ng serve
```

### Back end
Setup:  
```bash
cd fiesta-back
conda env create -f environment.yml -n fiesta 
conda activate fiesta
```

Run the back end:  
```
cd fiesta-back
gunicorn -b 0.0.0.0:5000 -k eventlet api:app
```

### Testing
```
sudo apt install firefox
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/ 
```

#### On WSL
- Download and Install this Windows X Server https://sourceforge.net/projects/vcxsrv/
- Open XLaunch
- Select " Multiple Windows " option
- Choose " Start no client " option
Type this in WSL in order to redirect display.
```
export DISPLAY=0:0  
```