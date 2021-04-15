extern "C" {
    #include "assimp.h"
}

#include <assimp/Importer.hpp>
#include <assimp/Exporter.hpp>
#include <assimp/DefaultLogger.hpp>
#include <assimp/postprocess.h>
#include <assimp/scene.h>

#include <set>
#include <string>
#include <sstream>
#include <unordered_map>

using namespace Assimp;

const auto MAGIC_PNG = "\x89PNG\r\n";
const auto MAGIC_JPEG = "\xFF\xD8\xFF\xE0";

ImageNode* extract_image_nodes(aiScene* pScene);
void import_image_nodes(aiScene* pScene, ImageNode* images);
void add_texture(aiScene* pScene, char* bytes, int bytes_length);

void assimp_import_from_bytes(char* bytes_in, int length_in, int flags_in, Scene* scene_out, int verbose) {
    // Enable verbose mode if asked
    if (verbose) {
        DefaultLogger::create(nullptr, Logger::NORMAL, aiDefaultLogStream_STDOUT);
    }

    unsigned int flags = 0u
        // | aiProcess_FindDegenerates          // Do not use, this can generate points and lines
        // | aiProcess_PreTransformVertices     // A bit too harsh, as it will remove the scene hierarchy
        // | aiProcess_EmbedTextures            // We do that by ourself in python
        | aiProcess_JoinIdenticalVertices
        | aiProcess_Triangulate
        | aiProcess_GenSmoothNormals
        | aiProcess_ImproveCacheLocality
        | aiProcess_RemoveRedundantMaterials
        | aiProcess_FindInvalidData
        | aiProcess_GenUVCoords;

    if (flags_in & FLAG_OPTIMIZE_GRAPH) {
        flags |= aiProcess_OptimizeGraph;
    }
    if (flags_in & FLAG_OPTIMIZE_MESHES) {
        flags |= aiProcess_OptimizeMeshes;
    }
    if (flags_in & FLAG_FIX_INFACING_NORMALS) {
        flags |= aiProcess_FixInfacingNormals;
    }

    Importer importer;
    importer.ReadFileFromMemory(bytes_in, length_in, flags);

    // Free the ownership of the scene from the importer
    auto pScene = importer.GetOrphanedScene();
    scene_out->assimp_scene = pScene;
    if (pScene == nullptr) return;

    // Extract image nodes
    scene_out->images = extract_image_nodes(pScene);
}

int assimp_export_to_bytes(Scene* scene_in, OutputFormat output_format_in, char** bytes_out) {
    auto pScene = reinterpret_cast<aiScene*>(scene_in->assimp_scene);
    Exporter exporter;

    import_image_nodes(pScene, scene_in->images);

    auto outputFormat = output_format_in == OUTPUT_FORMAT_GLB ? "glb2" : "gltf2";
    auto blob = exporter.ExportToBlob(pScene, outputFormat, 0, nullptr);
    if (blob == nullptr) return 0;

    // Copying bytes - as they will be freed
    *bytes_out = new char[blob->size];
    memcpy(*bytes_out, blob->data, blob->size);
    return blob->size;
}

void assimp_free_bytes(char** bytes) {
    delete[] *bytes;
    *bytes = nullptr;
}

void assimp_free_scene(Scene* scene) {
    free(reinterpret_cast<aiScene*>(scene->assimp_scene));

    auto image = scene->images;
    while (image != nullptr) {
        auto nextImage = image->next;
        delete image;
        image = nextImage;
    }
}

//---- Private

ImageNode* extract_image_nodes(aiScene* pScene) {
    ImageNode* images = nullptr;

    std::set<std::string> seenTextures;
    aiString path;
    for (auto matId = 0u; matId < pScene->mNumMaterials; ++matId) {
        auto material = pScene->mMaterials[matId];
 
        for (auto ttId = 1u; ttId < AI_TEXTURE_TYPE_MAX; ++ttId) {
            auto tt = static_cast<aiTextureType>(ttId);
            auto texturesCount = material->GetTextureCount(tt);
 
            for (auto texId = 0u; texId < texturesCount; ++texId) {
                material->GetTexture(tt, texId, &path);
                if (seenTextures.find(path.C_Str()) != seenTextures.end()) continue;

                seenTextures.emplace(path.C_Str()); 
                auto imageNode = new ImageNode();
                imageNode->path = strcpy(new char[path.length + 1], path.C_Str());
                imageNode->next = images;
                images = imageNode;

                // Load bytes of embedded textures
                if (path.data[0] == '*') {
                    // @todo Already embedded textures are not supported yet
                }
            }
        }
    }

    return images;
}

void import_image_nodes(aiScene* pScene, ImageNode* images) {
    std::unordered_map<std::string, std::string> texturesMap;
    std::unordered_map<int, std::string> seenTextures;
    
    // Embed all images
    auto image = images;
    while (image != nullptr) {
        if (image->bytes_length > 0 && image->path[0] != '*') {
            // Images might have different paths at first,
            // they still can point to the same image - as identified by their id.
            if (seenTextures.find(image->id) != std::end(seenTextures)) {
                texturesMap[image->path] = seenTextures[image->id];
            } else {
                add_texture(pScene, image->bytes, image->bytes_length);

                auto embeddedTextureId = pScene->mNumTextures - 1u;
                std::stringstream path;
                path << "*" << embeddedTextureId;
                texturesMap[image->path] = path.str();
                seenTextures[image->id] = path.str();
            }
        }

        image = image->next;
    }

    // Update materials references
    aiString path;
    for (auto matId = 0u; matId < pScene->mNumMaterials; ++matId) {
        auto material = pScene->mMaterials[matId];
 
        for (auto ttId = 1u; ttId < AI_TEXTURE_TYPE_MAX; ++ttId) {
            auto tt = static_cast<aiTextureType>(ttId);
            auto texturesCount = material->GetTextureCount(tt);
 
            for (auto texId = 0u; texId < texturesCount; ++texId) {
                material->GetTexture(tt, texId, &path);
                auto newPath = texturesMap.find(path.C_Str());
                if (newPath == texturesMap.end()) continue;

                path = newPath->second;
                material->AddProperty(&path, AI_MATKEY_TEXTURE(tt, texId));

                // @todo If already embedded texture, update textures table
            }
        }
    }
}

void add_texture(aiScene* pScene, char* bytes, int bytes_length) {
    // Grow the textures table
    auto textureId = pScene->mNumTextures++;
    auto oldTextures = pScene->mTextures;
    pScene->mTextures = new aiTexture*[pScene->mNumTextures];
    memmove(pScene->mTextures, oldTextures, sizeof(aiTexture*) * (pScene->mNumTextures - 1u));

    // Add the new texture
    auto pTexture = new aiTexture();
    pTexture->mHeight = 0; // Means that this is still compressed
    pTexture->mWidth = bytes_length;
    pTexture->pcData = reinterpret_cast<aiTexel*>(bytes);

    if (strncmp(bytes, MAGIC_JPEG, 4) == 0) {
        strcpy(pTexture->achFormatHint, "jpg");
    } else if (strncmp(bytes, MAGIC_PNG, 6) == 0) {
        strcpy(pTexture->achFormatHint, "png");
    }

    pScene->mTextures[textureId] = pTexture;
}
