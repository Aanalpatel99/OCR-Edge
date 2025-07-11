from transformers import VisionEncoderDecoderModel, ViTConfig, TrOCRConfig, VisionEncoderDecoderConfig

def get_student_model():
    # Configure smaller encoder (ViT)
    encoder_config = ViTConfig(
        num_hidden_layers=4,
        hidden_size=384,
        num_attention_heads=6,
        intermediate_size=1024,
        image_size=384,
        patch_size=16,
        num_channels=3,
    )

    # Configure smaller decoder (TrOCR)
    decoder_config = TrOCRConfig(
        vocab_size=50265,
        d_model=384,
        decoder_layers=4,
        decoder_attention_heads=6,
        decoder_ffn_dim=1024,
        activation_function="relu",
        dropout=0.1,
        attention_dropout=0.1,
        pad_token_id=1,
        bos_token_id=0,
        eos_token_id=2,
        max_position_embeddings=512,
        is_decoder=True,
        add_cross_attention=True
    )

    # ✅ Properly wrap configs
    model_config = VisionEncoderDecoderConfig.from_encoder_decoder_configs(
        encoder_config=encoder_config,
        decoder_config=decoder_config
    )

    model = VisionEncoderDecoderModel(config=model_config)
    return model
