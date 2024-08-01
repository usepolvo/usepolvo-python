include .env

default: run
MAKEFLAGS += -s

help:
	@echo "⚈ run			---> 🎮 Run project locally (default)."
	@echo "⚈ debug			---> 🕵️  Debug project locally."
	@echo "⚈ freeze		---> 🧊 Freeze requirements."
	@echo "⚈ sort			---> ⬇️  Sort requirements and env files alphabetically".

run:
	@echo "\n> 🎮 Running the project locally... (default)\n"

debug:
	@echo "\n> 🕵️  Debugging the project locally...\n"

freeze:
	@echo "\n> 🧊 Freezing the requirements...\n"
	@for file in requirements*.txt; do \
		if [ -f $$file ]; then \
			pip3 freeze -q -r $$file | sed '/freeze/,$$ d' > requirements-froze.txt && mv requirements-froze.txt $$file; \
			echo "Froze requirements in $$file"; \
		else \
			echo "$$file not found, skipping..."; \
		fi \
	done
	@python src/update_pyproject.py

sort:
	@echo "\n> ⬇️ Sorting requirements and env files alphabetically...\n"
	@for file in requirements*.txt; do \
		if [ -f $$file ]; then \
			sort --ignore-case -u -o $$file{,}; \
			echo "Sorted $$file"; \
		else \
			echo "$$file not found, skipping..."; \
		fi \
	done
	@for file in .env*; do \
		if [ -f $$file ]; then \
			sort --ignore-case -u -o $$file{,}; \
			echo "Sorted $$file"; \
		else \
			echo "$$file not found, skipping..."; \
		fi \
	done
