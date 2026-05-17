#define PAGE_SIZE 4096
#define ROW_SIZE 38
#define ROWS_PER_PAGE (PAGE_SIZE / ROW_SIZE)

#include <stdio.h>
#include <string.h>

struct Row {
    unsigned char is_occupied;
    unsigned int id;
    char name[32];
    unsigned char age;
} __attribute__((packed));

struct Page {
    struct Row rows[ROWS_PER_PAGE];
};

void insert_row(struct Page *page, int slot, struct Row row) {
    page ->rows[slot] = row; 
}

void write_page(struct Page *page, const char *filepath) {
    FILE *file = fopen(filepath, "wb");
    fwrite(page, PAGE_SIZE, 1, file);
    fclose(file);
}

void read_page(struct Page *page, const char *filepath) {
    FILE *file = fopen(filepath, "rb");
    fread(page, PAGE_SIZE, 1, file);
    fclose(file); 
}

struct Row read_row(struct Page *page, int slot) {
    return page->rows[slot];
}

int main() {
    struct Row row;
    struct Page page;

    memset(&page, 0, sizeof(page));

    row.id = 1;
    row.age = 30;
    strcpy(row.name, "Alice");

    insert_row(&page, 0, row);
    printf("id: %u, name: %s, age: %u\n", page.rows[0].id, page.rows[0].name, page.rows[0].age);
    
    write_page(&page, "phase2.db");

    memset(&page, 0, sizeof(page));

    read_page(&page, "phase2.db");
    printf("id: %u, name: %s, age: %u\n", page.rows[0].id, page.rows[0].name, page.rows[0].age);
    
    struct Row r = read_row(&page, 0);
    printf("row 0: id=%u, name=%s, age=%u\n", r.id, r.name, r.age);

    return 0;

}