{
  "dataset_reader": {
    "type": "streusle",
    "token_indexers": {
        "bert": {
            "type": "pretrained_transformer",
            "model_name": "/home/irfan/Downloads/bert-base-uncased"
        }
    }
  },
  "data_loader": {
        "batch_sampler": {
            "type": "bucket",
            "batch_size": 16
        }
    },
  "train_data_path": "data/streusle/streusle.ud_train.json",
  "validation_data_path": "data/streusle/streusle.ud_dev.json",
  "test_data_path": "data/streusle/streusle.ud_test.json",
  "model": {
    "type": "streusle_tagger",
    "use_upos_constraints": false,
    "use_lemma_constraints": false,
    "text_field_embedder": {
        "token_embedders": {
            "bert": {
                "type": "pretrained_transformer",
                "model_name": "/home/irfan/Downloads/bert-base-uncased"
            }
        }
    }
  },

  "trainer": {
    "validation_metric": "+accuracy",
    "optimizer": {
        "type": "adam",
        "lr": 0.001
    },
    "num_serialized_models_to_keep": 1,
    "num_epochs": 10,
    "grad_norm": 5.0,
    "patience": 25,
    "cuda_device": 0
  }
}
