install :
	cd ./evm-interaction && npm install
	cd ..
	cd ./script && npm install
	cd ..
	pip3 install -r requirements.txt
	cd .. 

run :
	streamlit run app.py
	
.PHONY:	all