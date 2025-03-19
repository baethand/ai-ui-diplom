package ru.mirea.diplom.ai_ui_diplom.model;

import jakarta.validation.constraints.*;
import lombok.Data;
import org.springframework.validation.annotation.Validated;

@Data
@Validated
public class ImageGenerationRequest {
    @NotBlank
    private String prompt;

    @NotNull
    private String modelId = "stabilityai/stable-diffusion-2-1";

    @Min(1) @Max(150)
    private int numInferenceSteps = 50;

    @DecimalMin("1.0") @DecimalMax("20.0")
    private float guidanceScale = 12.0f;

    @Min(256) @Max(1024)
    private int height = 768;

    @Min(256) @Max(1024)
    private int width = 768;

    private String device = "cuda";
}
