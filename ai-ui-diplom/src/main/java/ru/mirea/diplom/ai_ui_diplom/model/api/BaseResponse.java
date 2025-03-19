package ru.mirea.diplom.ai_ui_diplom.model.api;

import lombok.AllArgsConstructor;
import lombok.Data;
import ru.mirea.diplom.ai_ui_diplom.model.Error;

@Data
@AllArgsConstructor
public class BaseResponse<T> {
    private T result;
    private Error errors;
}
