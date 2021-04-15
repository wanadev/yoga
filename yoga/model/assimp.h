// Assimp

typedef struct ImageNode {
    struct ImageNode* next;
    
    // If bytes_length is non zero, bytes is filled.
    // Otherwise, path is a file path.
    const char* path;

    // Set by yoga.
    // If two paths are resolved to the same file,
    // they will share the same id.
    int id;

    char* bytes;
    int bytes_length;
} ImageNode;

typedef struct Scene {
    void* assimp_scene;
    ImageNode* images;
} Scene;

typedef enum OutputFormat {
    OUTPUT_FORMAT_GLTF,
    OUTPUT_FORMAT_GLB,
} OutputFormat;

typedef enum Flag {
    FLAG_OPTIMIZE_GRAPH = 1,
    FLAG_OPTIMIZE_MESHES = 2,
    FLAG_FIX_INFACING_NORMALS = 4,
} Flag;

// Import an input model.
void assimp_import_from_bytes(char* bytes_in, int length_in, int flags_in, Scene* scene_out, int verbose);

// Returns *bytes_out length.
int assimp_export_to_bytes(Scene* scene_in, OutputFormat output_format_in, char** bytes_out);

// Free allocated bytes.
void assimp_free_bytes(char** bytes);

// Free allocated scene.
void assimp_free_scene(Scene* scene);
