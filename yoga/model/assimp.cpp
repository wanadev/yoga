extern "C" {
    #include "assimp.h"
}

#include <assimp/scene.h>

Scene assimp_import_from_bytes(OutputFormat output_format_in, int optimization_flags_in,
                               char* bytes_in, int length_in) {
    // @fixme Not implemented yet
    return Scene();
}

int assimp_export_to_bytes(Scene scene_in, char** bytes_out) {
    // @fixme Not implemented yet
    return 0;
}

void assimp_free_scene(Scene scene) {
    // @fixme Not implemented yet
}

void assimp_free_bytes(char** bytes) {
    // @fixme Not implemented yet
}
