//> <
#define SDL_MAIN_HANDLED
#include<SDL2/SDL.h>
#include<stdio.h>
#include<time.h>

SDL_Window *window;
SDL_Surface *surface;
SDL_Surface *PaintSurface;
SDL_Rect windowRect;
FILE *filePtr;
SDL_Event event;
float frame_time;
int frame_size;

typedef struct
{
	unsigned char r;
	unsigned char g;
	unsigned char b;
	unsigned char a;
} Color;

void FillPixels(SDL_Surface* surface)
{
	SDL_LockSurface(PaintSurface);
	char pixel_array[windowRect.h][windowRect.w][3];
	fread(pixel_array,sizeof(unsigned char),frame_size,filePtr);
	unsigned char tempbyte;
	if(filePtr == NULL);
	for(int pixy = 0;pixy < windowRect.h;pixy++)
	{
		for(int pixx = 0;pixx < windowRect.w;pixx++)
		{
			*((char*)(*PaintSurface).pixels + pixx*4 + pixy * surface->pitch + 0) = pixel_array[pixy][pixx][2];
			*((char*)(*PaintSurface).pixels + pixx*4 + pixy * surface->pitch + 1) = pixel_array[pixy][pixx][1];
			*((char*)(*PaintSurface).pixels + pixx*4 + pixy * surface->pitch + 2) = pixel_array[pixy][pixx][0];
			*((char*)(*PaintSurface).pixels + pixx*4 + pixy * surface->pitch + 3) = 0xFF;
		}
	}
	fread(&tempbyte,sizeof(unsigned char),1,filePtr);
	if(feof(filePtr))
		fseek(filePtr,5,SEEK_SET);
	else fseek(filePtr,-1,SEEK_CUR);
	SDL_UnlockSurface(PaintSurface);
	if((SDL_UpperBlit(PaintSurface,&windowRect,surface,&windowRect)) < 0)
		exit(0x04);
}


void ReadHeader(int argc, char **argv)
{
	unsigned char temp;
	windowRect.w = 0;windowRect.h = 0;
	
	if(argc != 2) 
		exit(0x01);
	
	filePtr = fopen(argv[1],"r");
	
	if(filePtr == NULL) 
		exit(0x02);
	
	fread(&temp,sizeof(unsigned char),1,filePtr);
	frame_time = 1/temp;
	
	for(char i = 1; i >= 0;i--)
	{
		fread(&temp,sizeof(unsigned char),1,filePtr);
		windowRect.w += temp << 8*i;
	}
	for(char i = 1; i >= 0;i--)
	{
		fread(&temp,sizeof(unsigned char),1,filePtr);
		windowRect.h += temp << 8*i;
	}
	frame_size = windowRect.w * windowRect.h * 3;
}

int main(int argc, char **argv)
{
	SDL_Init(SDL_INIT_VIDEO);
	windowRect.x = 0;windowRect.y = 0;
	ReadHeader(argc, argv);
	window = SDL_CreateWindow("BluePlayer - 1.0",SDL_WINDOWPOS_CENTERED,SDL_WINDOWPOS_CENTERED,windowRect.w,windowRect.h,0);
	surface = SDL_GetWindowSurface(window);
	PaintSurface = SDL_CreateRGBSurface(0,windowRect.w,windowRect.h,32,0x00FF0000,0x0000FF00,0x000000FF,0xFF000000);
	if(PaintSurface == NULL) exit(0x03);
	clock_t starting_time;
	while(1)
	{
		while(SDL_PollEvent(&event))
		{
			switch(event.type)
			{
				case SDL_QUIT:
					goto Exit;
			}
		}
		surface = SDL_GetWindowSurface(window);
		starting_time = clock();
		FillPixels(surface);
		SDL_UpdateWindowSurface(window);
		SDL_Delay((frame_time - (clock()-starting_time) / CLOCKS_PER_SEC)*1000);
	}
	Exit:
		fclose(filePtr);
		SDL_DestroyWindow(window);	
		SDL_Quit();
	return 0;
}


