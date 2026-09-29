.PHONY: test demo clean

test:
	python -m unittest discover -s tests -t . -v

demo: clean
	python -m bibliolivre --db demo.db livro-add 978-85-359-0277-8 "Dom Casmurro" "Machado de Assis" --exemplares 2
	python -m bibliolivre --db demo.db membro-add "Ana Souza" ana@email.com
	python -m bibliolivre --db demo.db emprestar 9788535902778 1
	python -m bibliolivre --db demo.db livros
	python -m bibliolivre --db demo.db renovar 1
	python -m bibliolivre --db demo.db devolver 1
	python -m bibliolivre --db demo.db membro-anonimizar 1

clean:
	rm -f demo.db
