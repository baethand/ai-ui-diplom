package ru.mirea.diplom.ai_ui_diplom;

import java.io.File;
import java.net.URL;

public class PythonScriptTest {
    public static void main(String[] args) {
        try {
            // Получение пути к ресурсу
            URL resourceUrl = PythonScriptTest.class.getClassLoader().getResource("python/generate_image.py");
            if (resourceUrl == null) {
                throw new RuntimeException("Script not found!");
            }

            // Преобразование URL в путь к файлу
            File scriptFile = new File(resourceUrl.toURI());
            String pythonScriptPath = scriptFile.getAbsolutePath();

            // Вывод пути для проверки
            System.out.println("Python script path: " + pythonScriptPath);

            // Теперь можно использовать pythonScriptPath для запуска скрипта
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}