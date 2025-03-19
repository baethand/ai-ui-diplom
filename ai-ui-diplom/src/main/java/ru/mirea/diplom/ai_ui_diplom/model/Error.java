package ru.mirea.diplom.ai_ui_diplom.model;

import lombok.Data;

@Data
public class Error {
    private Integer id;
    private String code;
    private String message;
    private Boolean isCritical;

    public Error(Exception e) {
        this.id = 0;
        this.code = e.getClass().getName();
        this.message = e.getMessage();
        this.isCritical = true;
    }

    public Error(Integer id, String code, Exception e) {
        this.id = id;
        this.code = code;
        this.message = e.getMessage();
        this.isCritical = true;
    }

    public Error(Integer id, String code, Exception e, Boolean isCritical) {
        this.id = id;
        this.code = code;
        this.message = e.getMessage();
        this.isCritical = isCritical;
    }

    public Error(Integer id, String code, String message, Boolean isCritical) {
        this.id = id;
        this.code = code;
        this.message = message;
        this.isCritical = isCritical;
    }

}
