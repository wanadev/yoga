// Assimp

typedef struct ImageNode {
    struct ImageNode* next;
    
    // If bytes_length is non zero, bytes is filled.
    // Otherwise, path is.
    char* path;
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

typedef enum OptimizationFlag {
    OPTIMIZATION_FLAG_GRAPH = 1,
    OPTIMIZATION_FLAG_MESHES = 2,
} OptimizationFlag;

// Import an input model.
Scene assimp_import_from_bytes(int optimization_flags_in, char* bytes_in, int length_in);

// Returns *bytes_out length.
int assimp_export_to_bytes(Scene scene_in, OutputFormat output_format_in, char** bytes_out);

// Free allocated scene.
void assimp_free_scene(Scene scene);

// Free allocated bytes.
void assimp_free_bytes(char** bytes);
