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