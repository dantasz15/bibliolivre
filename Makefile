.PHONY: install-dev test coverage lint demo clean

install-dev:
	python3 -m pip install -e ".[dev]"

test:
	python3 -m unittest discover -s tests -t . -v

coverage:
	./scripts/run_coverage.sh

lint:
	ruff check bibliolivre tests

demo: clean
	python3 -m bibliolivre --db demo.db livro-add 978-85-359-0277-8 "Dom Casmurro" "Machado de Assis" --exemplares 2
	python3 -m bibliolivre --db demo.db membro-add "Ana Souza" ana@email.com
	python3 -m bibliolivre --db demo.db emprestar 9788535902778 1
	python3 -m bibliolivre --db demo.db livros
	python3 -m bibliolivre --db demo.db renovar 1
	python3 -m bibliolivre --db demo.db devolver 1
	python3 -m bibliolivre --db demo.db membro-anonimizar 1

clean:
	rm -f demo.db
