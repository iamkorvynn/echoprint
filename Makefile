.PHONY: test demo library clips plots benchmark clean

test:
	pytest -q

demo:
	python demo.py

library:
	python scripts/generate_library.py

clips:
	python scripts/make_clips.py

plots:
	python scripts/plot_all.py

benchmark:
	python scripts/benchmark.py

verify:
	python scripts/verify_library.py

batch:
	python -m echoprint batch demo_clips/

clean:
	rm -rf __pycache__ echoprint/__pycache__ echoprint/synth/__pycache__ tests/__pycache__ .pytest_cache
