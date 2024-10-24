package com.ohgiraffers.apirequest.section01.dto;

import lombok.*;


@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class ResponseDTO {

    private String summary;
    private String sentiment;
}
