#include <stdio.h>
#include <stdlib.h>

#include "readline/readline.h"

int main(int argc, char *argv[]) {

    if(!ISALPHA('a') || !ISDIGIT('1')) {
        return EXIT_FAILURE;
    }
    rl_message("Bincrafters");

    return EXIT_SUCCESS;
}
