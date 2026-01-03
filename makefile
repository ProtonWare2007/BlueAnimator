prog = ./BluePlayer.c
out = ./BluePlayer

$(out):$(prog)
	gcc $(prog) -o $(out) -lSDL2 -lm

run:
	$(out)

