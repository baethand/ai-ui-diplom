package ru.mirea.diplom.ai_ui_diplom.model.exceptions;

import lombok.Data;
import ru.mirea.diplom.ai_ui_diplom.model.Error;

import java.util.ArrayList;
import java.util.List;

@Data
public class BaseException extends Exception{

    private List<Error> errors;

    public BaseException(String message) {
        super(message);
        this.errors = new ArrayList<>();
        this.errors.add(new Error(0, super.getLocalizedMessage(), message, true));
    }
}
