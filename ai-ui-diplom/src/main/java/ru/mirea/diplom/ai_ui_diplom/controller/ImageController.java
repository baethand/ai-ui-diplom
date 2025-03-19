package ru.mirea.diplom.ai_ui_diplom.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.web.bind.annotation.*;
import ru.mirea.diplom.ai_ui_diplom.configuration.ImageGenerationConfig;
import ru.mirea.diplom.ai_ui_diplom.model.ImageGenerationRequest;
import ru.mirea.diplom.ai_ui_diplom.service.ValidationService;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.concurrent.CompletableFuture;

@RestController
@RequestMapping("/api/images")
@EnableAsync
public class ImageController {

    // Путь к директории для сохранения изображений
    private static final String IMAGE_DIRECTORY = "target/generated-source/images";

    // Путь к Python-скрипту
    private static final String PYTHON_SCRIPT_PATH = "python/generate_image.py";

    private final ValidationService validationService;

    public ImageController(ValidationService validationService) {
        this.validationService = validationService;
    }

    @Async
    @PostMapping(value = "/generate", produces = MediaType.IMAGE_PNG_VALUE)
    public CompletableFuture<ResponseEntity<byte[]>> generateImage(
            @RequestParam String prompt,
            @RequestParam(defaultValue = "stabilityai/stable-diffusion-2-1") String modelId,
            @RequestParam(defaultValue = "50") int numInferenceSteps,
            @RequestParam(defaultValue = "12.0") float guidanceScale,
            @RequestParam(defaultValue = "768") int height,
            @RequestParam(defaultValue = "768") int width,
            @RequestParam(defaultValue = "cuda") String device
    ) {
        try {
            ImageGenerationRequest imageGenerationRequest = ImageGenerationRequest.builder()
                    .prompt(prompt)
                    .modelId(modelId)
                    .numInferenceSteps(numInferenceSteps)
                    .guidanceScale(guidanceScale)
                    .height(height)
                    .width(width)
                    .device((device.trim().equalsIgnoreCase("cuda")) ? device : "cpu")
                    .build();

            validationService.validateImageGenerationRequest(imageGenerationRequest);

            // Создание директории, если она не существует
            Path imageDir = Paths.get(IMAGE_DIRECTORY);
            if (!Files.exists(imageDir)) {
                Files.createDirectories(imageDir);
            }

            // Получение пути к Python-скрипту
            InputStream inputStream = getClass().getClassLoader().getResourceAsStream(PYTHON_SCRIPT_PATH);
            if (inputStream == null) {
                return CompletableFuture.completedFuture(ResponseEntity.badRequest().body("Python script not found!".getBytes()));
            }

            // Копирование скрипта во временную директорию (если ещё не скопирован)
            Path tempScript = Paths.get(IMAGE_DIRECTORY, "generate_image.py");
            if (!Files.exists(tempScript)) {
                Files.copy(inputStream, tempScript, StandardCopyOption.REPLACE_EXISTING);
            }

            // Путь для сохранения изображения
            String imageName = "generated_image_" + System.currentTimeMillis() + ".png";
            Path outputImagePath = imageDir.resolve(imageName);

            // Запуск Python-скрипта с параметрами
            ProcessBuilder processBuilder = new ProcessBuilder(
                    "python",
                    tempScript.toAbsolutePath().toString(),
                    prompt,
                    outputImagePath.toAbsolutePath().toString(),
                    modelId,  // Модель
                    String.valueOf(numInferenceSteps),
                    String.valueOf(guidanceScale),
                    String.valueOf(height),
                    String.valueOf(width),
                    device  // Устройство (cuda или cpu)
            );
            processBuilder.redirectErrorStream(true);

            Process process = processBuilder.start();

            // Чтение вывода скрипта
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }

            // Ожидание завершения процесса
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                return CompletableFuture.completedFuture(ResponseEntity.internalServerError().body(
                        ("Failed to generate image: " + output.toString()).getBytes()
                ));
            }

            // Чтение сгенерированного изображения в виде byte[]
            byte[] imageBytes = Files.readAllBytes(outputImagePath);

            // Возврат изображения в ответе
            return CompletableFuture.completedFuture(ResponseEntity.ok()
                    .contentType(MediaType.IMAGE_PNG)
                    .body(imageBytes));
        } catch (Exception e) {
            e.printStackTrace();
            return CompletableFuture.completedFuture(ResponseEntity.internalServerError().body(
                    ("Error: " + e.getMessage()).getBytes()
            ));
        }
    }
}