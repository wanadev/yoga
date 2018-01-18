extern "C" {
    #include "assimp.h"
}

#include <assimp/Importer.hpp>
#include <assimp/DefaultLogger.hpp>

using namespace Assimp;

Scene assimp_import_from_bytes(int optimization_flags_in, char* bytes_in, int length_in) {
    Scene scene;

    // DefaultLogger::create(nullptr, Logger::NORMAL, aiDefaultLogStream_STDOUT);
    DefaultLogger::get()->attachStream(LogStream::createDefaultStream(aiDefaultLogStream_STDERR), Assimp::Logger::Err);

    Importer importer;
	scene.assimp_scene = const_cast<aiScene*>(importer.ReadFileFromMemory(bytes_in, length_in, 0u));

    // GetOrphanedScene () to free the ownership?

    return scene;
}

int assimp_export_to_bytes(Scene scene_in, OutputFormat output_format_in, char** bytes_out) {
    // @fixme Not implemented yet
    return 0;
}

void assimp_free_scene(Scene scene) {
    // @fixme Not implemented yet
}

void assimp_free_bytes(char** bytes) {
    // @fixme Not implemented yet
}
