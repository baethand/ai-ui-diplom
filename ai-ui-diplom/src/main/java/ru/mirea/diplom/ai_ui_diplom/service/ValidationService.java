package ru.mirea.diplom.ai_ui_diplom.service;

import jakarta.validation.ValidationException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ru.mirea.diplom.ai_ui_diplom.configuration.ImageGenerationConfig;
import ru.mirea.diplom.ai_ui_diplom.model.ImageGenerationRequest;
import ru.mirea.diplom.ai_ui_diplom.model.exceptions.BaseException;

import java.util.HashSet;

@Service
public class ValidationService {

    private final ImageGenerationConfig imageGenerationLimits;

    HashSet<String> availableModels = new HashSet<>();

    @Autowired
    public ValidationService(ImageGenerationConfig imageGenerationLimits) {
        this.imageGenerationLimits = imageGenerationLimits;
    }


    public void validateImageGenerationRequest(ImageGenerationRequest imageGenerationRequest) throws BaseException {

        if (imageGenerationRequest.getNumInferenceSteps() < imageGenerationLimits.getMinSteps()
                || imageGenerationRequest.getNumInferenceSteps() > imageGenerationLimits.getMaxSteps()) {
            throw new BaseException(String.format("numInferenceSteps must be between %d and %d.",
                    imageGenerationLimits.getMinSteps(),
                    imageGenerationLimits.getMaxSteps()));
        }
        if (imageGenerationRequest.getGuidanceScale() < imageGenerationLimits.getMinGuidanceScale()
                || imageGenerationRequest.getGuidanceScale() > imageGenerationLimits.getMaxGuidanceScale()) {
            throw new BaseException(String.format("guidanceScale must be between %.1f and %.1f.",
                    imageGenerationLimits.getMinGuidanceScale(),
                    imageGenerationLimits.getMaxGuidanceScale()));
        }
        if (imageGenerationRequest.getHeight() < imageGenerationLimits.getMinHeight()
                || imageGenerationRequest.getHeight() > imageGenerationLimits.getMaxHeight()
                || imageGenerationRequest.getWidth() < imageGenerationLimits.getMinWidth()
                || imageGenerationRequest.getWidth() > imageGenerationLimits.getMaxWidth()) {
            throw new BaseException(String.format("Height and width must be between %d and %d.",
                    imageGenerationLimits.getMinHeight(),
                    imageGenerationLimits.getMaxHeight()));
        }
    }
}
