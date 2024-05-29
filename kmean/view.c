#include <stdlib.h>
#include "tgui.h"
#include "tgin.h"

int main(){
	FILE *data = fopen(".out.txt", "r");

	int n; fscanf(data, "%d", &n);

	int *points = malloc(sizeof(int) * n * 3);

	for(int i=0; i<n; ++i)
		fscanf(data, "%d %d %d", points+i*3, points+i*3+1, points+i*3+2);

	int m; fscanf(data, "%d", &m);

	int *centroids = malloc(sizeof(int) * m * 3);

	for(int i=0; i<m; ++i)
		fscanf(data, "%d %d %d", centroids+i*3,
			centroids+i*3+1, centroids+i*3+2);

	fclose(data);

	system("clear");
	openfb();

	int colors[7][3] = {
		{255, 0, 0},
		{0, 255, 0},
		{0, 0, 255},
		{255, 255, 0},
		{255, 0, 255},
		{0, 255, 255},
		{255, 255, 255}
	};

	rect(24, 24, width-48, height-48, 10, 10, 10);

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

	char c; scanf("%c", &c);

	blank();
	closefb();
}
