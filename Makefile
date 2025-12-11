install:
	@echo 'Installing Backend...'
	cd backend && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo 'Installing Frontend...'
	cd frontend && npm install

run-backend:
	cd backend && . venv/bin/activate && uvicorn main:app --reload --port 8000

run-frontend:
	cd frontend && npm run dev

run:
	@echo 'Starting Full Stack...'
	make -j 2 run-backend run-frontend
