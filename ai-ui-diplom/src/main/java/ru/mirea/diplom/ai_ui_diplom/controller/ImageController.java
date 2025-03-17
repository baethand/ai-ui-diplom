package ru.mirea.diplom.ai_ui_diplom.controller;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.web.bind.annotation.*;

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

    // Минимальные и максимальные значения параметров
    private static final int MIN_STEPS = 10;
    private static final int MAX_STEPS = 100;
    private static final float MIN_GUIDANCE_SCALE = 1.0f;
    private static final float MAX_GUIDANCE_SCALE = 20.0f;
    private static final int MIN_HEIGHT = 256;
    private static final int MAX_HEIGHT = 1024;
    private static final int MIN_WIDTH = 256;
    private static final int MAX_WIDTH = 1024;

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
            // Проверка на адекватность параметров
            if (prompt == null || prompt.trim().isEmpty()) {
                return CompletableFuture.completedFuture(ResponseEntity.badRequest().body("Prompt cannot be empty!".getBytes()));
            }
            if (numInferenceSteps < MIN_STEPS || numInferenceSteps > MAX_STEPS) {
                return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(
                        String.format("numInferenceSteps must be between %d and %d.", MIN_STEPS, MAX_STEPS).getBytes()
                ));
            }
            if (guidanceScale < MIN_GUIDANCE_SCALE || guidanceScale > MAX_GUIDANCE_SCALE) {
                return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(
                        String.format("guidanceScale must be between %.1f and %.1f.", MIN_GUIDANCE_SCALE, MAX_GUIDANCE_SCALE).getBytes()
                ));
            }
            if (height < MIN_HEIGHT || height > MAX_HEIGHT || width < MIN_WIDTH || width > MAX_WIDTH) {
                return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(
                        String.format("Height and width must be between %d and %d.", MIN_HEIGHT, MAX_HEIGHT).getBytes()
                ));
            }
            if (!device.equals("cuda") && !device.equals("cpu")) {
                return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(
                        "Device must be either 'cuda' or 'cpu'.".getBytes()
                ));
            }

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