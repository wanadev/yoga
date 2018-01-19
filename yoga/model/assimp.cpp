extern "C" {
    #include "assimp.h"
}

#include <assimp/Importer.hpp>
#include <assimp/Exporter.hpp>
#include <assimp/DefaultLogger.hpp>

using namespace Assimp;

Scene assimp_import_from_bytes(int optimization_flags_in, char* bytes_in, int length_in) {
    Scene scene;

    // DefaultLogger::create(nullptr, Logger::NORMAL, aiDefaultLogStream_STDOUT);
    DefaultLogger::get()->attachStream(LogStream::createDefaultStream(aiDefaultLogStream_STDERR), Assimp::Logger::Err);

    Importer importer;
    importer.ReadFileFromMemory(bytes_in, length_in, 0u);

    // Free the ownership of the scene from the importer
    scene.assimp_scene = importer.GetOrphanedScene();

    return scene;
}

int assimp_export_to_bytes(Scene scene_in, OutputFormat output_format_in, char** bytes_out) {
    Exporter exporter;

    auto outputFormat = output_format_in == OUTPUT_FORMAT_GLB ? "glb2" : "gltf2";

    // @todo Apply images bytes back

    auto scene = reinterpret_cast<aiScene*>(scene_in.assimp_scene);
    auto blob = exporter.ExportToBlob(scene, outputFormat, 0, nullptr); // @fixme
    if (blob == nullptr) return 0;

    *bytes_out = reinterpret_cast<char*>(blob->data);
    return blob->size;
}

void assimp_free_scene(Scene scene) {
    // @fixme Not implemented yet
}

void assimp_free_bytes(char** bytes) {
    // @fixme Not implemented yet
}
