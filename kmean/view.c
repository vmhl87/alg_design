#include <stdlib.h>

// framebuffer libs  -  https://github.com/vmhl87/fbgui
#include "tgui.c"
#include "tgin.c"


int main(){
	// open coloring file and read
	FILE *data = fopen(".out.txt", "r");

	// points
	int n; fscanf(data, "%d", &n);
	int *points = malloc(sizeof(int) * n * 3);
	for(int i=0; i<n; ++i)
		fscanf(data, "%d %d %d", points+i*3, points+i*3+1, points+i*3+2);

	// centroids
	int m; fscanf(data, "%d", &m);
	int *centroids = malloc(sizeof(int) * m * 3);
	for(int i=0; i<m; ++i)
		fscanf(data, "%d %d %d", centroids+i*3,
			centroids+i*3+1, centroids+i*3+2);

	// cleanup file stream
	fclose(data);

	// cleanup terminal
	system("clear");
	openfb();

	// very simplistic pallete
	int colors[7][3] = {
		{255, 0, 0},
		{0, 255, 0},
		{0, 0, 255},
		{255, 255, 0},
		{255, 0, 255},
		{0, 255, 255},
		{255, 255, 255}
	};

	// initial background
	rect(24, 24, width-48, height-48, 10, 10, 10);

	// draw points
	for(int i=0; i<n; ++i){
		rect(
			width/2 - 203 + points[i*3],
			height/2 - 203 + points[i*3+1],
			6, 6,
			colors[points[i*3+2]][0],
			colors[points[i*3+2]][1],
			colors[points[i*3+2]][2]
		);
	}

	// draw centroids
	for(int i=0; i<m; ++i){
		line(
			width/2 - 205 + centroids[i*3],
			height/2 - 205 + centroids[i*3+1],
			width/2 - 197 + centroids[i*3],
			height/2 - 197 + centroids[i*3+1],
			colors[i][0],
			colors[i][1],
			colors[i][2]
		);
		line(
			width/2 - 205 + centroids[i*3],
			height/2 - 197 + centroids[i*3+1],
			width/2 - 197 + centroids[i*3],
			height/2 - 205 + centroids[i*3+1],
			colors[i][0],
			colors[i][1],
			colors[i][2]
		);
	}

	// break and wait on input
	char c; scanf("%c", &c);

	// clear framebuffer and cleanup
	blank();
	closefb();
}
