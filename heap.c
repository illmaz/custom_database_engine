#define PAGE_SIZE 4096
#define ROW_SIZE 37
#define ROWS_PER_PAGE (PAGE_SIZE / ROW_SIZE)
#define BUFFER_SIZE 3

#include <stdio.h>
#include <string.h>

struct Row {
    unsigned int id;
    char name[32];
    unsigned char age;
} __attribute__((packed));

struct Page {
    struct Row rows[ROWS_PER_PAGE];
};

struct BufferSlot {
    int page_number;
    int is_used;
};

struct BufferPool {
    struct Page pages [BUFFER_SIZE];
    struct BufferSlot slots[BUFFER_SIZE];

};


void insert_row(struct Page *page, int slot, struct Row row) {
    page ->rows[slot] = row; 
}

FILE* open_or_create(const char *filepath) {
        FILE *file = fopen(filepath, "r+b");
        if (file == NULL) {
            file = fopen(filepath, "wb");
        }
        return file; 
}

void write_page(struct Page *page, const char *filepath, int page_number) {
    FILE *file = open_or_create(filepath);
    fseek(file, page_number * PAGE_SIZE, SEEK_SET);
    fwrite(page, PAGE_SIZE, 1, file);
    fclose(file);

}

void read_page(struct Page *page, const char *filepath, int page_number) {
    FILE *file = fopen(filepath, "rb");
    fseek(file, page_number * PAGE_SIZE, SEEK_SET);
    fread(page, PAGE_SIZE, 1, file);
    fclose(file); 
}

struct Row read_row(struct Page *page, int slot) {
    return page->rows[slot];
}

int count_pages(const char *filepath) {
    FILE *file = fopen(filepath, "rb");
    if (file == NULL) return 0;
    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fclose(file);
    return size / PAGE_SIZE; 
}

void init_buffer_pool(struct BufferPool *pool) {
    for (int i = 0; i < BUFFER_SIZE; i++) {
        pool ->slots[i].is_used = 0;
        pool->slots[i].page_number = -1;
    }
}

struct Page *get_page(struct BufferPool *pool, const char *filepath, int page_number) {
    for (int i = 0; i < BUFFER_SIZE; i++) {
        if (pool ->slots[i].is_used && pool->slots[i].page_number == page_number) {
            return &pool ->pages[i];
        
        }
    }
    for (int i = 0; i < BUFFER_SIZE; i++) {
        if (pool->slots[i].is_used == 0) {
            read_page(&pool->pages[i], filepath, page_number);
            pool->slots[i].page_number = page_number;
            pool->slots[i].is_used = 1;
            return &pool ->pages[i];
        }

    } 
    return NULL;

}

