#




testDongle: venv/bin/activate
	. venv/bin/activate && python3 dongle.py
    
    

test: venv/bin/activate
	. venv/bin/activate && python3 sensor.py
    
    
venv/bin/activate: requirements.txt
	python3 -m venv venv
	. venv/bin/activate && pip3 install -r requirements.txt	
  