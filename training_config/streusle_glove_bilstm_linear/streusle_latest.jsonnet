{
  "dataset_reader": {
    "type": "streusle",
    "token_indexers": {
        "tokens": {
            "type": "single_id"
        },
        "token_characters": {
            "type": "characters",
            "min_padding_length": 5
        }
    }
  },
  "data_loader": {
        "batch_sampler": {
            "type": "bucket",
            "batch_size": 64
        }
    },
  "train_data_path": "data/streusle/streusle.ud_train.json",
  "validation_data_path": "data/streusle/streusle.ud_dev.json",
  "test_data_path": "data/streusle/streusle.ud_test.json",
  "model": {
    "type": "streusle_tagger_linear",
    "train_with_constraints": false,
    "use_upos_constraints": true,
    "use_lemma_constraints": true,
    "text_field_embedder": {
        "token_embedders": {
            "tokens": {
                "type": "embedding",
                "pretrained_file": "/home/irfan/Downloads/glove.6B.300d.txt",
                "embedding_dim": 300,
                "trainable": false
            },
            "token_characters": {
                "type": "character_encoding",
                "embedding": {
                    "embedding_dim": 64
                },
                "encoder": {
                    "type": "cnn",
                    "embedding_dim": 64,
                    "num_filters": 200,
                    "ngram_filter_sizes": [
                        5
                    ]
                }
            }
        }
    },
    "encoder": {
        "type": "lstm",
        "bidirectional": true,
        "input_size": 500,
        "hidden_size": 256,
        "num_layers": 2
    }
  },
  "trainer": {
    "validation_metric": "+accuracy",
    "optimizer": {
        "type": "adam",
        "lr": 0.001
    },
    "num_serialized_models_to_keep": 1,
    "num_epochs": 75,
    "grad_norm": 5.0,
    "patience": 25,
    "cuda_device": 0
  }
}
