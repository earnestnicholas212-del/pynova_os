.PHONY: run test cli sim benchmark clean

run:
	PYTHONPATH=src python main.py

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

cli:
	PYTHONPATH=src python cli.py sim --algo Round_Robin --ticks 100

sim:
	PYTHONPATH=src python cli.py sim --algo $(ALGO) --ticks $(TICKS) --processes $(PROCS)

benchmark:
	PYTHONPATH=src python benchmark.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
