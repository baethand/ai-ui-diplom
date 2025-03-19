package ru.mirea.diplom.ai_ui_diplom.configuration;

import lombok.Getter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Getter
@Configuration
@ConfigurationProperties(prefix = "image.generation")
public class ImageGenerationConfig {

    private int minSteps;
    private int maxSteps;

    private float minGuidanceScale;
    private float maxGuidanceScale;

    private int minHeight;
    private int maxHeight;

    private int minWidth;
    private int maxWidth;

}