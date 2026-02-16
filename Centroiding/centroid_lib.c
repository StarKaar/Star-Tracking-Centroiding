#include <stdint.h>

typedef struct {
    float x;
    float y;
    float flux;
} StarCentroid;

#define DLLEXPORT __declspec(dllexport)

DLLEXPORT int find_star_centroids(uint8_t* image, int width, int height, uint8_t threshold, int win_size, StarCentroid* results, int max_stars) {
    int star_count = 0;
    int half_win = win_size / 2;
    printf("\nC DEBUG: width=%d, height=%d\n", width, height);

    for (int y = half_win; y < height - half_win; y++) {
        // SAFETY: Stop processing if we've filled the results buffer
        if (star_count >= max_stars) break;

        for (int x = half_win; x < width - half_win; x++) {
            // Indexing check: Ensure y * width matches Python's row-major order
            uint8_t pixel_val = image[y * width + x];

            if (pixel_val > threshold) {
                // 1. Local Peak Check
                int is_peak = 1;
                for (int ny = -1; ny <= 1; ny++) {
                    for (int nx = -1; nx <= 1; nx++) {
                        if (image[(y + ny) * width + (x + nx)] > pixel_val) {
                            is_peak = 0; 
                            break;
                        }
                    }
                    if (!is_peak) break;
                }

                if (is_peak) {
                    float sum_i = 0.0f, sum_ix = 0.0f, sum_iy = 0.0f;
                    
                    // 2. Windowed CoG Calculation
                    for (int wy = -half_win; wy <= half_win; wy++) {
                        for (int wx = -half_win; wx <= half_win; wx++) {
                            float val = (float)image[(y + wy) * width + (x + wx)];
                            
                            // Background subtraction is vital for sub-pixel accuracy
                            float signal = (val > threshold) ? (val - threshold) : 0.0f;

                            sum_i += signal;
                            sum_ix += signal * (float)(x + wx);
                            sum_iy += signal * (float)(y + wy);
                        }
                    }

                    if (sum_i > 0) {
                        results[star_count].x = sum_ix / sum_i;
                        results[star_count].y = sum_iy / sum_i;
                        results[star_count].flux = sum_i;
                        star_count++;
                        
                        // 3. Jump ahead by half the window size
                        // This prevents the peak finder from triggering again 
                        // on the same star cluster.
                        x += half_win; 
                        
                        if (star_count >= max_stars) break;
                    }
                }
            }
        }
    }
    return star_count;
}