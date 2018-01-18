extern "C" {
    #include "assimp.h"
}

#include <assimp/importer.hpp>

Scene assimp_import_from_bytes(OutputFormat output_format_in, int optimization_flags_in,
                               char* bytes_in, int length_in) {
    Scene scene;

    Assimp::Importer importer;
	scene.assimp_scene = importer.readFileFromMemory(bytes_in, length_in, importer);

    return scene;
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
